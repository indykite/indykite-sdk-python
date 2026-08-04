"""Shared fixtures for the SDK test suite."""

from __future__ import annotations

import pytest

from indykite_sdk import Credentials

_ENV_VARS = (
    "INDYKITE_SERVICE_ACCOUNT_CREDENTIALS",
    "INDYKITE_SERVICE_ACCOUNT_CREDENTIALS_FILE",
    "INDYKITE_APPLICATION_CREDENTIALS",
    "INDYKITE_APPLICATION_CREDENTIALS_FILE",
    "INDYKITE_BASE_URL",
    "INDYKITE_REGION",
)

APP_AGENT_TOKEN = "app-agent-token-value"


@pytest.fixture(autouse=True)
def _clean_indykite_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep the developer's real credentials/env out of unit tests."""
    for var in _ENV_VARS:
        monkeypatch.delenv(var, raising=False)


@pytest.fixture
def app_agent_credentials() -> Credentials:
    """Application-agent credentials: the raw credential token, nothing else."""
    return Credentials.from_token(APP_AGENT_TOKEN)


@pytest.fixture
def service_account_credentials_dict() -> dict:
    """A service-account credential JSON artifact (pre-issued static token)."""
    return {
        "serviceAccountId": "gid:serviceaccount-123",
        "baseUrl": "",
        "token": "service-account-token-value",
    }


@pytest.fixture
def service_account_credentials(service_account_credentials_dict: dict) -> Credentials:
    """Service account credentials."""
    return Credentials.from_json(service_account_credentials_dict)


@pytest.fixture
def jwk_credentials_dict() -> dict:
    """A service-account credential JSON with only private-key material (no token)."""
    from joserfc.jwk import ECKey

    key = ECKey.generate_key("P-256", private=True)
    jwk = key.as_dict(private=True)
    jwk.update({"alg": "ES256", "use": "sig", "kid": "test-kid"})
    return {
        "serviceAccountId": "gid:serviceaccount-keyonly",
        "endpoint": "jarvis.indykite.com",
        "privateKeyJWK": jwk,
    }
