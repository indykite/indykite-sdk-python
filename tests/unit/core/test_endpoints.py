"""Base-URL resolution precedence (base_url > region > credential hint > default)."""

from __future__ import annotations

import pytest

from indykite_sdk import Credentials, CredentialsError
from indykite_sdk._core.endpoints import resolve_base_url


def test_default_is_eu_production() -> None:
    """Default is eu production."""
    assert resolve_base_url() == "https://eu.api.indykite.com"


def test_region_argument() -> None:
    """Region argument."""
    assert resolve_base_url(region="us") == "https://us.api.indykite.com"


def test_region_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    """Region env var."""
    monkeypatch.setenv("INDYKITE_REGION", "us")
    assert resolve_base_url() == "https://us.api.indykite.com"


def test_unknown_region_raises() -> None:
    """Unknown region raises."""
    with pytest.raises(CredentialsError, match="region"):
        resolve_base_url(region="mars")


def test_base_url_argument_wins_over_everything(monkeypatch: pytest.MonkeyPatch) -> None:
    """Base url argument wins over everything."""
    monkeypatch.setenv("INDYKITE_BASE_URL", "https://api.rc.indykite.xyz")
    assert resolve_base_url(base_url="https://api.dev.indykite.xyz") == "https://api.dev.indykite.xyz"


def test_env_base_url_wins_over_region(monkeypatch: pytest.MonkeyPatch) -> None:
    """Env base url wins over region."""
    monkeypatch.setenv("INDYKITE_BASE_URL", "https://api.dev.indykite.xyz/")
    assert resolve_base_url(region="us") == "https://api.dev.indykite.xyz"


def test_region_wins_over_credential_base_url() -> None:
    """Region wins over credential base url."""
    credentials = Credentials.from_json({"token": "t", "baseUrl": "https://api.dev.indykite.xyz"})
    assert resolve_base_url(credentials=credentials, region="us") == "https://us.api.indykite.com"


def test_credential_base_url_used_when_http() -> None:
    """Credential base url used when http."""
    credentials = Credentials.from_json({"token": "t", "baseUrl": "https://us.api.indykite.com"})
    assert resolve_base_url(credentials=credentials) == "https://us.api.indykite.com"


def test_credential_http_endpoint_used_as_fallback() -> None:
    """Credential http endpoint used as fallback."""
    credentials = Credentials.from_json({"token": "t", "endpoint": "https://api.dev.indykite.xyz"})
    assert resolve_base_url(credentials=credentials) == "https://api.dev.indykite.xyz"


def test_non_http_endpoint_is_ignored() -> None:
    """Non http endpoint is ignored."""
    credentials = Credentials.from_json({"token": "t", "endpoint": "jarvis.indykite.com"})
    assert resolve_base_url(credentials=credentials) == "https://eu.api.indykite.com"


def test_credential_base_url_without_scheme_is_ignored() -> None:
    """Credential base url without scheme is ignored."""
    credentials = Credentials.from_json({"token": "t", "baseUrl": "jarvis.indykite.com"})
    assert resolve_base_url(credentials=credentials) == "https://eu.api.indykite.com"


def test_invalid_explicit_base_url_raises() -> None:
    """Invalid explicit base url raises."""
    with pytest.raises(CredentialsError, match="http"):
        resolve_base_url(base_url="ftp://example.com")
