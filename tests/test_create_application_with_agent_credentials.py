import time

from indykite_sdk.config import ConfigClient
from indykite_sdk.model.create_application import CreateApplication
from indykite_sdk.model.create_application_agent import CreateApplicationAgent
from indykite_sdk.model.register_application_agent_credential import RegisterApplicationAgentCredential
from helpers import data


def test_create_application_with_agent_cred_success(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()
    right_now = int(time.time())
    application_name = "automation-application-"+str(right_now)
    application_agent_name = "automation-agent-"+str(right_now)
    application_agent_credentials_name = "automation-agent-cred-"+str(right_now)
    public_key_type = "jwk"
    expire_time = right_now + 120

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


def test_create_application_with_agent_cred_exists(capsys):
    client = ConfigClient()
    assert client is not None

    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()
    right_now = int(time.time())
    application_name = "automation-application-" + str(right_now)
    application_agent_name = "automation-agent-" + str(right_now)
    application_agent_credentials_name = "automation-agent-cred-" + str(right_now)
    public_key_type = "jwk"
    expire_time = right_now + 120

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


def test_create_application_with_agent_cred_no_expire_time(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_id = data.get_app_space_id()
    right_now = int(time.time() + 12365)
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
