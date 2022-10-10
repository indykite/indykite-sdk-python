import sys
import pytest
import json
from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk import api
from jarvis_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from jarvis_sdk.indykite.config.v1beta1 import model_pb2 as model
from jarvis_sdk.model.service_account import ServiceAccount
from tests.helpers import data


def test_service_account_short_id(capsys):
    client = ConfigClient()
    assert client is not None

    config_id = "AAAAAAAAAA"
    response = client.get_service_account(config_id)
    captured = capsys.readouterr()
    assert "invalid ReadServiceAccountRequest.Id: value length must be between 22 and 254 runes, inclusive" in captured.out
    assert response is None


def test_service_account_wrong_id(capsys):
    client = ConfigClient()
    assert client is not None

    config_id = data.get_wrong_account_id()

    def mocked_service_account(request: pb2.ReadServiceAccountRequest):
        return pb2.ReadServiceAccountResponse()

    client.stub.ServiceAccount = mocked_service_account
    response = client.get_service_account(config_id)
    captured = capsys.readouterr()
    assert "invalid id value was provided for id" in captured.out

    assert response is None


def test_service_account_success_with_param():
    client = ConfigClient()
    assert client is not None

    config_id = data.get_account_id()

    def mocked_service_account(request: pb2.ReadServiceAccountRequest):
        return pb2.ReadServiceAccountResponse()

    client.stub.ServiceAccount = mocked_service_account
    response = client.get_service_account(config_id)

    assert response is not None


