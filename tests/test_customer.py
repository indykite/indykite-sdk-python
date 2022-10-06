import pytest
import sys

from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from jarvis_sdk.model.customer import Customer
from tests.helpers import data


def test_get_customer_by_id_wrong_id(capsys):
    customer_id = "aaaaaaaaaaaaaaa"

    client = ConfigClient()
    assert client is not None

    response = client.get_customer_by_id(customer_id)
    captured = capsys.readouterr()
    print(captured)
    assert("invalid ReadCustomerRequest.Id: value length must be between 22 and 254 runes, inclusive" in captured.out)
    assert response is None


def test_get_customer_id_success(capsys):
    client = ConfigClient()
    assert client is not None

    try:
        service_account = client.get_service_account()
    except Exception as exception:
        return None

    assert service_account is not None
    customer = client.get_customer_by_id(service_account.customer_id)
    captured = capsys.readouterr()

    # assert customer is not None
    assert "invalid or expired access_token" not in captured.out


def test_get_customer_by_name_wrong_name(capsys):
    customer_name = "aaaaaaaaaaaaaaa"

    client = ConfigClient()
    assert client is not None

    response = client.get_customer_by_name(customer_name)
    captured = capsys.readouterr()
    assert("insufficient permission" in captured.out)
    assert response is None


def test_get_customer_name_success(capsys):
    client = ConfigClient()
    assert client is not None

    customer_name = data.get_customer_name()

    customer = client.get_customer_by_name(customer_name)
    captured = capsys.readouterr()

    assert customer is not None
    assert "invalid or expired access_token" not in captured.out
    # assert isinstance(customer, Customer)
