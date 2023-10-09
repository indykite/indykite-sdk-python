from indykite_sdk.identity import IdentityClient
from helpers import data


def test_verify_digital_twin_email_short_token(capsys):
    token = "short_token"

    client = IdentityClient()
    assert client is not None

    response = client.verify_digital_twin_email(token)
    captured = capsys.readouterr()
    assert "Token must be 32 chars or more" in captured.err


def test_start_digital_twin_email_verification_wrong_twin_id(capsys):
    digital_twin_id = "gid:AAAAAla6PZwUpk6Lizs5Iki3NDE"
    tenant_id = data.get_tenant()
    email = data.get_new_email()

    client = IdentityClient()
    assert client is not None

    response = client.start_digital_twin_email_verification(digital_twin_id, tenant_id, email)
    captured = capsys.readouterr()

    assert "StatusCode.INVALID_ARGUMENT" in captured.err


def test_start_digital_twin_email_verification_wrong_tenant_id(capsys):
    digital_twin_id = "gid:AAAAFf_ZpzyM2UpRuG22DJLLNq0"
    tenant_id = "gid:AAAAAla6PZwUpk6Lizs5Iki3NDE"
    email = data.get_new_email()

    client = IdentityClient()
    assert client is not None

    response = client.start_digital_twin_email_verification(digital_twin_id, tenant_id, email)
    captured = capsys.readouterr()

    assert "StatusCode.INVALID_ARGUMENT" in captured.err


def test_start_digital_twin_email_verification_nonexisting_twin_id(capsys):
    digital_twin_id = "gid:AAAAAla6PZwUpk6Lizs5Iki3NDE"
    tenant_id = data.get_tenant()
    email = data.get_new_email()

    client = IdentityClient()
    assert client is not None

    response = client.start_digital_twin_email_verification(digital_twin_id, tenant_id, email)
    captured = capsys.readouterr()

    assert "StatusCode.INVALID_ARGUMENT" in captured.err


def test_start_digital_twin_email_verification_email_not_found(capsys):
    digital_twin_id = data.get_digital_twin()
    tenant_id = data.get_tenant()
    email = data.get_new_email()

    client = IdentityClient()
    assert client is not None

    response = client.start_digital_twin_email_verification(digital_twin_id, tenant_id, email)
    captured = capsys.readouterr()

    assert "email address is not found" or "digital_twin was not found" in captured.err
