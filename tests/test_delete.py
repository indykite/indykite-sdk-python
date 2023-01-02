from indykite_sdk.identity import IdentityClient
from indykite_sdk.model.digital_twin import DigitalTwinCore
from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
from indykite_sdk.indykite.identity.v1beta2 import model_pb2 as model
from tests.helpers import data


def test_del_digital_twin_wrong_twin_id(capsys):
    digital_twin_id = "gid:AAAAAla6PZwUpk6Lizs5Iki3NDE"
    tenant_id = data.get_tenant()

    client = IdentityClient()
    assert client is not None

    response = client.del_digital_twin(digital_twin_id, tenant_id)
    captured = capsys.readouterr()

    assert "StatusCode.INVALID_ARGUMENT" in captured.out
    assert response is None


def test_del_digital_twin_wrong_tenant_id(capsys):
    digital_twin_id = "gid:AAAAFf_ZpzyM2UpRuG22DJLLNq0"
    tenant_id = "gid:AAAAAla6PZwUpk6Lizs5Iki3NDE"

    client = IdentityClient()
    assert client is not None

    response = client.del_digital_twin(digital_twin_id, tenant_id)
    captured = capsys.readouterr()

    assert "StatusCode.INVALID_ARGUMENT" in captured.out
    assert response is None


def test_del_digital_twin_nonexisting_twin_id(capsys):
    digital_twin_id = "gid:AAAAAla6PZwUpk6Lizs5Iki3NDE"
    tenant_id = data.get_tenant()

    client = IdentityClient()
    assert client is not None

    response = client.del_digital_twin(digital_twin_id, tenant_id)
    captured = capsys.readouterr()

    assert "StatusCode.INVALID_ARGUMENT" in captured.out
    assert response is None


def test_del_digital_twin_success(capsys):
    digital_twin_id = data.get_digital_twin()
    tenant_id = data.get_tenant()

    client = IdentityClient()
    assert client is not None

    def mocked_del_digital_twin(request: pb2.DeleteDigitalTwinRequest):
        assert request.id.digital_twin.id == digital_twin_id
        assert request.id.digital_twin.tenant_id == tenant_id
        return pb2.DeleteDigitalTwinResponse(
            digital_twin=model.DigitalTwin(id=digital_twin_id, tenant_id=tenant_id)
        )

    client.stub.DeleteDigitalTwin = mocked_del_digital_twin
    response = client.del_digital_twin(digital_twin_id, tenant_id)

    assert response is not None
    assert isinstance(response, DigitalTwinCore)


def test_del_digital_twin_by_token_short_token(capsys):
    token = "short_token"
    password = data.get_new_password()

    client = IdentityClient()
    assert client is not None

    response = client.del_digital_twin_by_token(token)
    captured = capsys.readouterr()

    assert captured.out == "Token must be 32 chars or more.\n"
    assert response is None


def test_del_digital_twin_by_token_expired_token(capsys):
    token = data.get_expired_token()

    client = IdentityClient()
    assert client is not None

    response = client.del_digital_twin_by_token(token)
    captured = capsys.readouterr()

    assert "invalid or expired access_token" in captured.out
    assert response is None


def test_del_digital_twin_by_token_success(registration):
    token = registration[0]

    client = IdentityClient()
    assert client is not None

    digital_twin_id = data.get_digital_twin()
    tenant_id = data.get_tenant()

    def mocked_del_digital_twin_by_token(request: pb2.DeleteDigitalTwinRequest):
        assert request.id.access_token == token
        return pb2.DeleteDigitalTwinResponse(
            digital_twin=model.DigitalTwin(id=digital_twin_id, tenant_id=tenant_id)
        )

    client.stub.DeleteDigitalTwin = mocked_del_digital_twin_by_token
    response = client.del_digital_twin_by_token(token)

    assert response is not None
    assert isinstance(response, DigitalTwinCore)
