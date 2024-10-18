import pytest
import time

from indykite_sdk.config import ConfigClient
from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.register_application_agent_credential import RegisterApplicationAgentCredential
from indykite_sdk.model.application_agent import ApplicationAgent
from helpers import data
from datetime import datetime


@pytest.fixture
def client():
    return ConfigClient()


@pytest.fixture
def application_id():
    return data.get_application_id()


@pytest.fixture
def application_agent_id():
    return data.get_application_agent_id()


@pytest.fixture
def application_agent_credential_id():
    return data.get_application_agent_credential_id()


def test_read_application_agent_credential_wrong_id(client, capsys):
    application_agent_credential_id = "aaaaaaaaaaaaaaa"
    response = client.read_application_agent_credential(application_agent_credential_id)
    captured = capsys.readouterr()
    print(captured)
    assert("invalid ReadApplicationAgentCredentialRequest.Id" in captured.err)


def test_read_application_agent_credential_success(client, application_agent_credential_id, capsys):
    application_agent = client.read_application_agent_credential(application_agent_credential_id)
    captured = capsys.readouterr()
    assert application_agent is not None
    assert "invalid or expired access_token" not in captured.out


def test_read_application_agent_credential_empty(client, application_agent_credential_id):

    def mocked_read_application_agent_credential(request: pb2.ReadApplicationAgentCredentialRequest):
        return None

    client.stub.ReadApplicationAgentCredential = mocked_read_application_agent_credential
    application_agent_credential = client.read_application_agent_credential(application_agent_credential_id)
    assert application_agent_credential is None


def test_register_application_agent_credential_jwk_success(client, application_agent_id, capsys):
    right_now = str(int(time.time()))
    jwk = None
    t = datetime.now().timestamp()
    expire_time_in_seconds = int(t) + 2678400
    application_agent_credential = client.register_application_agent_credential_jwk(application_agent_id,
                                                                                    "automation-"+right_now, jwk,
                                                                                    expire_time_in_seconds,
                                                                                   [])
    captured = capsys.readouterr()
    assert "invalid or expired access_token" not in captured.out
    assert application_agent_credential is not None
    assert isinstance(application_agent_credential, RegisterApplicationAgentCredential)
    application_agent = client.read_application_agent_by_id(application_agent_credential.application_agent_id)
    # assert isinstance(application_agent, ApplicationAgent)
    response = client.delete_application_agent_credential(application_agent_credential.id, [], application_agent.etag)
    assert response is not None


def test_register_application_agent_credential_jwk_empty(client, application_agent_id):
    right_now = str(int(time.time()))
    jwk = None
    t = datetime.now().timestamp()
    expire_time_in_seconds = int(t) + 2678400

    def mocked_register_application_agent_credential(request: pb2.RegisterApplicationAgentCredentialRequest):
        return None

    client.stub.RegisterApplicationAgentCredential = mocked_register_application_agent_credential
    application_agent_credential = client.register_application_agent_credential_jwk(application_agent_id,
                                                                                    "automation-"+right_now, jwk,
                                                                                    expire_time_in_seconds,
                                                                                    [])

    assert application_agent_credential is None


def test_register_application_agent_credential_jwk_exception(client, application_agent_id, capsys):
    right_now = str(int(time.time()))
    jwk = None
    t = datetime.now().timestamp()
    expire_time_in_seconds = int(t) + 2678400
    application_agent_credential = client.register_application_agent_credential_jwk(application_agent_id,
                                                                                    "automation-"+right_now, "automation",
                                                                                    expire_time_in_seconds,
                                                                                   [])

    captured = capsys.readouterr()
    assert "expected bytes, str found" in captured.err


def test_register_application_agent_credential_pem_success(client, application_agent_id, capsys):
    right_now = str(int(time.time()))
    pem = None
    t = datetime.now().timestamp()
    expire_time_in_seconds = int(t) + 2678400
    application_agent_credential = client.register_application_agent_credential_pem(application_agent_id,
                                                                                    "automation-"+right_now, pem,
                                                                                    expire_time_in_seconds,
                                                                                   [])
    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert application_agent_credential is not None
    assert isinstance(application_agent_credential, RegisterApplicationAgentCredential)
    application_agent = client.read_application_agent_by_id(application_agent_credential.application_agent_id)
    # assert isinstance(application_agent, ApplicationAgent)
    response = client.delete_application_agent_credential(application_agent_credential.id, [], application_agent.etag)
    assert response is not None


def test_register_application_agent_credential_pem_empty(client, application_agent_id):
    right_now = str(int(time.time()))
    pem = None
    t = datetime.now().timestamp()
    expire_time_in_seconds = int(t) + 2678400

    def mocked_register_application_agent_credential(request: pb2.RegisterApplicationAgentCredentialRequest):
        return None

    client.stub.RegisterApplicationAgentCredential = mocked_register_application_agent_credential
    application_agent_credential = client.register_application_agent_credential_pem(application_agent_id,
                                                                                    "automation-"+right_now, pem,
                                                                                    expire_time_in_seconds,
                                                                                   [])

    assert application_agent_credential is None


def test_register_application_agent_credential_pem_exception(client, application_agent_id, capsys):
    right_now = str(int(time.time()))
    pem = "automation"
    t = datetime.now().timestamp()
    expire_time_in_seconds = int(t) + 2678400

    application_agent_credential = client.register_application_agent_credential_pem(application_agent_id,
                                                                                    "automation-"+right_now, pem,
                                                                                    expire_time_in_seconds,
                                                                                   [])

    captured = capsys.readouterr()
    assert "expected bytes, str found" in captured.err


def test_del_application_agent_credential_success(client, application_agent_credential_id, capsys):
    bookmark = "RkI6a2N3US9RdnpsOGI4UWlPZU5OIGTHNTUQxcGNvU3NuZmZrQT09-r9S5McchAnB0Gz8oMjg_pWxPPdAZTJpaoNKq6HAAng"
    etag = "npsOGI4UW"

    def mocked_delete_application_agent_credential(request: pb2.DeleteApplicationAgentCredentialRequest):
        return bookmark

    client.stub.DeleteApplicationAgentCredential = mocked_delete_application_agent_credential
    response = client.delete_application_agent_credential(application_agent_credential_id, [], etag)
    assert response is not None


def test_del_application_agent_wrong_application_agent_id(client, application_agent_credential_id, capsys):
    etag = "npsOGI4UW"
    response = client.delete_application_agent_credential(application_agent_credential_id, [], etag)
    captured = capsys.readouterr()
    assert ("invalid eTag value" in captured.err)


def test_del_application_agent_empty(client):
    id = "gid:AAAAAjLRnbbaJE53rrjm_NJXyO"
    etag = "npsOGI4UW"

    def mocked_delete_application_agent_credential(request: pb2.DeleteApplicationAgentRequest):
        return None

    client.stub.DeleteApplicationAgentCredential = mocked_delete_application_agent_credential
    response = client.delete_application_agent_credential(id, [], etag)
    assert response is None
    etag = "npsOGI4UW"
    response = client.delete_application_agent_credential(id, [], etag)
    captured = capsys.readouterr()
    assert ("invalid id value was provided for id" in captured.err)


def test_del_application_agent_empty(client):
    id = "gid:AAAAAjLRnbbaJE53rrjm_NJXyO"
    etag = "npsOGI4UW"

    def mocked_delete_application_agent_credential(request: pb2.DeleteApplicationAgentRequest):
        return None

    client.stub.DeleteApplicationAgentCredential = mocked_delete_application_agent_credential
    response = client.delete_application_agent_credential(id, [], etag)
    assert response is None
