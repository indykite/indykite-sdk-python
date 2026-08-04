"""Auth headers: raw app-agent token, service-account token source + JWT minting."""

from __future__ import annotations

import base64
import json
import time

import httpx
import pytest

from indykite_sdk import Credentials, CredentialsError
from indykite_sdk._core import auth as auth_module
from indykite_sdk._core.auth import AppAgentAuth, ServiceAccountAuth, _parse_lifetime_seconds


def _apply(auth: httpx.Auth) -> httpx.Request:
    request = httpx.Request("POST", "https://eu.api.indykite.com/access/v1/evaluation")
    flow = auth.auth_flow(request)
    try:
        return next(flow)
    except StopIteration as exc:
        raise AssertionError("auth flow yielded no request") from exc


def _jwt_with_exp(exp: float) -> str:
    header = base64.urlsafe_b64encode(b'{"alg":"none"}').rstrip(b"=").decode()
    payload = base64.urlsafe_b64encode(json.dumps({"exp": exp}).encode()).rstrip(b"=").decode()
    return f"{header}.{payload}."


def test_app_agent_auth_sends_raw_token_verbatim(app_agent_credentials: Credentials) -> None:
    """App agent auth sends raw token verbatim."""
    request = _apply(AppAgentAuth(app_agent_credentials))
    assert request.headers["X-IK-ClientKey"] == "app-agent-token-value"
    assert "Authorization" not in request.headers


def test_app_agent_auth_requires_a_token(jwk_credentials_dict: dict) -> None:
    # Key material is a control-plane concept; the runtime plane needs the token itself.
    """App agent auth requires a token."""
    credentials = Credentials.from_json(jwk_credentials_dict)
    with pytest.raises(CredentialsError, match="raw credential token"):
        AppAgentAuth(credentials)


def test_service_account_pre_issued_token_opaque_token_is_sent_and_never_refreshed(
    service_account_credentials: Credentials,
) -> None:
    """Service account pre issued token opaque token is sent and never refreshed."""
    auth = ServiceAccountAuth(service_account_credentials)
    assert _apply(auth).headers["Authorization"] == "Bearer service-account-token-value"
    assert _apply(auth).headers["Authorization"] == "Bearer service-account-token-value"


def test_service_account_pre_issued_token_valid_jwt_token_is_used_until_expiry(jwk_credentials_dict: dict) -> None:
    """Service account pre issued token valid jwt token is used until expiry."""
    token = _jwt_with_exp(time.time() + 3600)
    credentials = Credentials.from_json(dict(jwk_credentials_dict, token=token))
    auth = ServiceAccountAuth(credentials)
    assert _apply(auth).headers["Authorization"] == f"Bearer {token}"


def test_service_account_pre_issued_token_expired_jwt_token_triggers_minting_when_key_present(
    jwk_credentials_dict: dict,
) -> None:
    """Service account pre issued token expired jwt token triggers minting when key present."""
    from joserfc import jwt
    from joserfc.jwk import ECKey

    expired = _jwt_with_exp(time.time() - 10)
    credentials = Credentials.from_json(dict(jwk_credentials_dict, token=expired))
    auth = ServiceAccountAuth(credentials)
    sent = _apply(auth).headers["Authorization"].removeprefix("Bearer ")
    assert sent != expired
    claims = jwt.decode(sent, ECKey.import_key(credentials.private_key_jwk), algorithms=["ES256"]).claims
    assert claims["iss"] == "gid:serviceaccount-keyonly"


def test_service_account_pre_issued_token_expired_token_without_key_is_still_sent() -> None:
    """Service account pre issued token expired token without key is still sent."""
    expired = _jwt_with_exp(time.time() - 10)
    credentials = Credentials.from_json({"serviceAccountId": "gid:sa", "token": expired})
    auth = ServiceAccountAuth(credentials)
    # Matches the Go SDK: nothing to mint with, so the platform gets to reject it.
    assert _apply(auth).headers["Authorization"] == f"Bearer {expired}"


def test_service_account_minting_signs_es256_jwt_with_thumbprint_kid(jwk_credentials_dict: dict) -> None:
    """Service account minting signs es256 jwt with thumbprint kid."""
    from joserfc import jwt
    from joserfc.jwk import ECKey

    credentials = Credentials.from_json(jwk_credentials_dict)
    request = _apply(ServiceAccountAuth(credentials))
    token = request.headers["Authorization"].removeprefix("Bearer ")
    claims = jwt.decode(token, ECKey.import_key(credentials.private_key_jwk), algorithms=["ES256"]).claims
    assert claims["iss"] == "gid:serviceaccount-keyonly"
    assert claims["sub"] == "gid:serviceaccount-keyonly"
    assert claims["jti"]
    assert claims["exp"] - claims["iat"] == 3600
    header = json.loads(base64.urlsafe_b64decode(token.split(".")[0] + "=="))
    assert header["alg"] == "ES256"
    # kid is regenerated as the RFC 7638 thumbprint, like the platform does.
    assert header["kid"] == ECKey.import_key(credentials.private_key_jwk).thumbprint()


def test_service_account_minting_minted_token_is_cached(jwk_credentials_dict: dict) -> None:
    """Service account minting minted token is cached."""
    auth = ServiceAccountAuth(Credentials.from_json(jwk_credentials_dict))
    first = _apply(auth).headers["Authorization"]
    second = _apply(auth).headers["Authorization"]
    assert first == second


def test_service_account_minting_minted_token_is_resigned_after_expiry(
    jwk_credentials_dict: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Service account minting minted token is resigned after expiry."""
    auth = ServiceAccountAuth(Credentials.from_json(jwk_credentials_dict))
    first = _apply(auth).headers["Authorization"]
    real_time = time.time
    monkeypatch.setattr(auth_module.time, "time", lambda: real_time() + 3600)
    second = _apply(auth).headers["Authorization"]
    assert first != second


def test_service_account_minting_pkcs8_pem_key() -> None:
    """Service account minting pkcs8 pem key."""
    from cryptography.hazmat.primitives.asymmetric.ec import SECP256R1, generate_private_key
    from cryptography.hazmat.primitives.serialization import (
        Encoding,
        NoEncryption,
        PrivateFormat,
        PublicFormat,
    )
    from joserfc import jwt
    from joserfc.jwk import ECKey

    key = generate_private_key(SECP256R1())
    pem = key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()).decode()
    credentials = Credentials.from_json({"serviceAccountId": "gid:sa", "privateKeyPKCS8": pem})
    token = _apply(ServiceAccountAuth(credentials)).headers["Authorization"].removeprefix("Bearer ")
    public_pem = key.public_key().public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
    claims = jwt.decode(token, ECKey.import_key(public_pem), algorithms=["ES256"]).claims
    assert claims["sub"] == "gid:sa"


def test_service_account_minting_pkcs8_base64_der_key() -> None:
    """Service account minting pkcs8 base64 der key."""
    from cryptography.hazmat.primitives.asymmetric.ec import SECP256R1, generate_private_key
    from cryptography.hazmat.primitives.serialization import Encoding, NoEncryption, PrivateFormat

    key = generate_private_key(SECP256R1())
    der = key.private_bytes(Encoding.DER, PrivateFormat.PKCS8, NoEncryption())
    credentials = Credentials.from_json(
        {"serviceAccountId": "gid:sa", "privateKeyPKCS8Base64": base64.standard_b64encode(der).decode()}
    )
    token = _apply(ServiceAccountAuth(credentials)).headers["Authorization"].removeprefix("Bearer ")
    assert token.count(".") == 2


def test_service_account_minting_missing_subject_raises(jwk_credentials_dict: dict) -> None:
    """Service account minting missing subject raises."""
    jwk_credentials_dict.pop("serviceAccountId")
    credentials = Credentials.from_json(jwk_credentials_dict)
    with pytest.raises(CredentialsError, match="serviceAccountId"):
        _apply(ServiceAccountAuth(credentials))


@pytest.mark.parametrize(
    ("lifetime", "expected"),
    [
        ("30m", 1800),
        ("1h", 3600),
        ("4h15m", 15300),
        ("1d", 86400),
        (None, 3600),  # default
        ("", 3600),  # default
        ("1m", 3600),  # below 2-minute floor -> default
        ("2d", 3600),  # above 24-hour ceiling -> default
        ("garbage", 3600),  # unparsable -> default
    ],
)
def test_parse_lifetime_lifetimes(lifetime: str | None, expected: int) -> None:
    """Parse lifetime lifetimes."""
    assert _parse_lifetime_seconds(lifetime) == expected
