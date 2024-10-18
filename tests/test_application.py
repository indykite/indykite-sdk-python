import pytest
import time

from indykite_sdk.config import ConfigClient
from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.application import Application
from indykite_sdk.model.create_application import CreateApplication
from indykite_sdk.model.update_application import UpdateApplication
from helpers import data


@pytest.fixture
def client():
    return ConfigClient()


@pytest.fixture
def app_space_id():
    return data.get_app_space_id()


@pytest.fixture
def application_id():
    return data.get_application_id()


def test_read_application_by_id_wrong_id(client, capsys):
    application_id = "aaaaaaaaaaaaaaa"
    response = client.read_application_by_id(application_id)
    captured = capsys.readouterr()
    assert("invalid ReadApplicationRequest.Id: value length must be between 22 and 254 runes, inclusive" in captured.err)


def test_read_application_id_success(client, application_id, capsys):
    application = client.read_application_by_id(application_id)
    captured = capsys.readouterr()

    assert application is not None
    assert "invalid or expired access_token" not in captured.out
    assert isinstance(application, Application)


def test_read_application_by_id_empty(client, application_id):

    def mocked_read_application_by_id(request: pb2.ReadApplicationRequest):
        return None

    client.stub.ReadApplication = mocked_read_application_by_id
    application = client.read_application_by_id(application_id)
    assert application is None


def test_read_application_by_name_wrong_name(client, app_space_id, capsys):
    application_name = "aaaaaaaaaaaaaaa"
    response = client.read_application_by_name(app_space_id, application_name)
    captured = capsys.readouterr()
    assert ("NOT_FOUND" in captured.err)


def test_read_application_by_name_wrong_app_space_id(client, capsys):
    application_name = data.get_application_name()
    app_space_id = "gid:AAAAAlrNh6beFUSNk6tTtka8dwg"
    response = client.read_application_by_name(app_space_id, application_name)
    captured = capsys.readouterr()
    assert("NOT_FOUND" in captured.err)


def test_read_application_by_name_wrong_app_space_size(client, capsys):
    application_name = data.get_application_name()
    app_space_id = "12546"
    response = client.read_application_by_name(app_space_id, application_name)
    captured = capsys.readouterr()
    assert("invalid ReadApplicationRequest.Name" in captured.err)


def test_read_application_name_success(client, app_space_id, capsys):
    application_name = data.get_application_name()
    application = client.read_application_by_name(app_space_id, application_name)
    captured = capsys.readouterr()

    assert application is not None
    assert "invalid or expired access_token" not in captured.out
    assert isinstance(application, Application)


def test_read_application_by_name_empty(client, app_space_id):
    application_name = data.get_application_name()

    def mocked_read_application_by_name(request: pb2.ReadApplicationRequest):
        return None

    client.stub.ReadApplication = mocked_read_application_by_name
    application = client.read_application_by_name(app_space_id, application_name)

    assert application is None


def test_create_application_success(client, app_space_id, capsys):
    right_now = str(int(time.time()))
    application = client.create_application(app_space_id, "automation-"+right_now,
                                         "Automation "+right_now, "description", [])
    captured = capsys.readouterr()
    assert "invalid or expired access_token" not in captured.out
    assert application is not None
    assert isinstance(application, CreateApplication)
    response = client.delete_application(application.id, application.etag, [])
    assert response.bookmark is not None


def test_create_application_empty(client, app_space_id):
    right_now = str(int(time.time()))

    def mocked_create_application(request: pb2.CreateApplicationRequest):
        return None

    client.stub.CreateApplication = mocked_create_application
    application = client.create_application(app_space_id, "automation-"+right_now, "Automation "+right_now, "description", [])
    assert application is None


def test_create_application_already_exists(client, app_space_id, capsys):
    application = client.create_application(app_space_id, "applicationpython", "Application test sdk", "description", [])
    captured = capsys.readouterr()
    assert "config entity with given name already exist" in captured.err


def test_create_application_fail_invalid_app_space_id(client, capsys):
    app_space_id = "gid:AAAAAdM5d45g4j5lIW1Ma1nFAA"
    application = client.create_application(app_space_id, "wonka-bars", "Application test", "description", [])
    captured = capsys.readouterr()
    assert "invalid id value was provided for application_space_id" in captured.err


def test_create_application_name_fail_type_parameter(client, app_space_id, capsys):
    application = client.create_application(app_space_id, ["test"], "test create", "description", [])
    captured = capsys.readouterr()
    assert "bad argument type for built-in operation" in captured.err


def test_update_application_success(client, app_space_id, capsys):
    application_name = data.get_application_name()
    response = client.read_application_by_name(app_space_id, application_name)
    assert response is not None
    application = client.update_application(response.id, response.etag, response.display_name, "description", [])
    captured = capsys.readouterr()
    assert "invalid or expired access_token" not in captured.out
    assert application is not None
    assert isinstance(application, UpdateApplication)


def test_update_application_empty(client, app_space_id):
    application_name = data.get_application_name()
    response = client.read_application_by_name(app_space_id, application_name)
    assert response is not None

    def mocked_update_application(request: pb2.UpdateApplicationRequest):
        return None

    client.stub.UpdateApplication = mocked_update_application
    application = client.update_application(response.id, response.etag, response.display_name, "description", [])
    assert application is None


def test_update_application_fail_invalid_application(client, app_space_id, capsys):
    application_name = data.get_application_name()
    response = client.read_application_by_name(app_space_id, application_name)
    assert response is not None
    application_id = "gid:AAAAAdM5dfh564j5lIW1Ma1nFAA"
    application = client.update_application(application_id, response.etag, response.display_name,"description update", [])
    captured = capsys.readouterr()
    assert "invalid id value was provided for id" in captured.err


def test_update_application_name_fail_type_parameter(client, app_space_id, application_id, capsys):
    application_name = data.get_application_name()
    response = client.read_application_by_name(app_space_id, application_name)
    assert response is not None
    application = client.update_application(application_id, [response.etag], response.display_name, "description", [])
    captured = capsys.readouterr()
    assert "bad argument type for built-in operation" in captured.err


def test_get_application_list_success(client, app_space_id, capsys):
    application_name = data.get_application_name()
    match = []
    match.append(application_name)
    application = client.list_applications(app_space_id, match, [])
    captured = capsys.readouterr()
    assert application is not None
    assert "invalid or expired access_token" not in captured.out


def test_get_application_list_wrong_app_space(client, capsys):
    app_space_id = "gid:AAAAAXX66V2_Jk3kjCCPThMQGaw"
    application_name = data.get_application_name()
    match = []
    match.append(application_name)
    application = client.list_applications(app_space_id, match, [])
    captured = capsys.readouterr()
    assert "invalid id value was provided for app_space_id" in captured.err


def test_get_application_list_wrong_type(client, app_space_id, capsys):
    application_name = data.get_application_name()
    match = "test-create"
    application = client.list_applications(app_space_id, match, [])
    captured = capsys.readouterr()
    assert "value length must be between 2 and 254 runes" in captured.err


def test_get_application_list_wrong_bookmark(client, app_space_id, capsys):
    application_name = data.get_application_name()
    match = []
    match.append(application_name)
    application = client.list_applications(app_space_id, match,
                                       ["RkI6a2N3US9RdnpsOGI4UWlPZU5OIGTHNTUQxcGNvU3NuZmZrQT09-r9S5McchAnB0Gz8oMjg_pWxPPdAZTJpaoNKq6HAAng"])
    captured = capsys.readouterr()
    assert "invalid bookmark value" in captured.err


def test_get_application_list_empty_match(client, app_space_id, capsys):
    match = []
    application = client.list_applications(app_space_id, match, [])
    captured = capsys.readouterr()
    assert "value must contain at least 1 item" in captured.err


def test_get_application_list_no_answer_match(client, app_space_id, capsys):
    application_name = "test-creation"
    match = []
    match.append(application_name)
    application = client.list_applications(app_space_id, match, [])
    captured = capsys.readouterr()
    assert application is not None
    assert application == []


def test_get_application_list_raise_exception(client, app_space_id, capsys):
    match = ""
    application = client.list_applications(app_space_id, match, [])
    captured = capsys.readouterr()
    assert "value must contain at least 1 item" in captured.err


def test_get_application_list_empty(client, app_space_id):
    application_name = data.get_application_name()
    match = []
    match.append(application_name)

    def mocked_get_application_list(request: pb2.ListApplicationsRequest):
        return None

    client.stub.ListApplications = mocked_get_application_list
    application = client.list_applications(app_space_id, match, [])
    assert application is None


def test_del_application_success(client, app_space_id, capsys):
    right_now = str(int(time.time()))
    application = client.create_application(app_space_id, "automation-" + right_now,
                                  "Automation " + right_now, "description", [])
    assert application is not None
    response = client.delete_application(application.id, application.etag, [] )
    captured = capsys.readouterr()
    assert response is not None


def test_del_application_wrong_application_id(client, application_id, capsys):
    response = client.delete_application(application_id, "oeprbUOYHUIYI75U", [] )
    captured = capsys.readouterr()
    assert("invalid eTag value" in captured.err)


def test_del_application_empty(client):
    id = "gid:AAAAAjLRnbbaJE53rrjm_NJXyO"
    etag = "HcQ77D8CUWV"

    def mocked_delete_application(request: pb2.DeleteApplicationRequest):
        return None

    client.stub.DeleteApplication = mocked_delete_application
    response = client.delete_application(id, etag, [])

    assert response is None
