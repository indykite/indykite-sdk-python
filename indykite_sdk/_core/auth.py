"""httpx auth implementations for the two IndyKite credential planes.

- :class:`AppAgentAuth` (runtime plane) — the App Agent credential token sent
  verbatim in ``X-IK-ClientKey``. The credential *is* the token; no JWT is
  ever minted and no key material is involved.
- :class:`ServiceAccountAuth` (control plane, Config API) -
  ``Authorization: Bearer <token>``. The pre-issued ``token`` from the
  credential JSON is sent as-is while it is valid; once it expires, a fresh
  JWT is self-signed from the credential's private key (JWK or PKCS#8) with a
  key-thumbprint ``kid``, cached, and re-signed 60 seconds before expiry.

This mirrors the behavior of the IndyKite Go SDK (`indykite-sdk-go/auth`).
"""

from __future__ import annotations

import base64
import json
import re
import threading
import time
import uuid
from collections.abc import Generator
from datetime import timedelta
from typing import TYPE_CHECKING, Any

import httpx

from indykite_sdk.errors import CredentialsError

if TYPE_CHECKING:
    from indykite_sdk._core.credentials import Credentials

_TOKEN_LIFETIME_PATTERN = re.compile(r"((?P<days>-?\d+)d)?((?P<hours>-?\d+)h)?((?P<minutes>-?\d+)m)?", re.IGNORECASE)
_MIN_LIFETIME_S = 120
_MAX_LIFETIME_S = 86400
_DEFAULT_LIFETIME_S = 3600
#: Tokens are refreshed this many seconds before their expiry.
_REFRESH_MARGIN_S = 60


def _parse_lifetime_seconds(lifetime: str | None) -> int:
    """Parse a ``"30m"`` / ``"1h"`` / ``"1d4h"`` lifetime, clamped to [2 min, 24 h]."""
    seconds = None
    if lifetime:
        match = _TOKEN_LIFETIME_PATTERN.match(lifetime)
        if match:
            parts = {k: int(v) for k, v in match.groupdict().items() if v}
            if parts:
                seconds = int(timedelta(**parts).total_seconds())
    if seconds is None or not _MIN_LIFETIME_S <= seconds <= _MAX_LIFETIME_S:
        return _DEFAULT_LIFETIME_S
    return seconds


def _pre_issued_expiry(token: str) -> float | None:
    """Effective expiry of a pre-issued token: 60 s before its JWT ``exp`` claim.

    Returns ``None`` (never expires) for opaque tokens or JWTs without ``exp``.
    The signature is NOT verified - the platform does that.
    """
    parts = token.split(".")
    if len(parts) != 3:
        return None
    try:
        payload_raw = base64.urlsafe_b64decode(parts[1] + "=" * (-len(parts[1]) % 4))
        payload = json.loads(payload_raw)
    except ValueError:  # binascii.Error is a ValueError subclass
        return None
    exp = payload.get("exp") if isinstance(payload, dict) else None
    if not isinstance(exp, (int, float)):
        return None
    return float(exp) - _REFRESH_MARGIN_S


def _import_pkcs8_key(key: Any) -> Any:
    """Wrap a cryptography private key in the matching joserfc key class."""
    from cryptography.hazmat.primitives.asymmetric import (  # skipcq: PYL-C0415 - lazy, only needed when signing
        ec,
        ed448,
        ed25519,
        rsa,
    )
    from joserfc.jwk import ECKey, OKPKey, RSAKey  # skipcq: PYL-C0415 - lazy, only needed when signing

    if isinstance(key, ec.EllipticCurvePrivateKey):
        return ECKey.import_key(key)
    if isinstance(key, rsa.RSAPrivateKey):
        return RSAKey.import_key(key)
    if isinstance(key, (ed25519.Ed25519PrivateKey, ed448.Ed448PrivateKey)):
        return OKPKey.import_key(key)
    raise CredentialsError(f"Unsupported private key type {type(key).__name__!r} in credentials.")


def _load_signing_key(credentials: Credentials) -> Any:
    """Load the credential's private key (JWK or PKCS#8) as a joserfc key."""
    if credentials.private_key_jwk:
        from joserfc.jwk import JWKRegistry  # skipcq: PYL-C0415 - lazy, only needed when signing

        # Drop any embedded kid; it is regenerated as the RFC 7638 thumbprint
        # below, the same way the platform derives it.
        jwk = {name: value for name, value in credentials.private_key_jwk.items() if name != "kid"}
        return JWKRegistry.import_key(jwk)
    if credentials.private_key_pkcs8_base64:
        try:
            der = base64.standard_b64decode(credentials.private_key_pkcs8_base64)
        except ValueError as exc:  # binascii.Error is a ValueError subclass
            raise CredentialsError(f"privateKeyPKCS8Base64 is not valid base64: {exc}") from exc
        from cryptography.hazmat.primitives.serialization import (  # skipcq: PYL-C0415 - lazy, only needed when signing
            load_der_private_key,
        )

        return _import_pkcs8_key(load_der_private_key(der, password=None))
    if credentials.private_key_pkcs8:
        from cryptography.hazmat.primitives.serialization import (  # skipcq: PYL-C0415 - lazy, only needed when signing
            load_pem_private_key,
        )

        return _import_pkcs8_key(load_pem_private_key(credentials.private_key_pkcs8.encode(), password=None))
    raise CredentialsError("Credential JSON has no private key to sign a JWT with.")


def _infer_algorithm(key: Any) -> str:
    """Choose the signing algorithm the way the platform expects."""
    if key.key_type == "EC":
        return {"P-256": "ES256", "P-384": "ES384", "P-521": "ES512"}.get(key.curve_name, "ES256")
    if key.key_type == "RSA":
        return "RS256"
    if key.key_type == "OKP":
        return "EdDSA"
    raise CredentialsError(f"Unsupported private key type {key.key_type!r} in credentials.")


class _ServiceAccountTokenProvider:
    """Go-SDK-equivalent token source: pre-issued token while valid, then self-signed JWTs."""

    def __init__(self, credentials: Credentials) -> None:
        self._credentials = credentials
        self._pre_issued = credentials.token
        self._pre_issued_expiry = _pre_issued_expiry(credentials.token) if credentials.token else None
        self._lock = threading.Lock()
        self._minted_token: str | None = None
        self._minted_expiry: float = 0.0

    def token(self) -> str:
        """The bearer token to send: pre-issued while valid, else a cached self-signed JWT."""
        now = time.time()
        if self._pre_issued and (self._pre_issued_expiry is None or now < self._pre_issued_expiry):
            return self._pre_issued
        if not self._credentials.has_private_key():
            if self._pre_issued:
                # Expired pre-issued token and nothing to mint with: send it
                # anyway and let the platform reject it (matches the Go SDK).
                return self._pre_issued
            raise CredentialsError(
                "Service-account credential has neither a 'token' nor private key material to sign a JWT with."
            )
        with self._lock:
            if self._minted_token is None or time.time() >= self._minted_expiry - _REFRESH_MARGIN_S:
                self._minted_token, self._minted_expiry = self._mint()
            return self._minted_token

    def _mint(self) -> tuple[str, float]:
        client_id = self._credentials.service_account_id or self._credentials.app_agent_id
        if not client_id:
            raise CredentialsError("Credential JSON has no 'serviceAccountId'; cannot self-sign a JWT.")
        from joserfc import jwt  # skipcq: PYL-C0415 - lazy, only needed when signing

        key = _load_signing_key(self._credentials)
        algorithm = self._credentials.private_key_jwk.get("alg") if self._credentials.private_key_jwk else None
        algorithm = algorithm or _infer_algorithm(key)
        # Regenerate the kid the same way the backend does (RFC 7638 thumbprint).
        kid = key.thumbprint()
        now = int(time.time())
        expiry = now + _parse_lifetime_seconds(self._credentials.token_lifetime)
        claims = {
            "exp": expiry,
            "iat": now,
            "iss": client_id,
            "jti": str(uuid.uuid4()),
            "sub": client_id,
        }
        return jwt.encode({"alg": algorithm, "kid": kid}, claims, key), float(expiry)


class ServiceAccountAuth(httpx.Auth):
    """``Authorization: Bearer <service-account token>`` - Config API only."""

    def __init__(self, credentials: Credentials) -> None:
        self._provider = _ServiceAccountTokenProvider(credentials)

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response]:
        request.headers["Authorization"] = f"Bearer {self._provider.token()}"
        yield request


class AppAgentAuth(httpx.Auth):
    """``X-IK-ClientKey: <application-agent credential token>`` - all data-plane APIs.

    The token is sent verbatim, without any prefix. The ``Authorization``
    header stays free for an optional end-user access token.
    """

    def __init__(self, credentials: Credentials) -> None:
        if not credentials.token:
            raise CredentialsError(
                "The application-agent credential must be the raw credential token "
                "(INDYKITE_APPLICATION_CREDENTIALS holds the token itself, not a JSON document)."
            )
        self._token = credentials.token

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response]:
        request.headers["X-IK-ClientKey"] = self._token
        yield request
