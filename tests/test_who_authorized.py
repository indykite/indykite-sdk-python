import pytest

from indykite_sdk.authorization import AuthorizationClient
from indykite_sdk.indykite.authorization.v1beta1 import authorization_service_pb2 as pb2
from indykite_sdk.model.who_authorized import WhoAuthorizedResource, WhoAuthorizedResponse


@pytest.fixture
def client():
    return AuthorizationClient()


def test_who_authorized_wrong(client, capsys):
    assert client is not None
    actions = [12, 13]
    resources = [
        WhoAuthorizedResource("resourceID", "TypeName", actions),
        WhoAuthorizedResource("resource2ID", "TypeName", actions),
    ]
    input_params = {}
    response = client.who_authorized(resources, input_params, [])
    captured = capsys.readouterr()
    assert "bad argument type for built-in operation" in captured.err


def test_who_authorized_success(client):
    assert client is not None
    actions = ["ACTION1", "ACTION2"]
    resources = [
        WhoAuthorizedResource("resourceID", "TypeName", actions),
        WhoAuthorizedResource("resource2ID", "TypeName", actions),
    ]
    input_params = {"age": "21"}
    policy_tags = ["Car", "Rental", "Sharing"]
    response = client.who_authorized(resources, input_params, policy_tags)
    assert response is not None
    assert isinstance(response, WhoAuthorizedResponse)


def test_who_authorized_empty(client):
    assert client is not None
    actions = ["ACTION1", "ACTION2"]
    resources = [
        WhoAuthorizedResource("resourceID", "TypeName", actions),
        WhoAuthorizedResource("resource2ID", "TypeName", actions),
    ]
    input_params = {}

    def mocked_who_authorized(request: pb2.WhoAuthorizedRequest):
        return None

    client.stub.WhoAuthorized = mocked_who_authorized
    response = client.who_authorized(resources, input_params, [])
    assert response is None
