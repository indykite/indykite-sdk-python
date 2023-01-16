import json
import time
from datetime import datetime

from indykite_sdk.authorization import AuthorizationClient
from indykite_sdk.indykite.authorization.v1beta1 import authorization_service_pb2 as pb2
from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2_ident
from google.protobuf.json_format import MessageToDict
from indykite_sdk.model.is_authorized import IsAuthorizedResource
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
