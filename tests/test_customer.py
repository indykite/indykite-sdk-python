import pytest
from helpers import data

from indykite_sdk.config import ConfigClient
from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.customer import Customer


@pytest.fixture
def client():
    return ConfigClient()


@pytest.fixture
def customer_name():
    return data.get_customer_name()


def test_read_customer_by_id_wrong_id(client, capsys):
    customer_id = "aaaaaaaaaaaaaaa"
    response = client.read_customer_by_id(customer_id)
    captured = capsys.readouterr()
    assert "invalid ReadCustomerRequest.Id: value length must be between 22 and 254 runes, inclusive" in captured.err


def test_read_customer_by_id_mock(client):
    customer_id = data.get_customer_id()

    def mocked_read_customer(request: pb2.ReadCustomerRequest):
        test_customer_id = str(customer_id)
        assert test_customer_id == customer_id
        return pb2.ReadCustomerResponse()

    client.stub.ReadCustomer = mocked_read_customer
    customer = client.read_customer_by_id(customer_id)
    assert customer is not None
    assert isinstance(customer, Customer)


def test_read_customer_by_id_wrong_id_mock(client, capsys):
    customer_id = "gid:AAAAAjUIwqhDT00ikJnfNwyeXF0"

    def mocked_read_customer(request: pb2.ReadCustomerRequest):
        raise Exception("something went wrong")

    client.stub.ReadCustomer = mocked_read_customer
    customer = client.read_customer_by_id(customer_id)
    captured = capsys.readouterr()
    assert "something went wrong" in captured.err


def test_read_customer_id_success(client, capsys):
    try:
        service_account = client.read_service_account()
    except Exception as exception:
        print(exception)
        return

    customer = client.read_customer_by_id(service_account.customer_id)
    captured = capsys.readouterr()
    assert "invalid or expired access_token" not in captured.out
    assert customer is not None


def test_read_customer_by_id_empty(client):
    try:
        service_account = client.read_service_account()
    except Exception as exception:
        print(exception)
        return

    def mocked_read_customer_by_id(request: pb2.ReadCustomerRequest):
        return None

    client.stub.ReadCustomer = mocked_read_customer_by_id
    customer = client.read_customer_by_id(service_account.customer_id)

    assert customer is None


def test_read_customer_by_name_wrong_name(client, capsys):
    customer_name = "aaaaaaaaaaaaaaa"
    response = client.read_customer_by_name(customer_name)
    captured = capsys.readouterr()
    assert "StatusCode.NOT_FOUND" in captured.err


def test_read_customer_name_success(client, customer_name, capsys):
    customer = client.read_customer_by_name(customer_name)
    captured = capsys.readouterr()
    assert customer is not None
    assert "invalid or expired access_token" not in captured.out
    assert isinstance(customer, Customer)


def test_read_customer_by_name_empty(client, customer_name):
    def mocked_read_customer_by_name(request: pb2.ReadCustomerRequest):
        return None

    client.stub.ReadCustomer = mocked_read_customer_by_name
    customer = client.read_customer_by_name(customer_name)
    assert customer is None


def test_read_customer_name_token_success(client, customer_name, capsys):
    customer = client.read_customer_by_name(customer_name)
    captured = capsys.readouterr()
    assert customer is not None
    assert "invalid or expired access_token" not in captured.out
    assert isinstance(customer, Customer)
    client_config2 = ConfigClient(client.token_source)
    customer2 = client_config2.read_customer_by_name(customer_name)
    assert customer2 is not None
    assert "invalid or expired access_token" not in captured.out
    assert isinstance(customer2, Customer)
