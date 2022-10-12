import pytest

from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.model.digital_twin import DigitalTwin
from jarvis_sdk.model.token_info import TokenInfo
from tests.helpers import data


def test_get_digital_twin_wrong_twin_id(capsys):
    digital_twin_id = "696e6479-6b69-465-8000-010f00000000"
    tenant_id = data.get_tenant()

    client = IdentityClient()
    assert client is not None

    response = client.get_digital_twin(digital_twin_id, tenant_id, [])
    captured = capsys.readouterr()

    assert (
        captured.out == "The digital twin id is not in UUID4 format:\nbadly formed hexadecimal UUID string\n"
    )
    assert response is None


def test_get_digital_twin_wrong_tenant_id(capsys):
    digital_twin_id = "534729fb-f1b9-43ad-b1c5-9bbc75ae7de8"
    tenant_id = "534729fb-f1b9-43ad-b1c5-9bbc75ae7de8"

    client = IdentityClient()
    assert client is not None

    response = client.get_digital_twin(digital_twin_id, tenant_id, [])
    captured = capsys.readouterr()

    assert "digital_twin was not found" in captured.out
    assert response is None


def test_get_digital_twin_wrong_format_tenant_id(capsys):
    digital_twin_id = "534729fb-f1b9-43ad-b1c5-9bbc75ae7de8"
    tenant_id = "gid:AAAAA2luZHlraURlgAADDwAAAAE"

    client = IdentityClient()
    assert client is not None

    response = client.get_digital_twin(digital_twin_id, tenant_id, [])
    captured = capsys.readouterr()

    assert captured.out == "The tenant id is not in UUID4 format:\nbadly formed hexadecimal UUID string\n"
    assert response is None


def test_get_digital_twin_nonexisting_twin_id(capsys):
    digital_twin_id = "696e6479-6b69-4465-8000-030f00000001"
    tenant_id = data.get_tenant()

    client = IdentityClient()
    assert client is not None

    response = client.get_digital_twin(digital_twin_id, tenant_id, [])
    captured = capsys.readouterr()

    assert "digital_twin was not found" in captured.out
    assert response is None


def test_get_digital_twin_unknown_property(capsys):
    digital_twin_id = "e1e9f07d-fc6e-4629-84d1-8d23836524ba"
    tenant_id = data.get_tenant()

    client = IdentityClient()
    assert client is not None

    response = client.get_digital_twin(digital_twin_id, tenant_id, ["test_property"])
    captured = capsys.readouterr()

    assert "unknown property 'test_property'" in captured.out
    assert response is None


def test_get_digital_twin_success(capsys):
    digital_twin_id = data.get_digital_twin()
    tenant_id = data.get_tenant()

    client = IdentityClient()
    assert client is not None

    response = client.get_digital_twin(digital_twin_id, tenant_id, [])
    captured = capsys.readouterr()

    assert response is not None
    assert isinstance(response["digitalTwin"], DigitalTwin)


def test_get_digital_twin_by_token_short_token(capsys):
    token = "short_token"
    password = data.get_new_password()

    client = IdentityClient()
    assert client is not None

    response = client.get_digital_twin_by_token(token, [])
    captured = capsys.readouterr()

    assert captured.out == "Token must be 32 chars or more.\n"
    assert response is None


def test_get_digital_twin_by_token_expired_token(capsys):
    token = data.get_expired_token()

    client = IdentityClient()
    assert client is not None

    response = client.get_digital_twin_by_token(token, [])
    captured = capsys.readouterr()

    assert "invalid or expired access_token" in captured.out
    assert response is None


def test_get_digital_twin_by_token_success(registration):
    token = registration[0]

    client = IdentityClient()
    assert client is not None

    response = client.get_digital_twin_by_token(token, [])

    assert response is not None
    assert isinstance(response["digitalTwin"], DigitalTwin)
    assert isinstance(response["tokenInfo"], TokenInfo)
