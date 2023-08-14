from indykite_sdk.authorization import AuthorizationClient
from indykite_sdk.indykite.authorization.v1beta1 import authorization_service_pb2 as pb2
from indykite_sdk.model.is_authorized import IsAuthorizedResource, IsAuthorizedResponse
from indykite_sdk.indykite.identity.v1beta2 import model_pb2 as model
from indykite_sdk.indykite.objects.v1beta1 import struct_pb2 as pb2_struct
from indykite_sdk.indykite.identity.v1beta2 import attributes_pb2 as attributes
from indykite_sdk.indykite.authorization.v1beta1 import model_pb2 as pb2_model
from helpers import data


def test_is_authorized_token_wrong_token(capsys):
    client = AuthorizationClient()
    assert client is not None

    access_token = data.get_expired_token()
    actions = ["ACTION1", "ACTION2"]
    resources = [IsAuthorizedResource("resourceID", "TypeName", actions),
                 IsAuthorizedResource("resource2ID", "TypeName", actions)]
    input_params = {}
    response = client.is_authorized_token(access_token, resources, input_params, [])
    captured = capsys.readouterr()
    assert "Failed to introspect the token" in captured.err


def test_is_authorized_token_empty():
    client = AuthorizationClient()
    assert client is not None

    access_token = data.get_verification_bearer()
    actions = ["ACTION1", "ACTION2"]
    resources = [IsAuthorizedResource("resourceID", "TypeName", actions),
                 IsAuthorizedResource("resource2ID", "TypeName", actions)]
    input_params = {}
    res = []
    for r in resources:
        res.append(pb2.IsAuthorizedRequest.Resource(id=r.id, type=r.type, actions=r.actions))
    subject = pb2_model.Subject(
        digital_twin_identifier = model.DigitalTwinIdentifier(
            access_token=str(access_token)
        )
    )

    def mocked_is_authorized(request: pb2.IsAuthorizedRequest):
        assert request.subject == subject
        return None
    client.stub.IsAuthorized = mocked_is_authorized
    response = client.is_authorized_token(access_token, resources, input_params, [])
    assert response is None


def test_is_authorized_token_success():
    client = AuthorizationClient()
    assert client is not None

    token = "mocked-token"
    actions = ["ACTION1", "ACTION2"]
    resources = [IsAuthorizedResource("resourceID", "TypeName", actions),
                 IsAuthorizedResource("resource2ID", "TypeName", actions)]
    input_params = {}
    policy_tags = []
    res = []
    for r in resources:
        res.append(pb2.IsAuthorizedRequest.Resource(id=r.id, type=r.type, actions=r.actions))
    subject = pb2_model.Subject(
        digital_twin_identifier = model.DigitalTwinIdentifier(
            access_token=str(token)
        )
    )

    def mocked_is_authorized(request: pb2.IsAuthorizedRequest):
        assert request.subject == subject
        return pb2.IsAuthorizedResponse

    client.stub.IsAuthorized = mocked_is_authorized
    response = client.is_authorized_token(token, resources, input_params, policy_tags)
    assert response is not None


def test_is_authorized_dt_wrong_dt(capsys):
    client = AuthorizationClient()
    assert client is not None

    digital_twin_id = data.get_tenant_email()
    tenant_id = data.get_tenant()
    actions = ["ACTION1", "ACTION2"]
    resources = [IsAuthorizedResource("resourceID", "TypeName", actions),
                 IsAuthorizedResource("resource2ID", "TypeName", actions)]
    input_params = {}
    response = client.is_authorized_digital_twin(digital_twin_id, tenant_id, resources, input_params, [])
    captured = capsys.readouterr()
    assert "id is not valid DigitalTwin identifier" in captured.err


def test_is_authorized_dt_success():
    client = AuthorizationClient()
    assert client is not None

    digital_twin_id = data.get_digital_twin()
    tenant_id = data.get_tenant()
    actions = ["ACTION1", "ACTION2"]
    resources = [IsAuthorizedResource("resourceID", "TypeName", actions), IsAuthorizedResource("resource2ID", "TypeName", actions)]
    input_params = {"age": "21"}
    policy_tags = ["Car", "Rental", "Sharing"]
    response = client.is_authorized_digital_twin(digital_twin_id, tenant_id, resources, input_params, policy_tags)
    assert response is not None
    assert isinstance(response, IsAuthorizedResponse)


def test_is_authorized_dt_empty():
    client = AuthorizationClient()
    assert client is not None

    digital_twin_id = data.get_digital_twin()
    tenant_id = data.get_tenant()
    actions = ["ACTION1", "ACTION2"]
    resources = [IsAuthorizedResource("resourceID", "TypeName", actions), IsAuthorizedResource("resource2ID", "TypeName", actions)]
    input_params = {}
    subject = pb2_model.Subject(
        digital_twin_identifier=model.DigitalTwinIdentifier(
            digital_twin=model.DigitalTwin(
                id=str(digital_twin_id),
                tenant_id=str(tenant_id)
            )
        )
    )

    def mocked_is_authorized(request: pb2.IsAuthorizedRequest):
        assert request.subject == subject
        return None

    client.stub.IsAuthorized = mocked_is_authorized
    response = client.is_authorized_digital_twin(digital_twin_id, tenant_id, resources, input_params, [])
    assert response is None


def test_is_authorized_property_wrong_property(capsys):
    client = AuthorizationClient()
    assert client is not None

    type_filter = "phone"
    email_value = "sdk@indykite.com"
    actions = ["ACTION1", "ACTION2"]
    resources = [IsAuthorizedResource("resourceID", "TypeName", actions), IsAuthorizedResource("resource2ID", "TypeName", actions)]
    input_params = {}
    response = client.is_authorized_property_filter(type_filter, email_value, resources, input_params, [])
    captured = capsys.readouterr()
    assert "Failed to find identity by property" in captured.err


def test_is_authorized_property_success():
    client = AuthorizationClient()
    assert client is not None

    type_filter = "email"
    email_value = "test2000@example.com"
    actions = ["ACTION1", "ACTION2"]
    resources = [IsAuthorizedResource("resourceID", "TypeName", actions),
                 IsAuthorizedResource("resource2ID", "TypeName", actions)]
    input_params = {}
    response = client.is_authorized_property_filter(type_filter, email_value, resources, input_params, [])
    assert response is not None
    assert isinstance(response, IsAuthorizedResponse)


def test_is_authorized_property_empty():
    client = AuthorizationClient()
    assert client is not None

    type_filter = "email"
    email_value = "sdk@indykite.com"
    actions = ["ACTION1", "ACTION2"]
    resources = [IsAuthorizedResource("resourceID", "TypeName", actions),
                 IsAuthorizedResource("resource2ID", "TypeName", actions)]
    input_params = {}
    subject = pb2_model.Subject(
        digital_twin_identifier=model.DigitalTwinIdentifier(
            property_filter=attributes.PropertyFilter(
                type=str(type_filter),
                value=pb2_struct.Value(string_value=email_value)
            )
        )
    )

    def mocked_is_authorized(request: pb2.IsAuthorizedRequest):
        assert request.subject == subject
        return None

    client.stub.IsAuthorized = mocked_is_authorized
    response = client.is_authorized_property_filter(type_filter, email_value, resources, input_params, [])
    assert response is None
