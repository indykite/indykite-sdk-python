"""Credential loading for the IndyKite REST APIs.

The platform has two planes with two different credential artifacts:

- **Runtime / data plane** (Capture, AuthZEN, ContX IQ, Data Schema, Entity
  Matching): the credential is the **Application Agent credential token
  itself** - an opaque string sent verbatim in the ``X-IK-ClientKey`` header.
  ``INDYKITE_APPLICATION_CREDENTIALS`` (or the file behind
  ``INDYKITE_APPLICATION_CREDENTIALS_FILE``) holds exactly that token, not a
  JSON document. No JWT is minted and no key material is involved.
- **Control plane** (Config API, ``/configs/v1``): the credential is a **JSON
  artifact** with ``serviceAccountId``, an optional ``baseUrl``, a pre-issued
  ``token``, and private key material. The token goes in
  ``Authorization: Bearer``; while the pre-issued token is valid it is sent
  as-is, and once it expires a fresh JWT is self-signed from the private key.
  Loaded from ``INDYKITE_SERVICE_ACCOUNT_CREDENTIALS`` (inline JSON) or
  ``INDYKITE_SERVICE_ACCOUNT_CREDENTIALS_FILE`` (path).
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Literal, Self

from pydantic import AliasChoices, Field, ValidationError

from indykite_sdk._core.models import IKResponseModel
from indykite_sdk.errors import CredentialsError

CredentialKind = Literal["service_account", "app_agent"]

_ENV_VARS: dict[str, tuple[str, str]] = {
    # kind -> (inline env var, file-path env var); inline wins.
    "service_account": ("INDYKITE_SERVICE_ACCOUNT_CREDENTIALS", "INDYKITE_SERVICE_ACCOUNT_CREDENTIALS_FILE"),
    "app_agent": ("INDYKITE_APPLICATION_CREDENTIALS", "INDYKITE_APPLICATION_CREDENTIALS_FILE"),
}


class Credentials(IKResponseModel):
    """A parsed IndyKite credential.

    For the **service account** this mirrors the credential JSON artifact
    (camelCase and snake_case both accepted). For the **application agent**
    only :attr:`token` is set - the credential *is* the token; build it with
    :meth:`from_token`.
    """

    #: Pre-issued credential token, sent verbatim (X-IK-ClientKey or Bearer).
    token: str | None = None
    app_agent_id: str | None = Field(default=None, validation_alias=AliasChoices("appAgentId", "app_agent_id"))
    application_id: str | None = Field(default=None, validation_alias=AliasChoices("applicationId", "application_id"))
    service_account_id: str | None = Field(
        default=None, validation_alias=AliasChoices("serviceAccountId", "service_account_id")
    )
    app_space_id: str | None = Field(default=None, validation_alias=AliasChoices("appSpaceId", "app_space_id"))
    base_url: str | None = Field(default=None, validation_alias=AliasChoices("baseUrl", "base_url"))
    #: Endpoint hint from the credential file; used as base URL only when it
    #: is an HTTP(S) URL (other values are ignored).
    endpoint: str | None = None
    private_key_jwk: dict[str, Any] | None = Field(
        default=None, validation_alias=AliasChoices("privateKeyJWK", "private_key_jwk")
    )
    private_key_pkcs8_base64: str | None = Field(
        default=None, validation_alias=AliasChoices("privateKeyPKCS8Base64", "private_key_pkcs8_base64")
    )
    private_key_pkcs8: str | None = Field(
        default=None,
        validation_alias=AliasChoices("privateKeyPKCS8", "private_key_pkcs8"),  # gitleaks:allow
    )
    #: Lifetime for self-signed JWTs, e.g. ``"30m"`` or ``"1h"``.
    token_lifetime: str | None = Field(default=None, validation_alias=AliasChoices("tokenLifetime", "token_lifetime"))

    def has_private_key(self) -> bool:
        """Whether any private-key form is present (JWK or PKCS#8)."""
        return bool(self.private_key_jwk or self.private_key_pkcs8_base64 or self.private_key_pkcs8)

    @classmethod
    def from_token(cls, token: str) -> Self:
        """Build application-agent credentials from the raw credential token.

        The App Agent credential is the token itself, sent verbatim in
        ``X-IK-ClientKey`` - it is never a JSON document.
        """
        token = token.strip()
        if not token:
            raise CredentialsError("The application-agent credential token is empty.")
        if token.startswith("{"):
            raise CredentialsError(
                "The App Agent credential is the raw credential token, not a JSON document. "
                "Pass the token value exactly as issued by the IndyKite Hub."
            )
        return cls(token=token)

    @classmethod
    def from_json(cls, data: str | bytes | dict[str, Any]) -> Self:
        """Parse a service-account credential JSON string or already-decoded dict."""
        if isinstance(data, (str, bytes)):
            try:
                data = json.loads(data)
            except json.JSONDecodeError as exc:
                raise CredentialsError(f"Credential content is not valid JSON: {exc}") from exc
        if not isinstance(data, dict):
            raise CredentialsError(f"Credential JSON must be an object, got {type(data).__name__}")
        try:
            credentials = cls.model_validate(data)
        except ValidationError as exc:
            raise CredentialsError(f"Credential JSON has invalid fields: {exc}") from exc
        if credentials.token is None and not credentials.has_private_key():
            raise CredentialsError(
                "Credential JSON contains neither 'token' nor private key material "
                "(privateKeyJWK / privateKeyPKCS8Base64 / privateKeyPKCS8). "
                "Download a fresh credential file from the IndyKite Hub."
            )
        return credentials

    @classmethod
    def from_file(cls, path: str | Path, kind: CredentialKind = "service_account") -> Self:
        """Load a credential file: JSON for a service account, the raw token for an app agent."""
        try:
            content = Path(path).read_text(encoding="utf-8")
        except OSError as exc:
            raise CredentialsError(f"Cannot read credential file {path!r}: {exc}") from exc
        if kind == "app_agent":
            return cls.from_token(content)
        return cls.from_json(content)

    @classmethod
    def from_env(cls, kind: CredentialKind) -> Self:
        """Load credentials from the standard environment variables for ``kind``.

        The inline variable takes precedence over the file-path variable. For
        ``app_agent`` the value/file content is the raw credential token; for
        ``service_account`` it is the credential JSON.
        """
        inline_var, file_var = _ENV_VARS[kind]
        inline = os.environ.get(inline_var)
        if inline:
            return cls.from_token(inline) if kind == "app_agent" else cls.from_json(inline)
        file_path = os.environ.get(file_var)
        if file_path:
            return cls.from_file(file_path, kind)
        what = "credential token" if kind == "app_agent" else "credential JSON"
        raise CredentialsError(
            f"No credentials provided and neither {inline_var} (inline {what}) nor {file_var} (file path) is set."
        )
