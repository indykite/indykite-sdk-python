import time

from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from jarvis_sdk.model.app_space import ApplicationSpace
from jarvis_sdk.model.create_app_space import CreateApplicationSpace
from jarvis_sdk.model.update_app_space import UpdateApplicationSpace
from tests.helpers import data


def test_get_app_space_by_id_wrong_id(capsys):
    app_space_id = "aaaaaaaaaaaaaaa"

    client = ConfigClient()
    assert client is not None

    response = client.get_app_space_by_id(app_space_id)
    captured = capsys.readouterr()
    print(captured)
    assert("invalid ReadApplicationSpaceRequest.Id: value length must be between 22 and 254 runes, inclusive" in captured.out)
    assert response is None


def test_get_app_space_id_success(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()
    app_space = client.get_app_space_by_id(app_space_id)
    captured = capsys.readouterr()

    assert app_space is not None
    assert "invalid or expired access_token" not in captured.out


def test_get_app_space_by_id_empty():
    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()

    def mocked_get_app_space_by_id(request: pb2.ReadApplicationSpaceRequest):
        return None

    client.stub.ReadApplicationSpace = mocked_get_app_space_by_id
    app_space = client.get_app_space_by_id(app_space_id)

    assert app_space is None


def test_get_app_space_by_name_wrong_name(capsys):
    app_space_name = "aaaaaaaaaaaaaaa"

    client = ConfigClient()
    assert client is not None

    customer_id = data.get_customer_id()

    response = client.get_app_space_by_name(customer_id, app_space_name)
    captured = capsys.readouterr()
    assert response is None


def test_get_app_space_by_name_wrong_customer_id(capsys):
    app_space_name = "do-not-delete"

    client = ConfigClient()
    assert client is not None

    customer_id = "gid:AAAAAmluZHlraURlgAABDwAAAAA"

    response = client.get_app_space_by_name(customer_id, app_space_name)
    captured = capsys.readouterr()
    assert response is None


def test_get_app_space_by_name_wrong_customer_size(capsys):
    app_space_name = data.get_app_space_name()

    client = ConfigClient()
    assert client is not None

    customer_id = "12546"

    response = client.get_app_space_by_name(customer_id, app_space_name)
    captured = capsys.readouterr()
    assert response is None


def test_get_app_space_name_success(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_name = data.get_app_space_name()
    customer_id = data.get_customer_id()

    app_space = client.get_app_space_by_name(customer_id, app_space_name)
    captured = capsys.readouterr()

    assert app_space is not None
    assert "invalid or expired access_token" not in captured.out
    assert isinstance(app_space, ApplicationSpace)


def test_get_app_space_by_name_empty():
    client = ConfigClient()
    assert client is not None

    app_space_name = data.get_app_space_name()
    customer_id = data.get_customer_id()

    def mocked_get_app_space_by_name(request: pb2.ReadApplicationSpaceRequest):
        return None

    client.stub.ReadApplicationSpace = mocked_get_app_space_by_name
    app_space = client.get_app_space_by_name(customer_id, app_space_name)

    assert app_space is None


def test_create_app_space_success(capsys):
    client = ConfigClient()
    assert client is not None

    customer_id = data.get_customer_id()
    right_now = str(int(time.time()))

    app_space = client.create_app_space(customer_id, "automation-"+right_now,"Automation "+right_now, "description", [])
    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert app_space is not None
    assert isinstance(app_space, CreateApplicationSpace)


def test_create_app_space_empty():
    client = ConfigClient()
    assert client is not None

    customer_id = data.get_customer_id()
    right_now = str(int(time.time()))

    def mocked_create_app_space(request: pb2.CreateApplicationSpaceRequest):
        return None

    client.stub.CreateApplicationSpace = mocked_create_app_space
    app_space = client.create_app_space(customer_id, "automation-"+right_now, "Automation "+right_now, "description", [])

    assert app_space is None


def test_create_app_space_already_exists(capsys):
    client = ConfigClient()
    assert client is not None

    customer_id = data.get_customer_id()

    app_space = client.create_app_space(customer_id, "appspacetestsdk", "app space test sdk ", "description", [])
    captured = capsys.readouterr()

    assert "config entity with given name already exist" in captured.out


def test_create_app_space_fail_invalid_customer(capsys):
    client = ConfigClient()
    assert client is not None

    customer_id = "gid:AAAAAdM5d45g4j5lIW1Ma1nFAA"

    app_space = client.create_app_space(customer_id, "appspacetestsdk5", "app space test sdk 5", "description", [])
    captured = capsys.readouterr()

    assert app_space is None
    assert "invalid id value was provided for customer_id" in captured.out


def test_create_app_space_fail_not_allowed_customer(capsys):
    client = ConfigClient()
    assert client is not None

    customer_id = "gid:AAAAAcsuX7kYWE3ioXQHUBbAIu8"

    app_space = client.create_app_space(customer_id, "test-create", "test create", "description", [])
    captured = capsys.readouterr()

    assert app_space is None
    assert "insufficient permission to perform requested action" in captured.out


def test_create_app_space_name_fail_type_parameter(capsys):
    client = ConfigClient()
    assert client is not None

    customer_id = data.get_customer_id()

    app_space = client.create_app_space(customer_id, ["test"], "test create", "description", [])
    captured = capsys.readouterr()

    assert app_space is None
    assert "has type list, but expected one of: bytes, unicode" in captured.out


def test_update_app_space_success(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_name = "appspacetestsdk"
    customer_id = data.get_customer_id()
    response = client.get_app_space_by_name(customer_id, app_space_name)
    assert response is not None

    app_space = client.update_app_space(response.id, response.etag, response.display_name,"description", [])
    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert app_space is not None
    assert isinstance(app_space, UpdateApplicationSpace)


def test_update_app_space_empty():
    client = ConfigClient()
    assert client is not None

    app_space_name = "appspacetestsdk"
    customer_id = data.get_customer_id()
    response = client.get_app_space_by_name(customer_id, app_space_name)
    assert response is not None

    def mocked_update_app_space(request: pb2.UpdateApplicationSpaceRequest):
        return None

    client.stub.UpdateApplicationSpace = mocked_update_app_space
    app_space = client.update_app_space(response.id, response.etag, response.display_name, "description", [])

    assert app_space is None


def test_update_app_space_fail_invalid_app_space(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_name = "appspacetestsdk"
    customer_id = data.get_customer_id()
    response = client.get_app_space_by_name(customer_id, app_space_name)
    assert response is not None
    app_space_id = "gid:AAAAAdM5d45g4j5lIW1Ma1nFAA"

    app_space = client.update_app_space(app_space_id, response.etag, response.display_name,"description update", [])
    captured = capsys.readouterr()

    assert app_space is None
    assert "invalid id value was provided for id" in captured.out


def test_update_app_space_fail_not_allowed_app_space_id(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()
    app_space_name = "appspacetestsdk"
    customer_id = data.get_customer_id()
    response = client.get_app_space_by_name(customer_id, app_space_name)
    assert response is not None
    app_space_id = "gid:AAAAAlrNh6beFUSNk6tTtka8dwg"

    app_space = client.update_app_space(app_space_id, response.etag, response.display_name,"description update", [])
    captured = capsys.readouterr()

    assert app_space is None
    assert "insufficient permission to perform requested action" in captured.out


def test_update_app_space_name_fail_type_parameter(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_name = "appspacetestsdk"
    customer_id = data.get_customer_id()
    response = client.get_app_space_by_name(customer_id, app_space_name)
    assert response is not None

    app_space = client.update_app_space(response.id, [response.etag], response.display_name,"description update", [])
    captured = capsys.readouterr()

    assert app_space is None
    assert "has type list, but expected one of: bytes, unicode" in captured.out


def test_get_app_space_list_success(capsys):
    client = ConfigClient()
    assert client is not None

    customer_id = data.get_customer_id()
    app_space_name = data.get_app_space_name()
    match = []
    match.append(app_space_name)

    app_space = client.list_app_spaces(customer_id, match, [])
    captured = capsys.readouterr()

    assert app_space is not None
    assert "invalid or expired access_token" not in captured.out


def test_get_app_space_list_wrong_customer(capsys):
    client = ConfigClient()
    assert client is not None

    customer_id = "gid:AAAAAjUIwqhDT00ikJnfNwyeXF0"
    app_space_name = data.get_app_space_name()
    match = []
    match.append(app_space_name)

    app_space = client.list_app_spaces(customer_id, match, [])
    captured = capsys.readouterr()

    assert app_space is None
    assert "invalid id value was provided for customer_id" in captured.out


def test_get_app_space_list_wrong_type(capsys):
    client = ConfigClient()
    assert client is not None

    customer_id = data.get_customer_id()
    app_space_name = data.get_app_space_name()
    match = app_space_name

    app_space = client.list_app_spaces(customer_id, match, [])
    captured = capsys.readouterr()

    assert app_space is None
    assert "value length must be between 2 and 254 runes" in captured.out


def test_get_app_space_list_wrong_bookmark(capsys):
    client = ConfigClient()
    assert client is not None

    customer_id = data.get_customer_id()
    app_space_name = data.get_app_space_name()
    match = []
    match.append(app_space_name)

    app_space = client.list_app_spaces(customer_id, match,
                                       ["RkI6a2N3US9RdnpsOGI4UWlPZU5OIGTHNTUQxcGNvU3NuZmZrQT09-r9S5McchAnB0Gz8oMjg_pWxPPdAZTJpaoNKq6HAAng"])
    captured = capsys.readouterr()

    assert app_space is None
    assert "invalid bookmark value" in captured.out


def test_get_app_space_list_empty_match(capsys):
    client = ConfigClient()
    assert client is not None

    customer_id = data.get_customer_id()
    match = []

    app_space = client.list_app_spaces(customer_id, match, [])
    captured = capsys.readouterr()

    assert app_space is None
    assert "value must contain at least 1 item" in captured.out


def test_get_app_space_list_no_answer_match(capsys):
    client = ConfigClient()
    assert client is not None

    customer_id = data.get_customer_id()
    app_space_name = "test-creation"
    match = []
    match.append(app_space_name)

    app_space = client.list_app_spaces(customer_id, match, [])
    captured = capsys.readouterr()

    assert app_space is not None
    assert app_space == []


def test_get_app_space_list_raise_exception(capsys):

    client = ConfigClient()
    assert client is not None

    customer_id = data.get_customer_id()
    match = ""

    app_space = client.list_app_spaces(customer_id, match, [])
    captured = capsys.readouterr()
    assert "value must contain at least 1 item" in captured.out
    assert app_space is None


def test_get_app_space_list_empty():
    client = ConfigClient()
    assert client is not None

    customer_id = data.get_customer_id()
    app_space_name = data.get_app_space_name()
    match = []
    match.append(app_space_name)

    def mocked_get_app_space_list(request: pb2.ListApplicationSpacesRequest):
        return None

    client.stub.ListApplicationSpaces = mocked_get_app_space_list
    app_space = client.list_app_spaces(customer_id, match, [])

    assert app_space is None


def test_del_app_space_success(capsys):
    client = ConfigClient()
    assert client is not None

    customer_id = data.get_customer_id()
    right_now = str(int(time.time()))
    app_space = client.create_app_space(customer_id, "automation-"+right_now,
                                         "Automation "+right_now, "description", [])

    assert app_space is not None

    response = client.delete_app_space(app_space.id, app_space.etag, [] )
    captured = capsys.readouterr()
    assert response is not None


def test_del_app_space_wrong_space_id(capsys):
    client = ConfigClient()
    assert client is not None

    customer_id = data.get_customer_id()
    response = client.delete_app_space(customer_id, "oeprbUOYHUIYI75U", [] )
    captured = capsys.readouterr()
    assert response is None


def test_del_app_space_empty():
    client = ConfigClient()
    assert client is not None

    id = "gid:AAAAAXX66V2_Jk3kjCCPThMQGaw"
    etag = "oeprbUOYHUIYI75U"

    def mocked_delete_app_space(request: pb2.DeleteApplicationSpaceRequest):
        return None

    client.stub.DeleteApplicationSpace = mocked_delete_app_space
    response = client.delete_app_space(id, etag, [])

    assert response is None
