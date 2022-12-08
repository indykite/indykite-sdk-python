from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.model.digital_twin import DigitalTwinCore
from jarvis_sdk.indykite.identity.v1beta1 import identity_management_api_pb2 as pb2
from jarvis_sdk.indykite.identity.v1beta1 import model_pb2 as model
from tests.helpers import data
from uuid import UUID, uuid4


def test_del_digital_twin_wrong_twin_id(capsys):
    digital_twin_id = "696e6479-6b69-465-8000-010f00000000"
    tenant_id = data.get_tenant()

    client = IdentityClient()
    assert client is not None

    response = client.del_digital_twin(digital_twin_id, tenant_id)
    captured = capsys.readouterr()

    assert (
        captured.out == "The digital twin id is not in UUID4 format:\nbadly formed hexadecimal UUID string\n"
    )
    assert response is None


def test_del_digital_twin_wrong_tenant_id(capsys):
    digital_twin_id = "696e6479-6b69-4465-8000-010f00000000"
    tenant_id = "696e6479-6b6-4465-8000-010f00000000"

    client = IdentityClient()
    assert client is not None

    response = client.del_digital_twin(digital_twin_id, tenant_id)
    captured = capsys.readouterr()

    assert captured.out == "The tenant id is not in UUID4 format:\nbadly formed hexadecimal UUID string\n"
    assert response is None


def test_del_digital_twin_nonexisting_twin_id(capsys):
    digital_twin_id = "e1e9f07d-fc6e-4629-84d1-8d23836524ba"
    tenant_id = data.get_tenant()

    client = IdentityClient()
    assert client is not None

    response = client.del_digital_twin(digital_twin_id, tenant_id)
    captured = capsys.readouterr()

    assert "digital_twin was not found" in captured.out
    assert response is None


def test_del_digital_twin_success(capsys):
    digital_twin_id = data.get_digital_twin()
    tenant_id = data.get_tenant()

    client = IdentityClient()
    assert client is not None

    def mocked_del_digital_twin(request: pb2.DeleteDigitalTwinRequest):
        digital_twin_bytes_uuid = UUID(digital_twin_id, version=4).bytes
        tenant_bytes_uuid = UUID(tenant_id, version=4).bytes
        assert request.id.digital_twin.id == digital_twin_bytes_uuid
        assert request.id.digital_twin.tenant_id == tenant_bytes_uuid
        return pb2.DeleteDigitalTwinResponse(
            digital_twin=model.DigitalTwin(id=digital_twin_bytes_uuid, tenant_id=tenant_bytes_uuid)
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

    def mocked_del_digital_twin_by_token(request: pb2.DeleteDigitalTwinRequest):
        assert request.id.access_token == token
        return pb2.DeleteDigitalTwinResponse(
            digital_twin=model.DigitalTwin(id=uuid4().bytes, tenant_id=uuid4().bytes)
        )

    client.stub.DeleteDigitalTwin = mocked_del_digital_twin_by_token
    response = client.del_digital_twin_by_token(token)

    assert response is not None
    assert isinstance(response, DigitalTwinCore)
