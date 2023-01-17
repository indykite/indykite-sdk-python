from indykite_sdk.authorization import AuthorizationClient
from indykite_sdk.indykite.authorization.v1beta1 import authorization_service_pb2 as pb2
from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2_ident
from indykite_sdk.model.is_authorized import IsAuthorizedResource
from indykite_sdk.indykite.identity.v1beta2 import model_pb2 as model
from indykite_sdk.indykite.objects.v1beta1 import struct_pb2 as pb2_struct
from helpers import data


def test_is_authorized_token_wrong_token():
    client = AuthorizationClient()
    assert client is not None

    access_token = data.get_expired_token()
    actions = ["HAS_FREE_PARKING"]
    resources = [IsAuthorizedResource("lotA", "ParkingLot"), IsAuthorizedResource("lotB", "ParkingLot")]
    response = client.is_authorized_token(access_token, resources, actions)
    assert response is None


def test_is_authorized_token_success():
    client = AuthorizationClient()
    assert client is not None

    access_token = data.get_verification_bearer()
    actions = ["HAS_FREE_PARKING"]
    resources = [IsAuthorizedResource("lotA", "ParkingLot"), IsAuthorizedResource("lotB", "ParkingLot")]
    res = []
    for r in resources:
        res.append(pb2.IsAuthorizedRequest.Resource(id=r.id, label=r.label))
    digital_twin_identifier = pb2_ident.DigitalTwinIdentifier(
        access_token=str(access_token)
    )

    def mocked_is_authorized(request: pb2.IsAuthorizedRequest):
        assert request.digital_twin_identifier == digital_twin_identifier
        return pb2.IsAuthorizedResponse()

    client.stub.IsAuthorized = mocked_is_authorized
    response = client.is_authorized_token(access_token, resources, actions)
    assert response is not None


def test_is_authorized_token_empty():
    client = AuthorizationClient()
    assert client is not None

    access_token = data.get_verification_bearer()
    actions = ["HAS_FREE_PARKING"]
    resources = [IsAuthorizedResource("lotA", "ParkingLot"), IsAuthorizedResource("lotB", "ParkingLot")]
    res = []
    for r in resources:
        res.append(pb2.IsAuthorizedRequest.Resource(id=r.id, label=r.label))
    digital_twin_identifier = pb2_ident.DigitalTwinIdentifier(
        access_token=str(access_token)
    )

    def mocked_is_authorized(request: pb2.IsAuthorizedRequest):
        assert request.digital_twin_identifier == digital_twin_identifier
        return None
    client.stub.IsAuthorized = mocked_is_authorized
    response = client.is_authorized_token(access_token, resources, actions)
    assert response is None


def test_is_authorized_dt_wrong_dt():
    client = AuthorizationClient()
    assert client is not None

    digital_twin_id = data.get_tenant_email()
    tenant_id = data.get_tenant()
    actions = ["HAS_FREE_PARKING"]
    resources = [IsAuthorizedResource("lotA", "ParkingLot"), IsAuthorizedResource("lotB", "ParkingLot")]
    response = client.is_authorized_digital_twin(digital_twin_id, tenant_id, resources, actions)
    assert response is None


def test_is_authorized_dt_wrong_resources():
    client = AuthorizationClient()
    assert client is not None

    digital_twin_id = data.get_digital_twin()
    tenant_id = data.get_tenant()
    actions = ["HAS_FREE_PARKING"]
    resources = [{"lotA", "ParkingLot"}]
    response = client.is_authorized_digital_twin(digital_twin_id, tenant_id, resources, actions)
    assert response is None


def test_is_authorized_dt_success():
    client = AuthorizationClient()
    assert client is not None

    digital_twin_id = data.get_digital_twin()
    tenant_id = data.get_tenant()
    actions = ["HAS_FREE_PARKING"]
    resources = [IsAuthorizedResource("lotA", "ParkingLot"), IsAuthorizedResource("lotB", "ParkingLot")]
    digital_twin_identifier = pb2_ident.DigitalTwinIdentifier(
        digital_twin=model.DigitalTwin(
            id=str(digital_twin_id),
            tenant_id=str(tenant_id)
        )
    )

    def mocked_is_authorized(request: pb2.IsAuthorizedRequest):
        assert request.digital_twin_identifier == digital_twin_identifier
        return pb2.IsAuthorizedResponse()

    client.stub.IsAuthorized = mocked_is_authorized
    response = client.is_authorized_digital_twin(digital_twin_id, tenant_id, resources, actions)
    assert response is not None


def test_is_authorized_dt_empty():
    client = AuthorizationClient()
    assert client is not None

    digital_twin_id = data.get_digital_twin()
    tenant_id = data.get_tenant()
    actions = ["HAS_FREE_PARKING"]
    resources = [IsAuthorizedResource("lotA", "ParkingLot"), IsAuthorizedResource("lotB", "ParkingLot")]
    digital_twin_identifier = pb2_ident.DigitalTwinIdentifier(
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


def test_is_authorized_property_wrong_property():
    client = AuthorizationClient()
    assert client is not None

    type_filter = "email"
    email_value = "sdk@indykite.com"
    tenant_id = data.get_tenant()
    actions = ["HAS_FREE_PARKING"]
    resources = [IsAuthorizedResource("lotA", "ParkingLot"), IsAuthorizedResource("lotB", "ParkingLot")]
    response = client.is_authorized_property_filter(type_filter, email_value, tenant_id, resources, actions)
    assert response is None


def test_is_authorized_property_wrong_resources():
    client = AuthorizationClient()
    assert client is not None

    type_filter = "email"
    email_value = "sdk@indykite.com"
    tenant_id = data.get_tenant()
    actions = ["HAS_FREE_PARKING"]
    resources = [{"lotA", "ParkingLot"}]
    response = client.is_authorized_property_filter(type_filter, email_value, tenant_id, resources, actions)
    assert response is None


def test_is_authorized_property_success():
    client = AuthorizationClient()
    assert client is not None

    type_filter = "email"
    email_value = "sdk@indykite.com"
    tenant_id = data.get_tenant()
    actions = ["HAS_FREE_PARKING"]
    resources = [IsAuthorizedResource("lotA", "ParkingLot"), IsAuthorizedResource("lotB", "ParkingLot")]
    digital_twin_identifier = pb2_ident.DigitalTwinIdentifier(
        property_filter=pb2_ident.PropertyFilter(
            type=str(type_filter),
            value=pb2_struct.Value(string_value=email_value),
            tenant_id=str(tenant_id)
        )
    )

    def mocked_is_authorized(request: pb2.IsAuthorizedRequest):
        assert request.digital_twin_identifier == digital_twin_identifier
        return pb2.IsAuthorizedResponse()

    client.stub.IsAuthorized = mocked_is_authorized
    response = client.is_authorized_property_filter(type_filter, email_value, tenant_id, resources, actions)
    assert response is not None


def test_is_authorized_property_empty():
    client = AuthorizationClient()
    assert client is not None

    type_filter = "email"
    email_value = "sdk@indykite.com"
    tenant_id = data.get_tenant()
    actions = ["HAS_FREE_PARKING"]
    resources = [IsAuthorizedResource("lotA", "ParkingLot"), IsAuthorizedResource("lotB", "ParkingLot")]
    digital_twin_identifier = pb2_ident.DigitalTwinIdentifier(
        property_filter=pb2_ident.PropertyFilter(
            type=str(type_filter),
            value=pb2_struct.Value(string_value=email_value),
            tenant_id=str(tenant_id)
        )
    )

    def mocked_is_authorized(request: pb2.IsAuthorizedRequest):
        assert request.digital_twin_identifier == digital_twin_identifier
        return None

    client.stub.IsAuthorized = mocked_is_authorized
    response = client.is_authorized_property_filter(type_filter, email_value, tenant_id, resources, actions)
    assert response is None
