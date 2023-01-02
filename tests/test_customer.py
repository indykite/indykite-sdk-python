from indykite_sdk.config import ConfigClient
from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.customer import Customer
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


def test_get_customer_by_id_mock():
    customer_id = data.get_customer_id()

    client = ConfigClient()
    assert client is not None

    def mocked_read_customer(request: pb2.ReadCustomerRequest):
        test_customer_id = str(customer_id)
        assert test_customer_id == customer_id
        return pb2.ReadCustomerResponse()

    client.stub.ReadCustomer = mocked_read_customer
    customer = client.get_customer_by_id(customer_id)
    assert customer is not None
    assert isinstance(customer, Customer)


def test_get_customer_by_id_wrong_id_mock():
    customer_id = "gid:AAAAAjUIwqhDT00ikJnfNwyeXF0"

    client = ConfigClient()
    assert client is not None

    def mocked_read_customer(request: pb2.ReadCustomerRequest):
        raise Exception("something went wrong")

    client.stub.ReadCustomer = mocked_read_customer
    customer = client.get_customer_by_id(customer_id)
    assert customer is None


def test_get_customer_id_success(capsys):
    client = ConfigClient()
    assert client is not None
    try:
        service_account = client.get_service_account()
    except Exception as exception:
        print(exception)
        return None

    customer = client.get_customer_by_id(service_account.customer_id)

    captured = capsys.readouterr()
    assert "invalid or expired access_token" not in captured.out
    assert customer is not None


def test_get_customer_by_id_empty():
    client = ConfigClient()
    assert client is not None

    try:
        service_account = client.get_service_account()
    except Exception as exception:
        print(exception)
        return None

    def mocked_get_customer_by_id(request: pb2.ReadCustomerRequest):
        return None

    client.stub.ReadCustomer = mocked_get_customer_by_id
    customer = client.get_customer_by_id(service_account.customer_id)

    assert customer is None


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
    assert isinstance(customer, Customer)


def test_get_customer_by_name_empty():
    client = ConfigClient()
    assert client is not None

    customer_name = data.get_customer_name()

    def mocked_get_customer_by_name(request: pb2.ReadCustomerRequest):
        return None

    client.stub.ReadCustomer = mocked_get_customer_by_name
    customer = client.get_customer_by_name(customer_name)

    assert customer is None

