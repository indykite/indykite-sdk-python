from indykite_sdk.identity import IdentityClient
from indykite_sdk.model.digital_twin import DigitalTwin
from helpers import data


def test_forgotten_password_wrong_twin_id(capsys):
    digital_twin_id = "696e6479-6b69-465-8000-010f00000000"
    tenant_id = data.get_tenant()

    client = IdentityClient()
    assert client is not None

    response = client.start_forgotten_password_flow(digital_twin_id, tenant_id)
    captured = capsys.readouterr()

    assert (
        "StatusCode.INVALID_ARGUMENT" in captured.err
    )


def test_forgotten_password_wrong_tenant_id(capsys):
    digital_twin_id = data.get_digital_twin_test()
    tenant_id = "gid:AAAAAbHLUExsxkqsqRoI93amR30"

    client = IdentityClient()
    assert client is not None

    response = client.start_forgotten_password_flow(digital_twin_id, tenant_id)
    captured = capsys.readouterr()

    assert "tenantId is not valid Tenant identifier" in captured.err


def test_forgotten_password_uuid_tenant_id(capsys):
    digital_twin_id = data.get_digital_twin_test()
    tenant_id = "696e6479-6b69-4465-8000-030f00000001"

    client = IdentityClient()
    assert client is not None

    response = client.start_forgotten_password_flow(digital_twin_id, tenant_id)
    captured = capsys.readouterr()

    "invalid DigitalTwin.Id: value length must be 16 bytes" in captured.err


def test_forgotten_password_nonexisting_twin_id(capsys):
    digital_twin_id = "gid:AAAAAbHLUExsxkqsqRoI93amR30"
    tenant_id = data.get_tenant()

    client = IdentityClient()
    assert client is not None

    response = client.start_forgotten_password_flow(digital_twin_id, tenant_id)
    captured = capsys.readouterr()

    assert "StatusCode.INVALID_ARGUMENT" in captured.err


def test_forgotten_password_success(capsys):
    digital_twin_id = data.get_digital_twin_test()
    tenant_id = data.get_tenant()

    client = IdentityClient()
    assert client is not None

    response = client.start_forgotten_password_flow(digital_twin_id, tenant_id)
    captured = capsys.readouterr()

    assert response is True
