"""Credentials loading: raw app-agent tokens, service-account JSON, env precedence."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from indykite_sdk import Credentials, CredentialsError


def test_app_agent_token_from_token() -> None:
    """App agent token from token."""
    credentials = Credentials.from_token("  ik1_raw-token \n")
    assert credentials.token == "ik1_raw-token"
    assert not credentials.has_private_key()


def test_app_agent_token_json_document_is_rejected() -> None:
    """App agent token json document is rejected."""
    with pytest.raises(CredentialsError, match="raw credential token, not a JSON document"):
        Credentials.from_token('{"appAgentId": "gid:x", "token": "t"}')


def test_app_agent_token_empty_token_is_rejected() -> None:
    """App agent token empty token is rejected."""
    with pytest.raises(CredentialsError, match="empty"):
        Credentials.from_token("   ")


def test_app_agent_token_from_env_inline(monkeypatch: pytest.MonkeyPatch) -> None:
    """App agent token from env inline."""
    monkeypatch.setenv("INDYKITE_APPLICATION_CREDENTIALS", "ik1_from-env")  # gitleaks:allow
    assert Credentials.from_env("app_agent").token == "ik1_from-env"  # gitleaks:allow


def test_app_agent_token_from_env_file_holds_raw_token(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """App agent token from env file holds raw token."""
    path = tmp_path / "app-agent.txt"
    path.write_text("ik1_from-file\n")
    monkeypatch.setenv("INDYKITE_APPLICATION_CREDENTIALS_FILE", str(path))
    assert Credentials.from_env("app_agent").token == "ik1_from-file"


def test_app_agent_token_from_env_rejects_json(monkeypatch: pytest.MonkeyPatch) -> None:
    """App agent token from env rejects json."""
    monkeypatch.setenv("INDYKITE_APPLICATION_CREDENTIALS", '{"token": "t"}')
    with pytest.raises(CredentialsError, match="raw credential token"):
        Credentials.from_env("app_agent")


def test_service_account_json_parses_recent_format_with_token(service_account_credentials_dict: dict) -> None:
    """Service account json parses recent format with token."""
    credentials = Credentials.from_json(service_account_credentials_dict)
    assert credentials.service_account_id == "gid:serviceaccount-123"
    assert credentials.token == "service-account-token-value"


def test_service_account_json_parses_json_string(service_account_credentials_dict: dict) -> None:
    """Service account json parses json string."""
    credentials = Credentials.from_json(json.dumps(service_account_credentials_dict))
    assert credentials.token == "service-account-token-value"


def test_service_account_json_parses_key_only_format(jwk_credentials_dict: dict) -> None:
    """Service account json parses key only format."""
    credentials = Credentials.from_json(jwk_credentials_dict)
    assert credentials.token is None
    assert credentials.has_private_key()
    assert credentials.private_key_jwk is not None
    assert credentials.private_key_jwk["kty"] == "EC"


def test_service_account_json_accepts_pkcs8_key_material() -> None:
    """Service account json accepts pkcs8 key material."""
    credentials = Credentials.from_json(
        {"serviceAccountId": "gid:sa", "privateKeyPKCS8Base64": "QUJD", "privateKeyPKCS8": "-----BEGIN..."}
    )
    assert credentials.has_private_key()


def test_service_account_json_accepts_snake_case_field_names() -> None:
    """Service account json accepts snake case field names."""
    credentials = Credentials.from_json({"service_account_id": "gid:x", "token": "t"})
    assert credentials.service_account_id == "gid:x"


def test_service_account_json_keeps_unknown_fields(service_account_credentials_dict: dict) -> None:
    """Service account json keeps unknown fields."""
    service_account_credentials_dict["somethingNew"] = "abc"
    credentials = Credentials.from_json(service_account_credentials_dict)
    assert credentials.model_extra is not None
    assert credentials.model_extra["somethingNew"] == "abc"


def test_service_account_json_rejects_invalid_json() -> None:
    """Service account json rejects invalid json."""
    with pytest.raises(CredentialsError, match="not valid JSON"):
        Credentials.from_json("{not json")


def test_service_account_json_rejects_non_object_json() -> None:
    """Service account json rejects non object json."""
    with pytest.raises(CredentialsError, match="must be an object"):
        Credentials.from_json("[1, 2]")


def test_service_account_json_rejects_credential_without_token_or_key() -> None:
    """Service account json rejects credential without token or key."""
    with pytest.raises(CredentialsError, match="neither 'token' nor private key"):
        Credentials.from_json({"serviceAccountId": "gid:x"})


def test_from_file_loads_service_account_file(tmp_path: Path, service_account_credentials_dict: dict) -> None:
    """From file loads service account file."""
    path = tmp_path / "credentials.json"
    path.write_text(json.dumps(service_account_credentials_dict))
    credentials = Credentials.from_file(path)
    assert credentials.token == "service-account-token-value"


def test_from_file_missing_file_raises_credentials_error(tmp_path: Path) -> None:
    """From file missing file raises credentials error."""
    with pytest.raises(CredentialsError, match="Cannot read credential file"):
        Credentials.from_file(tmp_path / "missing.json")


def test_from_env_inline_json_wins_over_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    service_account_credentials_dict: dict,
) -> None:
    """From env inline json wins over file."""
    file_credentials = dict(service_account_credentials_dict, token="file-token")
    path = tmp_path / "credentials.json"
    path.write_text(json.dumps(file_credentials))
    monkeypatch.setenv("INDYKITE_SERVICE_ACCOUNT_CREDENTIALS", json.dumps(service_account_credentials_dict))
    monkeypatch.setenv("INDYKITE_SERVICE_ACCOUNT_CREDENTIALS_FILE", str(path))
    assert Credentials.from_env("service_account").token == "service-account-token-value"


def test_from_env_falls_back_to_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    service_account_credentials_dict: dict,
) -> None:
    """From env falls back to file."""
    path = tmp_path / "sa.json"
    path.write_text(json.dumps(service_account_credentials_dict))
    monkeypatch.setenv("INDYKITE_SERVICE_ACCOUNT_CREDENTIALS_FILE", str(path))
    assert Credentials.from_env("service_account").service_account_id == "gid:serviceaccount-123"


def test_from_env_missing_env_raises_with_var_names() -> None:
    """From env missing env raises with var names."""
    with pytest.raises(CredentialsError, match="INDYKITE_APPLICATION_CREDENTIALS"):
        Credentials.from_env("app_agent")
    with pytest.raises(CredentialsError, match="INDYKITE_SERVICE_ACCOUNT_CREDENTIALS"):
        Credentials.from_env("service_account")
