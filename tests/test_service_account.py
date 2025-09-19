import time

import pytest
from helpers import data

from indykite_sdk.config import ConfigClient
from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.create_service_account import CreateServiceAccount
from indykite_sdk.model.service_account import ServiceAccount
from indykite_sdk.model.update_service_account import UpdateServiceAccount


@pytest.fixture
def client():
    return ConfigClient()


@pytest.fixture
def config_id():
    return data.get_account_id()


@pytest.fixture
def customer_id():
    return data.get_customer_id()


@pytest.fixture
def service_account_name():
    return data.get_service_account_name()


def test_service_account_short_id(client, capsys):
    assert client is not None
    config_id = "AAAAAAAAAA"
    response = client.read_service_account(config_id)
    captured = capsys.readouterr()
    assert (
        "invalid ReadServiceAccountRequest.Id: value length must be between 22 and 254 runes, inclusive" in captured.err
    )


def test_service_account_wrong_id(client, capsys):
    assert client is not None
    config_id = data.get_wrong_account_id()

    def mocked_service_account(request: pb2.ReadServiceAccountRequest):
        return pb2.ReadServiceAccountResponse()

    client.stub.ServiceAccount = mocked_service_account
    response = client.read_service_account(config_id)
    captured = capsys.readouterr()
    assert "invalid id value was provided for id" in captured.err


def test_service_account_error(client, config_id, capsys):
    assert client is not None

    def mocked_service_account(request: pb2.ReadServiceAccountRequest):
        raise Exception("something went very wrong")

    client.stub.ReadServiceAccount = mocked_service_account
    response = client.read_service_account(config_id)
    captured = capsys.readouterr()
    assert "something went very wrong" in captured.err


def test_service_account_success_credentials(client):
    assert client is not None
    service_account_id = client.credentials.get("serviceAccountId")
    client.stub.ServiceAccount = service_account_id
    response = client.read_service_account()
    assert response is not None
    assert isinstance(response, ServiceAccount)


def test_service_account_error_credentials(client, capsys):
    assert client is not None
    client.credentials = None
    response = client.read_service_account()
    captured = capsys.readouterr()
    assert "Missing service account" in captured.err


def test_service_account_error_credentials_empty(client, capsys):
    assert client is not None
    client.credentials = {}
    response = client.read_service_account()
    captured = capsys.readouterr()
    assert "Missing service account" in captured.err


def test_service_account_success(client):
    assert client is not None
    response = client.read_service_account()
    assert response is not None
    assert isinstance(response, ServiceAccount)


def test_service_account_success_with_param(client, config_id):
    assert client is not None

    def mocked_service_account(request: pb2.ReadServiceAccountRequest):
        return pb2.ReadServiceAccountResponse()

    client.stub.ServiceAccount = mocked_service_account
    response = client.read_service_account(config_id)
    assert response is not None
    assert isinstance(response, ServiceAccount)


def test_service_account_empty(client):
    assert client is not None

    def mocked_read_service_account(request: pb2.ReadServiceAccountRequest):
        return None

    client.stub.ReadServiceAccount = mocked_read_service_account
    response = client.read_service_account()

    assert response is None


def test_read_service_account_by_name_wrong_name(client, customer_id, capsys):
    service_account_name = "aaaaaaaaaaaaaaa"
    response = client.read_service_account_by_name(customer_id, service_account_name)
    captured = capsys.readouterr()
    assert "NOT_FOUND" in captured.err


def test_read_service_account_by_name_wrong_customer_id(client, service_account_name, capsys):
    assert client is not None
    customer_id = "gid:AAAAAlrNh6beFUSNk6tTtka8dwg"
    response = client.read_service_account_by_name(customer_id, service_account_name)
    captured = capsys.readouterr()
    assert "NOT_FOUND" in captured.err


def test_read_service_account_by_name_wrong_customer_size(client, service_account_name, capsys):
    assert client is not None
    customer_id = "12546"
    response = client.read_service_account_by_name(customer_id, service_account_name)
    captured = capsys.readouterr()
    assert "invalid ReadServiceAccountRequest.Name" in captured.err


def test_read_service_account_name_success(client, customer_id, service_account_name, capsys):
    assert client is not None
    service_account = client.read_service_account_by_name(customer_id, service_account_name)
    captured = capsys.readouterr()

    assert service_account is not None
    assert "invalid or expired access_token" not in captured.out
    assert isinstance(service_account, ServiceAccount)


def test_read_service_account_by_name_empty(client, customer_id, service_account_name):
    assert client is not None

    def mocked_read_service_account_by_name(request: pb2.ReadServiceAccountRequest):
        return None

    client.stub.ReadServiceAccount = mocked_read_service_account_by_name
    service_account = client.read_service_account_by_name(customer_id, service_account_name)
    assert service_account is None


def test_create_service_account_success(client, customer_id, capsys):
    assert client is not None
    right_now = str(int(time.time()))
    create_service_account = CreateServiceAccount(
        "gid:AAAAEiuyZi3zVE9hvsu0gSqgi-g",
        time.time(),
        time.time(),
        "HdQo8h8csJ6",
    )

    def mocked_create_service_account(request: pb2.CreateServiceAccountRequest):
        return create_service_account

    client.stub.CreateServiceAccount = mocked_create_service_account
    captured = capsys.readouterr()

    assert create_service_account is not None
    assert isinstance(create_service_account, CreateServiceAccount)


def test_create_service_account_empty(client, customer_id):
    assert client is not None
    right_now = str(int(time.time()))

    def mocked_create_service_account(request: pb2.CreateServiceAccountRequest):
        return None

    client.stub.CreateServiceAccount = mocked_create_service_account
    service_account = client.create_service_account(
        customer_id,
        "automation-" + right_now,
        "Automation " + right_now,
        "description",
        "all_viewer",
    )

    assert service_account is None


def test_create_service_account_already_exists(client, customer_id, capsys):
    assert client is not None
    service_account = client.create_service_account(
        customer_id,
        "sa-to-expire",
        "ServiceAccount test sdk",
        "description",
        "all_viewer",
    )
    captured = capsys.readouterr()
    assert "config entity with given name already exist" in captured.err


def test_create_service_account_fail_invalid_customer_id(client, capsys):
    assert client is not None
    customer_id = "gid:AAAAAdM5d45g4j5lIW1Ma1nFAA"
    service_account = client.create_service_account(
        customer_id,
        "service-account-test",
        "ServiceAccount test",
        "description",
        "all_viewer",
    )
    captured = capsys.readouterr()
    assert "invalid id value was provided for location" in captured.err


def test_create_service_account_fail_invalid_role(client, customer_id, capsys):
    assert client is not None
    service_account = client.create_service_account(
        customer_id,
        "service-account-test",
        "ServiceAccount test",
        "description",
        "viewer",
    )
    captured = capsys.readouterr()
    assert "value must be in list" in captured.err


def test_create_service_account_name_fail_type_parameter(client, customer_id, capsys):
    assert client is not None
    service_account = client.create_service_account(customer_id, ["test"], "test create", "description", "all_viewer")
    captured = capsys.readouterr()
    assert "bad argument type for built-in operation" in captured.err


def test_update_service_account_success(client, customer_id, service_account_name, capsys):
    assert client is not None
    response = client.read_service_account_by_name(customer_id, service_account_name)
    assert response is not None

    service_account = client.update_service_account(response.id, response.etag, response.display_name, "description")
    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert service_account is not None
    assert isinstance(service_account, UpdateServiceAccount)


def test_update_service_account_empty(client, customer_id, service_account_name):
    assert client is not None
    response = client.read_service_account_by_name(customer_id, service_account_name)
    assert response is not None

    def mocked_update_service_account(request: pb2.UpdateServiceAccountRequest):
        return None

    client.stub.UpdateServiceAccount = mocked_update_service_account
    service_account = client.update_service_account(response.id, response.etag, response.display_name, "description")

    assert service_account is None


def test_update_service_account_fail_invalid_service_account(client, customer_id, service_account_name, capsys):
    assert client is not None
    response = client.read_service_account_by_name(customer_id, service_account_name)
    assert response is not None
    service_account_id = "gid:AAAAAdM5dfh564j5lIW1Ma1nFAA"

    service_account = client.update_service_account(
        service_account_id,
        response.etag,
        response.display_name,
        "description update",
    )
    captured = capsys.readouterr()
    assert "invalid id value was provided for id" in captured.err


def test_update_service_account_name_fail_type_parameter(client, customer_id, service_account_name, capsys):
    assert client is not None
    service_account_id = data.get_service_account_id()
    response = client.read_service_account_by_name(customer_id, service_account_name)
    assert response is not None

    service_account = client.update_service_account(
        service_account_id,
        [response.etag],
        response.display_name,
        "description",
    )
    captured = capsys.readouterr()
    assert "bad argument type for built-in operation" in captured.err


def test_del_service_account_success(client, customer_id, capsys):
    assert client is not None
    right_now = str(int(time.time()))
    service_account = client.create_service_account(
        customer_id,
        "automation-" + right_now,
        "Automation " + right_now,
        "description",
        "all_viewer",
    )
    assert service_account is not None

    def mocked_create_service_account(request: pb2.CreateServiceAccountRequest):
        return service_account

    client.stub.CreateServiceAccount = mocked_create_service_account
    captured = capsys.readouterr()
    assert service_account is not None
    assert isinstance(service_account, CreateServiceAccount)

    delete = client.delete_service_account(service_account.id, service_account.etag)

    def mocked_delete_service_account(request: pb2.DeleteServiceAccountRequest):
        return delete

    client.stub.DeleteServiceAccount = mocked_delete_service_account
    assert delete is not None
    assert isinstance(delete, pb2.DeleteServiceAccountResponse)


def test_del_service_account_wrong_service_account_id(client, capsys):
    assert client is not None
    service_account_id = data.get_app_space_id()
    response = client.delete_service_account(service_account_id, "oeprbUOYHUIYI75U")
    captured = capsys.readouterr()
    assert "invalid id value was provided for id" in captured.err


def test_del_service_account_empty(client, capsys):
    assert client is not None
    id = "gid:AAAAAjLRnbbaJE53rrjm_NJXyO"
    etag = "HcQ77D8CUWV"

    def mocked_delete_service_account(request: pb2.DeleteServiceAccountRequest):
        return None

    client.stub.DeleteServiceAccount = mocked_delete_service_account
    response = client.delete_service_account(id, etag)
    captured = capsys.readouterr()
    assert response is None
