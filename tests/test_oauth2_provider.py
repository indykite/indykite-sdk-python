import time
import random

from indykite_sdk.config import ConfigClient
from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.create_oauth2_provider import CreateOAuth2Provider
from indykite_sdk.model.update_oauth2_provider import UpdateOAuth2Provider
from helpers import data


def test_read_oauth2_provider_success(capsys):
    client = ConfigClient()
    assert client is not None

    oauth2_provider_id = data.get_oauth2_provider_id()
    oauth2_provider = client.read_oauth2_provider(oauth2_provider_id)
    captured = capsys.readouterr()

    assert oauth2_provider is not None
    assert "invalid or expired access_token" not in captured.out


def test_read_oauth2_provider_empty():
    client = ConfigClient()
    assert client is not None

    oauth2_provider_id = data.get_oauth2_provider_id()

    def mocked_read_oauth2_provider(request: pb2.ReadOAuth2ProviderRequest):
        return None

    client.stub.ReadOAuth2Provider = mocked_read_oauth2_provider
    oauth2_provider = client.read_oauth2_provider(oauth2_provider_id)

    assert oauth2_provider is None


def test_read_oauth2_provider_wrong_id(capsys):
    oauth2_provider_id = "aaaaaaaaaaaaaaa"

    client = ConfigClient()
    assert client is not None

    response = client.read_oauth2_provider(oauth2_provider_id)
    captured = capsys.readouterr()
    assert("invalid ReadOAuth2ProviderRequest.Id: value length must be between 22 and 254 runes, inclusive" in captured.out)
    assert response is None


def test_create_oauth2_provider_success(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    num = str(int(random.random()))
    app_space_id = data.get_app_space_id()
    oauth2_provider_config = data.get_oauth2_provider()

    config = client.create_oauth2_provider(app_space_id,
                                           "automation-"+num+right_now,
                                           "Automation "+num+right_now,
                                           "description",
                                           oauth2_provider_config,
                                           [])
    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert config is not None
    assert isinstance(config, CreateOAuth2Provider)


def test_create_oauth2_provider_empty(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    app_space_id = data.get_app_space_id()
    oauth2_provider_config = data.get_oauth2_provider()

    def mocked_create_oauth2_provider(request: pb2.CreateOAuth2ProviderRequest):
        return None

    client.stub.CreateOAuth2Provider = mocked_create_oauth2_provider
    config = client.create_oauth2_provider(app_space_id,
                                           "automation-"+right_now,
                                           "Automation "+right_now,
                                           "description",
                                           oauth2_provider_config,
                                           [])

    assert config is None


def test_create_oauth2_provider_exception(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    app_space_id = data.get_app_space_id()
    config = client.create_oauth2_provider(app_space_id,
                                           "automation-"+right_now,
                                           "Automation "+right_now,
                                           "description",
                                           "description",
                                           [])

    captured = capsys.readouterr()
    assert "Message must be initialized with a dict: indykite.config.v1beta1.CreateOAuth2ProviderRequest" in captured.out


def test_update_oauth2_provider_success(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    oauth2_provider_id = data.get_oauth2_provider_id()
    response = client.read_oauth2_provider(oauth2_provider_id)
    assert response is not None

    oauth2_provider_config = data.get_oauth2_provider()
    config_response = client.update_oauth2_provider(response.id,
                                                    response.etag,
                                                    "Automation "+right_now,
                                                    "description "+right_now,
                                                    oauth2_provider_config,
                                                    [])

    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert config_response is not None
    assert isinstance(config_response, UpdateOAuth2Provider)


def test_update_oauth2_provider_empty(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    oauth2_provider_id = data.get_oauth2_provider_id()
    response = client.read_oauth2_provider(oauth2_provider_id)
    assert response is not None

    oauth2_provider_config = data.get_oauth2_provider()

    def mocked_update_oauth2_provider(request: pb2.UpdateOAuth2ProviderRequest):
        return None

    client.stub.UpdateOAuth2Provider = mocked_update_oauth2_provider
    config_response = client.update_oauth2_provider(response.id,
                                                    response.etag,
                                                    "Automation " + right_now,
                                                    "description " + right_now,
                                                    oauth2_provider_config,
                                                    [])

    assert config_response is None


def test_update_oauth2_provider_exception(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    oauth2_provider_id = data.get_oauth2_provider_id()
    response = client.read_oauth2_provider(oauth2_provider_id)
    assert response is not None

    config_response = client.update_oauth2_provider(response.id,
                                                    response.etag,
                                                    "Automation "+right_now,
                                                    "description "+right_now,
                                                    "description",
                                                    [])

    captured = capsys.readouterr()
    assert "Message must be initialized with a dict: indykite.config.v1beta1.UpdateOAuth2ProviderRequest" in captured.out


def test_del_oauth2_provider_success(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    app_space_id = data.get_app_space_id()
    config = data.get_oauth2_provider()

    oauth2_provider = client.create_oauth2_provider(app_space_id,
                                                    "automation-" + right_now,
                                                    "Automation " + right_now,
                                                    "description",
                                                    config,
                                                    [])

    assert oauth2_provider is not None

    response = client.delete_oauth2_provider(oauth2_provider.id, oauth2_provider.etag, [] )
    captured = capsys.readouterr()
    assert response is not None


def test_del_oauth2_provider_empty(capsys):
    client = ConfigClient()
    assert client is not None

    id = "gid:AAAAAjLRnbbaJE53rrjm_NJXyO"
    etag = "HcQ77D8CUWV"

    def mocked_delete_oauth2_provider(request: pb2.DeleteOAuth2ProviderRequest):
        return None

    client.stub.DeleteOAuth2Provider = mocked_delete_oauth2_provider
    response = client.delete_oauth2_provider(id, etag, [])

    assert response is None


def test_del_oauth2_provider_wrong_id(capsys):
    client = ConfigClient()
    assert client is not None

    id = "gid:AAAAAjLRnbbaJE53rrjm_NJXyO"
    etag = "HcQ77D8CUWV"

    response = client.delete_oauth2_provider(id, etag, [])
    captured = capsys.readouterr()
    assert response is None
