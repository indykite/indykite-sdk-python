from indykite_sdk.identity import IdentityClient
from indykite_sdk.model.digital_twin import DigitalTwinCore
from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
from indykite_sdk.indykite.identity.v1beta2 import model_pb2 as model
from indykite_sdk.utils.message_to_value import arg_to_value
from indykite_sdk.indykite.identity.v1beta2 import attributes_pb2 as attributes
from helpers import data


def test_del_digital_twin_wrong_twin_id(capsys):
    digital_twin_id = "gid:AAAAAla6PZwUpk6Lizs5Iki3NDE"
    tenant_id = data.get_tenant()

    client = IdentityClient()
    assert client is not None

    response = client.del_digital_twin(digital_twin_id, tenant_id)
    captured = capsys.readouterr()

    assert "StatusCode.INVALID_ARGUMENT" in captured.err


def test_del_digital_twin_wrong_tenant_id(capsys):
    digital_twin_id = "gid:AAAAFf_ZpzyM2UpRuG22DJLLNq0"
    tenant_id = "gid:AAAAAla6PZwUpk6Lizs5Iki3NDE"

    client = IdentityClient()
    assert client is not None

    response = client.del_digital_twin(digital_twin_id, tenant_id)
    captured = capsys.readouterr()

    assert "StatusCode.INVALID_ARGUMENT" in captured.err


def test_del_digital_twin_nonexisting_twin_id(capsys):
    digital_twin_id = "gid:AAAAAla6PZwUpk6Lizs5Iki3NDE"
    tenant_id = data.get_tenant()

    client = IdentityClient()
    assert client is not None

    response = client.del_digital_twin(digital_twin_id, tenant_id)
    captured = capsys.readouterr()

    assert "StatusCode.INVALID_ARGUMENT" in captured.err


def test_del_digital_twin_empty(capsys):
    digital_twin_id = data.get_digital_twin()
    tenant_id = data.get_tenant()

    client = IdentityClient()
    assert client is not None

    def mocked_del_digital_twin(request: pb2.DeleteDigitalTwinRequest):
        return None

    client.stub.DeleteDigitalTwin = mocked_del_digital_twin
    response = client.del_digital_twin(digital_twin_id, tenant_id)
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

    assert "Token must be 32 chars or more" in captured.err


def test_del_digital_twin_by_token_expired_token(capsys):
    token = data.get_expired_token()

    client = IdentityClient()
    assert client is not None

    response = client.del_digital_twin_by_token(token)
    captured = capsys.readouterr()

    assert "invalid or expired access_token" in captured.err


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


def test_del_digital_twin_non_existing_email(capsys):
    digital_twin_email = "nonexistingemail@example.com"
    tenant_id = data.get_tenant()

    client = IdentityClient()
    assert client is not None

    property_filter = client.property_filter("email", digital_twin_email, tenant_id)
    response = client.del_digital_twin_by_property(property_filter)
    captured = capsys.readouterr()
    assert "StatusCode.NOT_FOUND" in captured.err


def test_del_digital_twin_success(capsys):
    digital_twin_email = "gid:AAAAFf_ZpzyM3UpRuG33DJLLNq0"
    digital_twin_id = "existingemail@example.com"
    tenant_id = data.get_tenant()

    client = IdentityClient()
    assert client is not None

    property_filter = client.property_filter("email", digital_twin_email, tenant_id)

    def mocked_del_digital_twin(request: pb2.DeleteDigitalTwinRequest):
        assert request.id.property_filter.type == "email"
        assert request.id.property_filter.value == arg_to_value(digital_twin_email)
        assert request.id.property_filter.tenant_id == tenant_id
        return pb2.DeleteDigitalTwinResponse(
            digital_twin=model.DigitalTwin(id=digital_twin_id, tenant_id=tenant_id)
        )

    client.stub.DeleteDigitalTwin = mocked_del_digital_twin
    response = client.del_digital_twin_by_property(property_filter)

    assert response is not None
    assert isinstance(response, DigitalTwinCore)
