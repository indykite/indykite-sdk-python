import sys
import pytest
import json
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk import api
from jarvis_sdk.indykite.identity.v1beta1 import identity_management_api_pb2 as pb2
from jarvis_sdk.indykite.identity.v1beta1 import model_pb2 as model
from jarvis_sdk.model.token_info import TokenInfo
from tests.helpers import data
from uuid import UUID, uuid4


def test_introspect_token_short_token(capsys):
    token = "invalid_token"

    client = IdentityClient()
    assert client is not None

    response = client.introspect_token(token)
    captured = capsys.readouterr()

    assert response is None


def test_introspect_token_error(registration):
    token = registration[0]
    client = IdentityClient()
    assert client is not None

    def mocked_introspect_token_error(request: pb2.TokenIntrospectRequest):
        raise Exception("something went wrong")

    client.stub.TokenIntrospect = mocked_introspect_token_error
    response = client.introspect_token(token)

    response is None


def test_introspec_token_success(registration):
    token = registration[0]
    client = IdentityClient()
    assert client is not None

    def mocked_introspect_token(request: pb2.TokenIntrospectRequest):
        assert request.access_token == token
        return pb2.TokenIntrospectResponse()

    client.stub.TokenIntrospect = mocked_introspect_token
    response = client.introspect_token(token)

    response is not None
