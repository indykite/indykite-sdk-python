import pytest
import time

from indykite_sdk.config import ConfigClient
from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.app_space import ApplicationSpace
from indykite_sdk.model.create_app_space import CreateApplicationSpace
from indykite_sdk.model.update_app_space import UpdateApplicationSpace
from helpers import data


@pytest.fixture
def client():
    return ConfigClient()


@pytest.fixture
def app_space_id():
    return data.get_app_space_id()


@pytest.fixture
def customer_id():
    return data.get_customer_id()


def test_read_app_space_by_id_wrong_id(client, capsys):
    app_space_id = "aaaaaaaaaaaaaaa"

    response = client.read_app_space_by_id(app_space_id)
    captured = capsys.readouterr()
    assert("invalid ReadApplicationSpaceRequest.Id: value length must be between 22 and 254 runes, inclusive" in captured.err)


def test_read_app_space_id_success(client, app_space_id, capsys):
    app_space = client.read_app_space_by_id(app_space_id)
    captured = capsys.readouterr()

    assert app_space is not None
    assert "invalid or expired access_token" not in captured.out


def test_read_app_space_by_id_empty(client, app_space_id):

    def mocked_read_app_space_by_id(request: pb2.ReadApplicationSpaceRequest):
        return None

    client.stub.ReadApplicationSpace = mocked_read_app_space_by_id
    app_space = client.read_app_space_by_id(app_space_id)

    assert app_space is None


def test_read_app_space_by_name_wrong_name(client, customer_id, capsys):
    app_space_name = "aaaaaaaaaaaaaaa"

    response = client.read_app_space_by_name(customer_id, app_space_name)
    captured = capsys.readouterr()
    assert ("NOT_FOUND" in captured.err)


def test_read_app_space_by_name_wrong_customer_id(client, capsys):
    app_space_name = "do-not-delete"

    customer_id = "gid:AAAAAmluZHlraURlgAABDwAAAAA"
    response = client.read_app_space_by_name(customer_id, app_space_name)
    captured = capsys.readouterr()
    assert ("invalid id value was provided for name.location" in captured.err)


def test_read_app_space_by_name_wrong_customer_size(client, capsys):
    app_space_name = data.get_app_space_name()
    customer_id = "12546"
    response = client.read_app_space_by_name(customer_id, app_space_name)
    captured = capsys.readouterr()
    assert ("invalid ReadApplicationSpaceRequest.Name" in captured.err)


def test_read_app_space_name_success(client, customer_id, capsys):
    app_space_name = data.get_app_space_name()
    app_space = client.read_app_space_by_name(customer_id, app_space_name)
    captured = capsys.readouterr()

    assert app_space is not None
    assert "invalid or expired access_token" not in captured.out
    assert isinstance(app_space, ApplicationSpace)


def test_read_app_space_by_name_empty(client, customer_id):
    app_space_name = data.get_app_space_name()

    def mocked_read_app_space_by_name(request: pb2.ReadApplicationSpaceRequest):
        return None

    client.stub.ReadApplicationSpace = mocked_read_app_space_by_name
    app_space = client.read_app_space_by_name(customer_id, app_space_name)

    assert app_space is None


def test_create_app_space_success(client, customer_id, capsys):
    right_now = str(int(time.time()))

    app_space = client.create_app_space(customer_id, "automation-"+right_now,"Automation "+right_now, "description")
    captured = capsys.readouterr()
    assert "invalid or expired access_token" not in captured.out
    assert app_space is not None
    assert isinstance(app_space, CreateApplicationSpace)
    response = client.delete_app_space(app_space.id, app_space.etag)
    assert response is not None


def test_create_app_space_empty(client, customer_id):
    right_now = str(int(time.time()))

    def mocked_create_app_space(request: pb2.CreateApplicationSpaceRequest):
        return None

    client.stub.CreateApplicationSpace = mocked_create_app_space
    app_space = client.create_app_space(customer_id, "automation-"+right_now, "Automation "+right_now, "description")

    assert app_space is None


def test_create_app_space_already_exists(client, customer_id, capsys):
    app_space = client.create_app_space(customer_id, "appspacetest", "app space test sdk ", "description")
    captured = capsys.readouterr()
    assert "config entity with given name already exist" in captured.err


def test_create_app_space_fail_invalid_customer(client, capsys):
    customer_id = "gid:AAAAAdM5d45g4j5lIW1Ma1nFAA"
    app_space = client.create_app_space(customer_id, "appspacetestsdk5", "app space test sdk 5", "description")
    captured = capsys.readouterr()
    assert "invalid id value was provided for customer_id" in captured.err


def test_create_app_space_fail_not_allowed_customer(client, capsys):
    customer_id = "gid:AAAAAcsuX7kYWE3ioXQHUBbAIu8"
    app_space = client.create_app_space(customer_id, "test-create", "test create", "description")
    captured = capsys.readouterr()
    assert "insufficient permission to perform requested action" in captured.err


def test_create_app_space_name_fail_type_parameter(client, customer_id, capsys):
    app_space = client.create_app_space(customer_id, ["test"], "test create", "description")
    captured = capsys.readouterr()
    assert "bad argument type for built-in operation" in captured.err


def test_create_app_space_wrong_region(client, customer_id, capsys):
    right_now = str(int(time.time()))
    app_space = client.create_app_space(customer_id,
                                        "automation-"+right_now,
                                        "Automation "+right_now,
                                        "description",
                                        "wrong-region")
    captured = capsys.readouterr()
    assert "value must be in list [europe-west1 us-east1]" in captured.err


def test_update_app_space_success(client, customer_id, capsys):
    app_space_name = "appspacetest"
    response = client.read_app_space_by_name(customer_id, app_space_name)
    assert response is not None

    app_space = client.update_app_space(response.id, response.etag, response.display_name,"description")
    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert app_space is not None
    assert isinstance(app_space, UpdateApplicationSpace)


def test_update_app_space_empty(client, customer_id):
    app_space_name = "appspacetest"
    response = client.read_app_space_by_name(customer_id, app_space_name)
    assert response is not None

    def mocked_update_app_space(request: pb2.UpdateApplicationSpaceRequest):
        return None

    client.stub.UpdateApplicationSpace = mocked_update_app_space
    app_space = client.update_app_space(response.id, response.etag, response.display_name, "description")

    assert app_space is None


def test_update_app_space_fail_invalid_app_space(client, customer_id, capsys):
    app_space_name = "appspacetest"
    response = client.read_app_space_by_name(customer_id, app_space_name)
    assert response is not None
    app_space_id = "gid:AAAAAdM5d45g4j5lIW1Ma1nFAA"

    app_space = client.update_app_space(app_space_id, response.etag, response.display_name,"description update")
    captured = capsys.readouterr()
    assert "invalid id value was provided for id" in captured.err


def test_update_app_space_fail_not_allowed_app_space_id(client, customer_id, capsys):
    app_space_name = "appspacetest"
    response = client.read_app_space_by_name(customer_id, app_space_name)
    assert response is not None
    app_space_id = "gid:AAAAAlrNh6beFUSNk6tTtka8dwg"

    app_space = client.update_app_space(app_space_id, response.etag, response.display_name,"description update")
    captured = capsys.readouterr()
    assert "NOT_FOUND" in captured.err


def test_update_app_space_name_fail_type_parameter(client, customer_id, capsys):
    app_space_name = "appspacetest"
    response = client.read_app_space_by_name(customer_id, app_space_name)
    assert response is not None

    app_space = client.update_app_space(response.id, [response.etag], response.display_name,"description update")
    captured = capsys.readouterr()
    assert "bad argument type for built-in operation" in captured.err


def test_read_app_space_list_success(client, customer_id, capsys):
    app_space_name = data.get_app_space_name()
    match = [app_space_name]

    app_space = client.list_app_spaces(customer_id, match)
    captured = capsys.readouterr()

    assert app_space is not None
    assert "invalid or expired access_token" not in captured.out


def test_get_app_space_list_wrong_customer(client, capsys):
    customer_id = "gid:AAAAAjUIwqhDT00ikJnfNwyeXF0"
    app_space_name = data.get_app_space_name()
    match = [app_space_name]
    app_space = client.list_app_spaces(customer_id, match)
    captured = capsys.readouterr()
    assert "invalid id value was provided for customer_id" in captured.err


def test_get_app_space_list_wrong_type(client, customer_id, capsys):
    app_space_name = data.get_app_space_name()
    match = app_space_name

    app_space = client.list_app_spaces(customer_id, match)
    captured = capsys.readouterr()
    assert "value length must be between 2 and 254 runes" in captured.err


def test_get_app_space_list_empty_match(client, customer_id, capsys):
    match = []
    app_space = client.list_app_spaces(customer_id, match)
    captured = capsys.readouterr()
    assert "value must contain at least 1 item" in captured.err


def test_get_app_space_list_raise_exception(client, customer_id, capsys):
    match = ""
    app_space = client.list_app_spaces(customer_id, match)
    captured = capsys.readouterr()
    assert "value must contain at least 1 item" in captured.err


def test_get_app_space_list_empty(client, customer_id):
    app_space_name = data.get_app_space_name()
    match = []
    match.append(app_space_name)

    def mocked_get_app_space_list(request: pb2.ListApplicationSpacesRequest):
        return None

    client.stub.ListApplicationSpaces = mocked_get_app_space_list
    app_space = client.list_app_spaces(customer_id, match)

    assert app_space is None


def test_del_app_space_success(client, customer_id, capsys):
    right_now = str(int(time.time()))
    app_space = client.create_app_space(customer_id, "automation-"+right_now,
                                         "Automation "+right_now, "description")
    assert app_space is not None
    response = client.delete_app_space(app_space.id, app_space.etag)
    captured = capsys.readouterr()
    assert response is not None


def test_del_app_space_wrong_space_id(client, customer_id, capsys):
    response = client.delete_app_space(customer_id, "oeprbUOYHUIYI75U")
    captured = capsys.readouterr()
    assert "invalid id value was provided for id" in captured.err


def test_del_app_space_empty(client):
    id = "gid:AAAAAXX66V2_Jk3kjCCPThMQGaw"
    etag = "oeprbUOYHUIYI75U"

    def mocked_delete_app_space(request: pb2.DeleteApplicationSpaceRequest):
        return None

    client.stub.DeleteApplicationSpace = mocked_delete_app_space
    response = client.delete_app_space(id, etag)
    assert response is None
