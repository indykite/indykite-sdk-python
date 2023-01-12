from indykite_sdk.identity import IdentityClient
from helpers import data


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


def test_verify_digital_twin_email_success(registration_until_email_arrives, capsys):
    token = registration_until_email_arrives

    client = IdentityClient()
    assert client is not None

    response = client.verify_digital_twin_email(token)
    captured = capsys.readouterr()

    assert response is not None or "property does not belong under current application" in captured.out


def test_start_digital_twin_email_verification_wrong_twin_id(capsys):
    digital_twin_id = "gid:AAAAAla6PZwUpk6Lizs5Iki3NDE"
    tenant_id = data.get_tenant()
    email = data.get_new_email()

    client = IdentityClient()
    assert client is not None

    response = client.start_digital_twin_email_verification(digital_twin_id, tenant_id, email)
    captured = capsys.readouterr()

    assert "StatusCode.INVALID_ARGUMENT" in captured.out
    assert response is None


def test_start_digital_twin_email_verification_wrong_tenant_id(capsys):
    digital_twin_id = "gid:AAAAFf_ZpzyM2UpRuG22DJLLNq0"
    tenant_id = "gid:AAAAAla6PZwUpk6Lizs5Iki3NDE"
    email = data.get_new_email()

    client = IdentityClient()
    assert client is not None

    response = client.start_digital_twin_email_verification(digital_twin_id, tenant_id, email)
    captured = capsys.readouterr()

    assert "StatusCode.INVALID_ARGUMENT" in captured.out
    assert response is None


def test_start_digital_twin_email_verification_nonexisting_twin_id(capsys):
    digital_twin_id = "gid:AAAAAla6PZwUpk6Lizs5Iki3NDE"
    tenant_id = data.get_tenant()
    email = data.get_new_email()

    client = IdentityClient()
    assert client is not None

    response = client.start_digital_twin_email_verification(digital_twin_id, tenant_id, email)
    captured = capsys.readouterr()

    assert "StatusCode.INVALID_ARGUMENT" in captured.out
    assert response is None


def test_start_digital_twin_email_verification_invalid_email_address(capsys):
    digital_twin_id = "gid:AAAAFf_ZpzyM2UpRuG22DJLLNq0"
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
