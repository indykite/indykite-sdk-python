from indykite_sdk.config import ConfigClient
from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.customer import Customer
from indykite_sdk.model.read_customer_config import ReadCustomerConfig
from indykite_sdk.model.update_customer_config import UpdateCustomerConfig
from indykite_sdk.indykite.config.v1beta1.model_pb2 import CustomerConfig
from helpers import data


def test_read_customer_by_id_wrong_id(capsys):
    customer_id = "aaaaaaaaaaaaaaa"

    client = ConfigClient()
    assert client is not None

    response = client.read_customer_by_id(customer_id)
    captured = capsys.readouterr()
    assert("invalid ReadCustomerRequest.Id: value length must be between 22 and 254 runes, inclusive" in captured.err)


def test_read_customer_by_id_mock():
    customer_id = data.get_customer_id()

    client = ConfigClient()
    assert client is not None

    def mocked_read_customer(request: pb2.ReadCustomerRequest):
        test_customer_id = str(customer_id)
        assert test_customer_id == customer_id
        return pb2.ReadCustomerResponse()

    client.stub.ReadCustomer = mocked_read_customer
    customer = client.read_customer_by_id(customer_id)
    assert customer is not None
    assert isinstance(customer, Customer)


def test_read_customer_by_id_wrong_id_mock(capsys):
    customer_id = "gid:AAAAAjUIwqhDT00ikJnfNwyeXF0"

    client = ConfigClient()
    assert client is not None

    def mocked_read_customer(request: pb2.ReadCustomerRequest):
        raise Exception("something went wrong")

    client.stub.ReadCustomer = mocked_read_customer
    customer = client.read_customer_by_id(customer_id)
    captured = capsys.readouterr()
    assert("something went wrong" in captured.err)


def test_read_customer_id_success(capsys):
    client = ConfigClient()
    assert client is not None
    try:
        service_account = client.read_service_account()
    except Exception as exception:
        print(exception)
        return None

    customer = client.read_customer_by_id(service_account.customer_id)

    captured = capsys.readouterr()
    assert "invalid or expired access_token" not in captured.out
    assert customer is not None


def test_read_customer_by_id_empty():
    client = ConfigClient()
    assert client is not None

    try:
        service_account = client.read_service_account()
    except Exception as exception:
        print(exception)
        return None

    def mocked_read_customer_by_id(request: pb2.ReadCustomerRequest):
        return None

    client.stub.ReadCustomer = mocked_read_customer_by_id
    customer = client.read_customer_by_id(service_account.customer_id)

    assert customer is None


def test_read_customer_by_name_wrong_name(capsys):
    customer_name = "aaaaaaaaaaaaaaa"

    client = ConfigClient()
    assert client is not None

    response = client.read_customer_by_name(customer_name)
    captured = capsys.readouterr()
    assert("insufficient permission" in captured.err)


def test_read_customer_name_success(capsys):
    client = ConfigClient()
    assert client is not None

    customer_name = data.get_customer_name()

    customer = client.read_customer_by_name(customer_name)
    captured = capsys.readouterr()

    assert customer is not None
    assert "invalid or expired access_token" not in captured.out
    assert isinstance(customer, Customer)


def test_read_customer_by_name_empty():
    client = ConfigClient()
    assert client is not None

    customer_name = data.get_customer_name()

    def mocked_read_customer_by_name(request: pb2.ReadCustomerRequest):
        return None

    client.stub.ReadCustomer = mocked_read_customer_by_name
    customer = client.read_customer_by_name(customer_name)

    assert customer is None


def test_read_customer_config_wrong_id(capsys):
    customer_id = "aaaaaaaaaaaaaaa"

    client = ConfigClient()
    assert client is not None

    response = client.read_customer_config(customer_id)
    captured = capsys.readouterr()
    assert("invalid ReadCustomerConfigRequest.Id: value length must be between 22 and 254 runes, inclusive" in captured.err)


def test_read_customer_config_mock():
    customer_id = data.get_customer_id()

    client = ConfigClient()
    assert client is not None

    def mocked_read_customer_config(request: pb2.ReadCustomerConfigRequest):
        test_customer_id = str(customer_id)
        assert test_customer_id == customer_id
        return pb2.ReadCustomerConfigResponse()

    client.stub.ReadCustomerConfig = mocked_read_customer_config
    customer_config = client.read_customer_config(customer_id)
    assert customer_config is not None
    assert isinstance(customer_config, ReadCustomerConfig)


def test_read_customer_config_wrong_id_mock(capsys):
    customer_id = "gid:AAAAAjUIwqhDT00ikJnfNwyeXF0"

    client = ConfigClient()
    assert client is not None

    def mocked_read_customer_config(request: pb2.ReadCustomerConfigRequest):
        raise Exception("something went wrong")

    client.stub.ReadCustomerConfig = mocked_read_customer_config
    customer = client.read_customer_config(customer_id)
    captured = capsys.readouterr()
    assert("something went wrong" in captured.err)


def test_read_customer_config_success(capsys):
    client = ConfigClient()
    assert client is not None
    try:
        service_account = client.read_service_account()
    except Exception as exception:
        print(exception)
        return None

    customer_config = client.read_customer_config(service_account.customer_id)

    captured = capsys.readouterr()
    assert "invalid or expired access_token" not in captured.out
    assert customer_config is not None


def test_read_customer_config_empty():
    client = ConfigClient()
    assert client is not None

    try:
        service_account = client.read_service_account()
    except Exception as exception:
        print(exception)
        return None

    def mocked_read_customer_config(request: pb2.ReadCustomerConfigRequest):
        return None

    client.stub.ReadCustomerConfig = mocked_read_customer_config
    customer_config = client.read_customer_config(service_account.customer_id)

    assert customer_config is None


def test_update_customer_config_mock():
    customer_id = data.get_customer_id()
    etag = "Random"
    customer_config = CustomerConfig(
            default_auth_flow_id=None,
            default_email_service_id=None
        )
    bookmarks = []
    client = ConfigClient()
    assert client is not None

    def mocked_update_customer_config(request: pb2.UpdateCustomerConfigRequest):
        test_customer_id = str(customer_id)
        assert test_customer_id == customer_id
        test_etag = str(etag)
        assert test_etag == etag
        test_customer_config = customer_config
        assert test_customer_config == customer_config
        test_bookmarks = bookmarks
        assert test_bookmarks == bookmarks
        return pb2.UpdateCustomerConfigResponse()

    client.stub.UpdateCustomerConfig = mocked_update_customer_config
    update = client.update_customer_config(customer_id, etag, customer_config, bookmarks)
    assert update is not None
    assert isinstance(update, UpdateCustomerConfig)


def test_update_customer_config_wrong_id_mock(capsys):
    customer_id = "gid:AAAAAjUIwqhDT00ikJnfNwyeXF0"
    etag = "Random"
    customer_config = CustomerConfig(
        default_auth_flow_id=None,
        default_email_service_id=None
    )
    bookmarks = []
    client = ConfigClient()
    assert client is not None

    def mocked_update_customer_config(request: pb2.UpdateCustomerConfigRequest):
        raise Exception("something went wrong")

    client.stub.UpdateCustomerConfig = mocked_update_customer_config
    update = client.update_customer_config(customer_id, etag, customer_config, bookmarks)
    captured = capsys.readouterr()
    assert("something went wrong" in captured.err)


def test_update_customer_config_success(capsys):
    client = ConfigClient()
    assert client is not None
    try:
        service_account = client.update_service_account()
    except Exception as exception:
        print(exception)
        return None

    customer = client.read_customer_config(service_account.customer_id)
    customer_config = client.create_customer_config(
        default_auth_flow_id=customer.config.default_auth_flow_id,
        default_email_service_id=None)
    update = client.update_customer_config(customer.customer_id, customer.etag, customer_config,[])
    captured = capsys.readouterr()
    assert "invalid or expired access_token" not in captured.out
    assert isinstance(update, UpdateCustomerConfig)


def test_update_customer_config_empty():
    client = ConfigClient()
    assert client is not None

    try:
        service_account = client.update_service_account()
    except Exception as exception:
        print(exception)
        return None

    etag = "Random"
    customer_config = CustomerConfig(
        default_auth_flow_id=None,
        default_email_service_id=None
    )
    bookmarks = []

    def mocked_update_customer_config(request: pb2.UpdateCustomerConfigRequest):
        return None

    client.stub.UpdateCustomerConfig = mocked_update_customer_config
    update = client.update_customer_config(service_account.customer_id, etag, customer_config, bookmarks)
    assert update is None


def test_create_customer_config():
    client = ConfigClient()
    assert client is not None
    customer_config = client.create_customer_config(
        default_auth_flow_id=None,
        default_email_service_id=None)
    assert isinstance(customer_config, CustomerConfig)


def test_read_customer_name_token_success(capsys):
    client = ConfigClient()
    assert client is not None

    customer_name = data.get_customer_name()
    customer = client.read_customer_by_name(customer_name)
    captured = capsys.readouterr()
    assert customer is not None
    assert "invalid or expired access_token" not in captured.out
    assert isinstance(customer, Customer)
    client_config2 = ConfigClient(False, client.token_source)
    customer2 = client_config2.read_customer_by_name(customer_name)
    assert customer2 is not None
    assert "invalid or expired access_token" not in captured.out
    assert isinstance(customer2, Customer)
