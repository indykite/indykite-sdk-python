from indykite_sdk.identity import IdentityClient
from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
from helpers import data


def test_token_introspect_short_token(capsys):
    token = "invalid_token"

    client = IdentityClient()
    assert client is not None

    response = client.token_introspect(token)
    captured = capsys.readouterr()

    assert response is None


def test_token_introspect_error(registration,capsys):
    token = registration[0]
    client = IdentityClient()
    assert client is not None

    def mocked_token_introspect_error(request: pb2.TokenIntrospectRequest):
        raise Exception("something went wrong")

    client.stub.TokenIntrospect = mocked_token_introspect_error
    response = client.token_introspect(token)
    captured = capsys.readouterr()

    assert "something went wrong" in captured.err


def test_token_introspect_success(registration):
    token = registration[0]
    client = IdentityClient()
    assert client is not None

    def mocked_token_introspect(request: pb2.TokenIntrospectRequest):
        assert request.access_token == token
        return pb2.TokenIntrospectResponse()

    client.stub.TokenIntrospect = mocked_token_introspect
    response = client.token_introspect(token)

    assert response is not None
