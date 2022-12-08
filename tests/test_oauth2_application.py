import time
import random

from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from jarvis_sdk.model.create_oauth2_application import CreateOAuth2Application
from jarvis_sdk.model.update_oauth2_application import UpdateOAuth2Application
from tests.helpers import data


def test_read_oauth2_application_success(capsys):
    client = ConfigClient()
    assert client is not None

    oauth2_application_id = data.get_oauth2_application_id()
    oauth2_application = client.read_oauth2_application(oauth2_application_id)
    captured = capsys.readouterr()

    assert oauth2_application is not None
    assert "invalid or expired access_token" not in captured.out


def test_read_oauth2_application_empty():
    client = ConfigClient()
    assert client is not None

    oauth2_application_id = data.get_oauth2_application_id()

    def mocked_read_oauth2_application(request: pb2.ReadOAuth2ApplicationRequest):
        return None

    client.stub.ReadOAuth2Application = mocked_read_oauth2_application
    oauth2_application = client.read_oauth2_application(oauth2_application_id)

    assert oauth2_application is None


def test_read_oauth2_application_wrong_id(capsys):
    oauth2_application_id = "aaaaaaaaaaaaaaa"

    client = ConfigClient()
    assert client is not None

    response = client.read_oauth2_application(oauth2_application_id)
    captured = capsys.readouterr()
    assert("invalid ReadOAuth2ApplicationRequest.Id: value length must be between 22 and 254 runes, inclusive" in captured.out)
    assert response is None


def test_create_oauth2_application_success(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    num = str(int(random.random()))
    oauth2_provider_id = data.get_oauth2_provider_id()
    oauth2_application_config = data.get_oauth2_application()

    config = client.create_oauth2_application(oauth2_provider_id,
                                              "automation-"+num+right_now,
                                              "Automation "+num+right_now,
                                              "description",
                                              oauth2_application_config,
                                              [])
    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert config is not None
    assert isinstance(config, CreateOAuth2Application)


def test_create_oauth2_application_empty(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    oauth2_provider_id = data.get_oauth2_provider_id()
    oauth2_application_config = data.get_oauth2_application()

    def mocked_create_oauth2_application(request: pb2.CreateOAuth2ApplicationRequest):
        return None

    client.stub.CreateOAuth2Application = mocked_create_oauth2_application
    config = client.create_oauth2_application(oauth2_provider_id,
                                              "automation-"+right_now,
                                              "Automation "+right_now,
                                              "description",
                                              oauth2_application_config,
                                              [])

    assert config is None


def test_create_oauth2_application_exception(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    oauth2_provider_id = data.get_oauth2_provider_id()
    config = client.create_oauth2_application(oauth2_provider_id,
                                              "automation-"+right_now,
                                              "Automation "+right_now,
                                              "description",
                                              "description",
                                              [])

    captured = capsys.readouterr()
    assert "expected indykite.config.v1beta1.OAuth2ApplicationConfig got str" in captured.out


def test_update_oauth2_application_success(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    oauth2_application_id = data.get_oauth2_application_id()
    response = client.read_oauth2_application(oauth2_application_id)
    assert response is not None

    oauth2_application_config = data.get_oauth2_application()
    config_response = client.update_oauth2_application(response.id,
                                                       response.etag,
                                                       "Automation "+right_now,
                                                       "description "+right_now,
                                                       oauth2_application_config,
                                                       [])

    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert config_response is not None
    assert isinstance(config_response, UpdateOAuth2Application)


def test_update_oauth2_application_empty(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    oauth2_application_id = data.get_oauth2_application_id()
    response = client.read_oauth2_application(oauth2_application_id)
    assert response is not None

    oauth2_application_config = data.get_oauth2_application()

    def mocked_update_oauth2_application(request: pb2.UpdateOAuth2ApplicationRequest):
        return None

    client.stub.UpdateOAuth2Application = mocked_update_oauth2_application
    config_response = client.update_oauth2_application(response.id,
                                                       response.etag,
                                                       "Automation " + right_now,
                                                       "description " + right_now,
                                                       oauth2_application_config,
                                                       [])

    assert config_response is None


def test_update_oauth2_application_exception(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    oauth2_application_id = data.get_oauth2_application_id()
    response = client.read_oauth2_application(oauth2_application_id)
    assert response is not None

    config_response = client.update_oauth2_application(response.id,
                                                       response.etag,
                                                       "Automation "+right_now,
                                                       "description "+right_now,
                                                       "description",
                                                       [])

    captured = capsys.readouterr()
    assert "expected indykite.config.v1beta1.OAuth2ApplicationConfig got str" in captured.out


def test_del_oauth2_application_success(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    oauth2_provider_id = data.get_oauth2_provider_id()
    config = data.get_oauth2_application()

    oauth2_application = client.create_oauth2_application(oauth2_provider_id,
                                                          "automation-" + right_now,
                                                          "Automation " + right_now,
                                                          "description",
                                                          config,
                                                          [])

    assert oauth2_application is not None

    response = client.delete_oauth2_application(oauth2_application.id, oauth2_application.etag, [] )
    captured = capsys.readouterr()
    assert response is not None


def test_del_oauth2_application_empty(capsys):
    client = ConfigClient()
    assert client is not None

    id = "gid:AAAAAjLRnbbaJE53rrjm_NJXyO"
    etag = "HcQ77D8CUWV"

    def mocked_delete_oauth2_application(request: pb2.DeleteOAuth2ApplicationRequest):
        return None

    client.stub.DeleteOAuth2Application = mocked_delete_oauth2_application
    response = client.delete_oauth2_application(id, etag, [])

    assert response is None


def test_del_oauth2_application_wrong_id(capsys):
    client = ConfigClient()
    assert client is not None

    id = "gid:AAAAAjLRnbbaJE53rrjm_NJXyO"
    etag = "HcQ77D8CUWV"

    response = client.delete_oauth2_application(id, etag, [])
    captured = capsys.readouterr()
    assert response is None
