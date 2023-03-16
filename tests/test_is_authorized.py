from indykite_sdk.authorization import AuthorizationClient
from indykite_sdk.indykite.authorization.v1beta1 import authorization_service_pb2 as pb2
from indykite_sdk.model.is_authorized import IsAuthorizedResource, IsAuthorizedResponse, IsAuthorizedActions
from indykite_sdk.indykite.identity.v1beta2 import model_pb2 as model
from indykite_sdk.indykite.objects.v1beta1 import struct_pb2 as pb2_struct
from indykite_sdk.indykite.identity.v1beta2 import attributes_pb2 as attributes
from helpers import data


def test_is_authorized_token_wrong_token(capsys):
    client = AuthorizationClient()
    assert client is not None

    access_token = data.get_expired_token()
    resources = [IsAuthorizedResource("resourceID", "LabelName"), IsAuthorizedResource("resource2ID", "LabelName")]
    actions = ["ACTION"]
    response = client.is_authorized_token(access_token, resources, actions)
    captured = capsys.readouterr()
    assert "invalid or expired access_token" in captured.err


def test_is_authorized_token_empty():
    client = AuthorizationClient()
    assert client is not None

    access_token = data.get_verification_bearer()
    resources = [IsAuthorizedResource("resourceID", "LabelName"), IsAuthorizedResource("resource2ID", "LabelName")]
    actions = ["ACTION"]
    res = []
    for r in resources:
        res.append(pb2.IsAuthorizedRequest.Resource(id=r.id, label=r.label))
    digital_twin_identifier = model.DigitalTwinIdentifier(
        access_token=str(access_token)
    )

    def mocked_is_authorized(request: pb2.IsAuthorizedRequest):
        assert request.digital_twin_identifier == digital_twin_identifier
        return None
    client.stub.IsAuthorized = mocked_is_authorized
    response = client.is_authorized_token(access_token, resources, actions)
    assert response is None


def test_is_authorized_dt_wrong_dt(capsys):
    client = AuthorizationClient()
    assert client is not None

    digital_twin_id = data.get_tenant_email()
    tenant_id = data.get_tenant()
    resources = [IsAuthorizedResource("resourceID", "LabelName"), IsAuthorizedResource("resource2ID", "LabelName")]
    actions = ["ACTION"]
    response = client.is_authorized_digital_twin(digital_twin_id, tenant_id, resources, actions)
    captured = capsys.readouterr()
    assert "id is not valid DigitalTwin identifier" in captured.err


def test_is_authorized_dt_wrong_resources(capsys):
    client = AuthorizationClient()
    assert client is not None

    digital_twin_id = data.get_digital_twin()
    tenant_id = data.get_tenant()
    actions = ["ACTION"]
    resources = [{"resourceID", "LabelName"}]
    response = client.is_authorized_digital_twin(digital_twin_id, tenant_id, resources, actions)
    captured = capsys.readouterr()
    assert "'set' object has no attribute 'id'" in captured.err


def test_is_authorized_dt_success():
    client = AuthorizationClient()
    assert client is not None

    digital_twin_id = data.get_digital_twin()
    tenant_id = data.get_tenant()
    resources = [IsAuthorizedResource("resourceID", "LabelName"), IsAuthorizedResource("resource2ID", "LabelName")]
    actions = ["ACTION"]
    digital_twin_identifier = model.DigitalTwinIdentifier(
        digital_twin=model.DigitalTwin(
            id=str(digital_twin_id),
            tenant_id=str(tenant_id)
        )
    )

    response = client.is_authorized_digital_twin(digital_twin_id, tenant_id, resources, actions)
    assert response is not None
    assert isinstance(response, IsAuthorizedResponse)


def test_is_authorized_dt_empty():
    client = AuthorizationClient()
    assert client is not None

    digital_twin_id = data.get_digital_twin()
    tenant_id = data.get_tenant()
    resources = [IsAuthorizedResource("resourceID", "LabelName"), IsAuthorizedResource("resource2ID", "LabelName")]
    actions = ["ACTION"]
    digital_twin_identifier = model.DigitalTwinIdentifier(
        digital_twin=model.DigitalTwin(
            id=str(digital_twin_id),
            tenant_id=str(tenant_id)
        )
    )

    def mocked_is_authorized(request: pb2.IsAuthorizedRequest):
        assert request.digital_twin_identifier == digital_twin_identifier
        return None

    client.stub.IsAuthorized = mocked_is_authorized
    response = client.is_authorized_digital_twin(digital_twin_id, tenant_id, resources, actions)
    assert response is None


def test_is_authorized_property_wrong_property(capsys):
    client = AuthorizationClient()
    assert client is not None

    type_filter = "phone"
    email_value = "sdk@indykite.com"
    resources = [IsAuthorizedResource("resourceID", "LabelName"), IsAuthorizedResource("resource2ID", "LabelName")]
    actions = ["ACTION"]
    response = client.is_authorized_property_filter(type_filter, email_value, resources, actions)
    captured = capsys.readouterr()
    assert "digital_twin was not found" in captured.err


def test_is_authorized_property_wrong_resources(capsys):
    client = AuthorizationClient()
    assert client is not None

    type_filter = "email"
    email_value = "sdk@indykite.com"
    actions = ["ACTION"]
    resources = [{"resourceID", "LabelName"}]
    response = client.is_authorized_property_filter(type_filter, email_value, resources, actions)
    captured = capsys.readouterr()
    assert "'set' object has no attribute 'id'" in captured.err


def test_is_authorized_property_success():
    client = AuthorizationClient()
    assert client is not None

    type_filter = "email"
    email_value = "test2000@example.com"
    resources = [IsAuthorizedResource("resourceID", "LabelName"), IsAuthorizedResource("resource2ID", "LabelName")]
    actions = ["ACTION"]
    digital_twin_identifier = model.DigitalTwinIdentifier(
        property_filter=attributes.PropertyFilter(
            type=str(type_filter),
            value=pb2_struct.Value(string_value=email_value)
        )
    )

    response = client.is_authorized_property_filter(type_filter, email_value, resources, actions)
    assert response is not None
    assert isinstance(response, IsAuthorizedResponse)


def test_is_authorized_property_empty():
    client = AuthorizationClient()
    assert client is not None

    type_filter = "email"
    email_value = "sdk@indykite.com"
    resources = [IsAuthorizedResource("resourceID", "LabelName"), IsAuthorizedResource("resource2ID", "LabelName")]
    actions = ["ACTION"]
    digital_twin_identifier = model.DigitalTwinIdentifier(
        property_filter=attributes.PropertyFilter(
            type=str(type_filter),
            value=pb2_struct.Value(string_value=email_value)
        )
    )

    def mocked_is_authorized(request: pb2.IsAuthorizedRequest):
        assert request.digital_twin_identifier == digital_twin_identifier
        return None

    client.stub.IsAuthorized = mocked_is_authorized
    response = client.is_authorized_property_filter(type_filter, email_value, resources, actions)
    assert response is None
