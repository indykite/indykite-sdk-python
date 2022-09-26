import pytest

from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2


def test_get_customer_by_id_wrong_id(capsys):
    customer_id = "aaaaaaaaaaaaaaa"

    client = IdentityClient()
    assert client is not None

    response = client.get_customer_by_id(customer_id)
    captured = capsys.readouterr()

    assert (
        captured.out == "The customer id is not in UUID4 format:\nbadly formed hexadecimal UUID string\n"
    )
    assert response is None


def test_get_customer_id_success(registration,capsys):
    customer_id = "024d07ca-dde6-40ed-9685-9e610f9de025"
    token = registration[0]

    client = IdentityClient()
    assert client is not None

    response = client.get_customer_by_id(customer_id,token)
    captured = capsys.readouterr()

    response is not None
    assert "invalid or expired access_token" not in captured.out


