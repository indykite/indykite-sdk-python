import pytest

from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.model.digital_twin import DigitalTwinCore
from tests.helpers import data


def test_verify_digital_twin_email_short_token(capsys):
    token = "short_token"

    client = IdentityClient()
    assert client is not None

    response = client.verify_digital_twin_email(token)
    captured = capsys.readouterr()

    assert captured.out == "Token must be 32 chars or more.\n"
    assert response is None


def test_verify_digital_twin_email_invalid_token(capsys):
    token = data.get_expired_token()

    client = IdentityClient()
    assert client is not None

    response = client.verify_digital_twin_email(token)
    captured = capsys.readouterr()

    assert "invalid token format" in captured.out
    assert response is None


def test_verify_digital_twin_email_success(registration_until_email_arrives):
    token = registration_until_email_arrives

    client = IdentityClient()
    assert client is not None

    response = client.verify_digital_twin_email(token)

    #assert isinstance(response, DigitalTwinCore)


def test_start_digital_twin_email_verification_wrong_twin_id(capsys):
    digital_twin_id = "696e6479-6b69-465-8000-010f00000000"
    tenant_id = data.get_tenant()
    email = data.get_new_email()

    client = IdentityClient()
    assert client is not None

    response = client.start_digital_twin_email_verification(digital_twin_id, tenant_id, email)
    captured = capsys.readouterr()

    assert (
        captured.out == "The digital twin id is not in UUID4 format:\nbadly formed hexadecimal UUID string\n"
    )
    assert response is None


def test_start_digital_twin_email_verification_wrong_tenant_id(capsys):
    digital_twin_id = "696e6479-6b69-4465-8000-010f00000000"
    tenant_id = "696e6479-6b6-4465-8000-010f00000000"
    email = data.get_new_email()

    client = IdentityClient()
    assert client is not None

    response = client.start_digital_twin_email_verification(digital_twin_id, tenant_id, email)
    captured = capsys.readouterr()

    assert captured.out == "The tenant id is not in UUID4 format:\nbadly formed hexadecimal UUID string\n"
    assert response is None


def test_start_digital_twin_email_verification_nonexisting_twin_id(capsys):
    digital_twin_id = "e1e9f07d-fc6e-4629-84d1-8d23836524ba"
    tenant_id = data.get_tenant()
    email = data.get_new_email()

    client = IdentityClient()
    assert client is not None

    response = client.start_digital_twin_email_verification(digital_twin_id, tenant_id, email)
    captured = capsys.readouterr()

    assert "digital_twin was not found" in captured.out
    assert response is None


def test_start_digital_twin_email_verification_invalid_email_address(capsys):
    digital_twin_id = "e1e9f07d-fc6e-4629-84d1-8d23836524ba"
    tenant_id = data.get_tenant()
    email = "invalid_email"

    client = IdentityClient()
    assert client is not None

    response = client.start_digital_twin_email_verification(digital_twin_id, tenant_id, email)
    captured = capsys.readouterr()

    assert "value must be a valid email address" in captured.out
    assert response is None


def test_start_digital_twin_email_verification_email_not_found(capsys):
    digital_twin_id = data.get_digital_twin()
    tenant_id = data.get_tenant()
    email = data.get_new_email()

    client = IdentityClient()
    assert client is not None

    response = client.start_digital_twin_email_verification(digital_twin_id, tenant_id, email)
    captured = capsys.readouterr()

    assert "email address is not found" or "digital_twin was not found" in captured.out
    assert response is None
