import pytest
import time

from indykite_sdk.config import ConfigClient
from indykite_sdk.model.create_application import CreateApplication
from indykite_sdk.model.create_application_agent import CreateApplicationAgent
from indykite_sdk.model.register_application_agent_credential import RegisterApplicationAgentCredential
from helpers import data


@pytest.fixture
def client():
    return ConfigClient()


@pytest.fixture
def right_now():
    return str(int(time.time()) + 2)


@pytest.fixture
def app_space_id():
    return data.get_app_space_id()


def test_create_application_with_agent_cred_success(client, app_space_id, right_now, capsys):
    application_name = "automation-application-"+str(right_now)
    application_agent_name = "automation-agent-"+str(right_now)
    application_agent_credentials_name = "automation-agent-cred-"+str(right_now)
    public_key_type = "jwk"
    expire_time = int(right_now) + 25000

    response = client.create_application_with_agent_credentials(
            app_space_id,
            application_name,
            application_agent_name,
            application_agent_credentials_name,
            public_key_type,
            public_key=None,
            expire_time=expire_time)
    captured = capsys.readouterr()

    assert response is not None
    assert isinstance(response["response_application"], CreateApplication)
    assert isinstance(response["response_application_agent"], CreateApplicationAgent)
    assert isinstance(response["response_application_agent_credentials"], RegisterApplicationAgentCredential)


def test_create_application_with_agent_cred_exists(client, app_space_id, right_now, capsys):
    application_name = "automation-application-" + str(right_now)
    application_agent_name = "automation-agent-" + str(right_now)
    application_agent_credentials_name = "automation-agent-cred-" + str(right_now)
    public_key_type = "jwk"
    expire_time = int(right_now) + 12000

    response = client.create_application_with_agent_credentials(
        app_space_id,
        application_name,
        application_agent_name,
        application_agent_credentials_name,
        public_key_type,
        public_key=None,
        expire_time=expire_time)

    response2 = client.create_application_with_agent_credentials(
        app_space_id,
        application_name,
        application_agent_name,
        application_agent_credentials_name,
        public_key_type,
        public_key=None,
        expire_time=expire_time)
    captured = capsys.readouterr()
    assert "config entity with given name already exist" in captured.err


def test_create_application_with_agent_cred_no_expire_time(client, app_space_id, right_now, capsys):
    application_name = "automation-application-"+str(right_now)
    application_agent_name = "automation-agent-"+str(right_now)
    application_agent_credentials_name = "automation-agent-cred-"+str(right_now)
    public_key_type = "pem"

    response = client.create_application_with_agent_credentials(
            app_space_id,
            application_name,
            application_agent_name,
            application_agent_credentials_name,
            public_key_type,
            public_key=None,
            expire_time=None)
    captured = capsys.readouterr()

    assert response is not None
    assert isinstance(response["response_application"], CreateApplication)
    assert isinstance(response["response_application_agent"], CreateApplicationAgent)
    assert isinstance(response["response_application_agent_credentials"], RegisterApplicationAgentCredential)
