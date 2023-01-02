import time

from indykite_sdk.config import ConfigClient
from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.application import Application
from indykite_sdk.model.create_application import CreateApplication
from indykite_sdk.model.update_application import UpdateApplication
from tests.helpers import data


def test_get_application_by_id_wrong_id(capsys):
    application_id = "aaaaaaaaaaaaaaa"

    client = ConfigClient()
    assert client is not None

    response = client.get_application_by_id(application_id)
    captured = capsys.readouterr()
    print(captured)
    assert("invalid ReadApplicationRequest.Id: value length must be between 22 and 254 runes, inclusive" in captured.out)
    assert response is None


def test_get_application_id_success(capsys):
    client = ConfigClient()
    assert client is not None

    application_id = data.get_application_id()
    application = client.get_application_by_id(application_id)
    captured = capsys.readouterr()

    assert application is not None
    assert "invalid or expired access_token" not in captured.out


def test_get_application_by_id_empty():
    client = ConfigClient()
    assert client is not None

    application_id = data.get_application_id()

    def mocked_get_application_by_id(request: pb2.ReadApplicationRequest):
        return None

    client.stub.ReadApplication = mocked_get_application_by_id
    application = client.get_application_by_id(application_id)

    assert application is None


def test_get_application_by_name_wrong_name(capsys):
    application_name = "aaaaaaaaaaaaaaa"

    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()

    response = client.get_application_by_name(app_space_id, application_name)
    captured = capsys.readouterr()
    assert response is None


def test_get_application_by_name_wrong_app_space_id(capsys):
    application_name = data.get_application_name()

    client = ConfigClient()
    assert client is not None

    app_space_id = "gid:AAAAAlrNh6beFUSNk6tTtka8dwg"

    response = client.get_application_by_name(app_space_id, application_name)
    captured = capsys.readouterr()
    assert response is None


def test_get_application_by_name_wrong_app_space_size(capsys):
    application_name = data.get_application_name()

    client = ConfigClient()
    assert client is not None

    app_space_id = "12546"

    response = client.get_application_by_name(app_space_id, application_name)
    captured = capsys.readouterr()
    assert response is None


def test_get_application_name_success(capsys):
    client = ConfigClient()
    assert client is not None

    application_name = data.get_application_name()
    app_space_id = data.get_app_space_id()

    application = client.get_application_by_name(app_space_id, application_name)
    captured = capsys.readouterr()

    assert application is not None
    assert "invalid or expired access_token" not in captured.out
    assert isinstance(application, Application)


def test_get_application_by_name_empty():
    client = ConfigClient()
    assert client is not None

    application_name = data.get_application_name()
    app_space_id = data.get_app_space_id()

    def mocked_get_application_by_name(request: pb2.ReadApplicationRequest):
        return None

    client.stub.ReadApplication = mocked_get_application_by_name
    application = client.get_application_by_name(app_space_id, application_name)

    assert application is None


def test_create_application_success(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()
    right_now = str(int(time.time()))

    application = client.create_application(app_space_id, "automation-"+right_now,
                                         "Automation "+right_now, "description", [])
    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert application is not None
    assert isinstance(application, CreateApplication)


def test_create_application_empty():
    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()
    right_now = str(int(time.time()))

    def mocked_create_application(request: pb2.CreateApplicationRequest):
        return None

    client.stub.CreateApplication = mocked_create_application
    application = client.create_application(app_space_id, "automation-"+right_now, "Automation "+right_now, "description", [])

    assert application is None


def test_create_application_already_exists(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()

    application = client.create_application(app_space_id, "wonka-bars", "Application test sdk", "description", [])
    captured = capsys.readouterr()

    assert "config entity with given name already exist" in captured.out


def test_create_application_fail_invalid_app_space_id(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_id = "gid:AAAAAdM5d45g4j5lIW1Ma1nFAA"

    application = client.create_application(app_space_id, "wonka-bars", "Application test", "description", [])
    captured = capsys.readouterr()

    assert application is None
    assert "invalid id value was provided for application_space_id" in captured.out


def test_create_application_name_fail_type_parameter(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()

    application = client.create_application(app_space_id, ["test"], "test create", "description", [])
    captured = capsys.readouterr()

    assert application is None
    assert "bad argument type for built-in operation" in captured.out


def test_update_application_success(capsys):
    client = ConfigClient()
    assert client is not None

    application_name = data.get_application_name()
    app_space_id = data.get_app_space_id()
    response = client.get_application_by_name(app_space_id, application_name)
    assert response is not None

    application = client.update_application(response.id, response.etag, response.display_name, "description", [])
    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert application is not None
    assert isinstance(application, UpdateApplication)


def test_update_application_empty():
    client = ConfigClient()
    assert client is not None

    application_name = data.get_application_name()
    app_space_id = data.get_app_space_id()
    response = client.get_application_by_name(app_space_id, application_name)
    assert response is not None

    def mocked_update_application(request: pb2.UpdateApplicationRequest):
        return None

    client.stub.UpdateApplication = mocked_update_application
    application = client.update_application(response.id, response.etag, response.display_name, "description", [])

    assert application is None


def test_update_application_fail_invalid_application(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()
    application_name = data.get_application_name()
    response = client.get_application_by_name(app_space_id, application_name)
    assert response is not None
    application_id = "gid:AAAAAdM5dfh564j5lIW1Ma1nFAA"

    application = client.update_application(application_id, response.etag, response.display_name,"description update", [])
    captured = capsys.readouterr()

    assert application is None
    assert "invalid id value was provided for id" in captured.out


def test_update_application_name_fail_type_parameter(capsys):
    client = ConfigClient()
    assert client is not None

    application_id = data.get_application_id()
    application_name = data.get_application_name()
    app_space_id = data.get_app_space_id()
    response = client.get_application_by_name(app_space_id, application_name)
    assert response is not None

    application = client.update_application(application_id, [response.etag], response.display_name, "description", [])
    captured = capsys.readouterr()

    assert application is None
    assert "bad argument type for built-in operation" in captured.out


def test_get_application_list_success(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()
    application_name = data.get_application_name()
    match = []
    match.append(application_name)

    application = client.list_applications(app_space_id, match, [])
    captured = capsys.readouterr()

    assert application is not None
    assert "invalid or expired access_token" not in captured.out


def test_get_application_list_wrong_app_space(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_id = "gid:AAAAAXX66V2_Jk3kjCCPThMQGaw"
    application_name = data.get_application_name()
    match = []
    match.append(application_name)
    application = client.list_applications(app_space_id, match, [])
    captured = capsys.readouterr()

    assert application is None
    assert "invalid id value was provided for app_space_id" in captured.out


def test_get_application_list_wrong_type(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()
    application_name = data.get_application_name()
    match = "test-create"

    application = client.list_applications(app_space_id, match, [])
    captured = capsys.readouterr()

    assert application is None
    assert "value length must be between 2 and 254 runes" in captured.out


def test_get_application_list_wrong_bookmark(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()
    application_name = data.get_application_name()
    match = []
    match.append(application_name)

    application = client.list_applications(app_space_id, match,
                                       ["RkI6a2N3US9RdnpsOGI4UWlPZU5OIGTHNTUQxcGNvU3NuZmZrQT09-r9S5McchAnB0Gz8oMjg_pWxPPdAZTJpaoNKq6HAAng"])
    captured = capsys.readouterr()

    assert application is None
    assert "invalid bookmark value" in captured.out


def test_get_application_list_empty_match(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()
    match = []

    application = client.list_applications(app_space_id, match, [])
    captured = capsys.readouterr()

    assert application is None
    assert "value must contain at least 1 item" in captured.out


def test_get_application_list_no_answer_match(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()
    application_name = data.get_application_name()
    application_name = "test-creation"
    match = []
    match.append(application_name)

    application = client.list_applications(app_space_id, match, [])
    captured = capsys.readouterr()

    assert application is not None
    assert application == []


def test_get_application_list_raise_exception(capsys):

    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()
    match = ""

    application = client.list_applications(app_space_id, match, [])
    captured = capsys.readouterr()
    assert "value must contain at least 1 item" in captured.out
    assert application is None


def test_get_application_list_empty():
    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()
    application_name = data.get_application_name()
    match = []
    match.append(application_name)

    def mocked_get_application_list(request: pb2.ListApplicationsRequest):
        return None

    client.stub.ListApplications = mocked_get_application_list
    application = client.list_applications(app_space_id, match, [])

    assert application is None


def test_del_application_success(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()
    right_now = str(int(time.time()))
    application = client.create_application(app_space_id, "automation-" + right_now,
                                  "Automation " + right_now, "description", [])

    assert application is not None

    response = client.delete_application(application.id, application.etag, [] )
    captured = capsys.readouterr()
    assert response is not None


def test_del_application_wrong_application_id(capsys):
    client = ConfigClient()
    assert client is not None

    application_id= data.get_app_space_id()
    response = client.delete_application(application_id, "oeprbUOYHUIYI75U", [] )
    captured = capsys.readouterr()
    assert response is None


def test_del_application_empty():
    client = ConfigClient()
    assert client is not None

    id = "gid:AAAAAjLRnbbaJE53rrjm_NJXyO"
    etag = "HcQ77D8CUWV"

    def mocked_delete_application(request: pb2.DeleteApplicationRequest):
        return None

    client.stub.DeleteApplication = mocked_delete_application
    response = client.delete_application(id, etag, [])

    assert response is None
