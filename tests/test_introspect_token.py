import sys
import pytest
import json
from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk import api
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


def test_introspec_token_success(registration):
    token = registration[0]

    client = IdentityClient()
    assert client is not None

    response = client.introspect_token(token)
    assert isinstance(response, TokenInfo)


original_introspect = IdentityClient.introspect_token
app_space_id = uuid4()

def mocked_introspect(this, token):
  assert token == "mocked-token"

  return model.IdentityTokenInfo(
    app_space_id=app_space_id.bytes
  )

@pytest.fixture(name="prepare")
def prepare():
  IdentityClient.introspect_token = original_introspect


def test_introspect_token(prepare, capsys):
  # Prepare
  IdentityClient.introspect_token = mocked_introspect
  sys.argv = ["this_is_skipped", "introspect", "mocked-token"]

  # Act
  api.main()
  captured = capsys.readouterr()
  x = json.loads(captured.out)

  # Assert
  assert x["appSpaceId"] == str(app_space_id)
