from indykite_sdk.identity import IdentityClient
from indykite_sdk.model.digital_twin import DigitalTwin
from helpers import data


def test_get_digital_twin_wrong_twin_id(capsys):
    digital_twin_id = "696e6479-6b69-465-8000-010f00000000"
    tenant_id = data.get_tenant()

    client = IdentityClient()
    assert client is not None

    response = client.get_digital_twin(digital_twin_id, tenant_id, [])
    captured = capsys.readouterr()

    assert (
        "StatusCode.INVALID_ARGUMENT" in captured.out
    )
    assert response is None


def test_get_digital_twin_wrong_tenant_id(capsys):
    digital_twin_id = "gid:AAAAFf_ZpzyM2UpRuG22DJLLNq0"
    tenant_id = "gid:AAAAAbHLUExsxkqsqRoI93amR30"

    client = IdentityClient()
    assert client is not None

    response = client.get_digital_twin(digital_twin_id, tenant_id, [])
    captured = capsys.readouterr()

    assert "tenantId is not valid Tenant identifier" in captured.out
    assert response is None


def test_get_digital_twin_uuid_tenant_id(capsys):
    digital_twin_id = "gid:AAAAFf_ZpzyM2UpRuG22DJLLNq0"
    tenant_id = "696e6479-6b69-4465-8000-030f00000001"

    client = IdentityClient()
    assert client is not None

    response = client.get_digital_twin(digital_twin_id, tenant_id, [])
    captured = capsys.readouterr()

    "invalid DigitalTwin.Id: value length must be 16 bytes" in captured.out
    assert response is None


def test_get_digital_twin_nonexisting_twin_id(capsys):
    digital_twin_id = "gid:AAAAAbHLUExsxkqsqRoI93amR30"
    tenant_id = data.get_tenant()

    client = IdentityClient()
    assert client is not None

    response = client.get_digital_twin(digital_twin_id, tenant_id, [])
    captured = capsys.readouterr()

    assert "StatusCode.INVALID_ARGUMENT" in captured.out
    assert response is None


def test_get_digital_twin_unknown_property(capsys):
    digital_twin_id = "gid:AAAAFf_ZpzyM2UpRuG22DJLLNq0"
    tenant_id = "gid:AAAAA2CHw7x3Dk68uWSkjl7FoG0"

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

    response = client.get_digital_twin("gid:AAAAFf_ZpzyM2UpRuG22DJLLNq0", "gid:AAAAA2CHw7x3Dk68uWSkjl7FoG0", [])
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

    assert response is None
