import time

from indykite_sdk.config import ConfigClient
from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.register_application_agent_credential import RegisterApplicationAgentCredential
from helpers import data
from datetime import datetime


def test_get_application_agent_credential_wrong_id(capsys):
    application_agent_credential_id = "aaaaaaaaaaaaaaa"

    client = ConfigClient()
    assert client is not None

    response = client.get_application_agent_credential(application_agent_credential_id)
    captured = capsys.readouterr()
    print(captured)
    assert("invalid ReadApplicationAgentCredentialRequest.Id" in captured.err)


def test_get_application_agent_credential_success(capsys):
    client = ConfigClient()
    assert client is not None

    application_agent_credential_id = data.get_application_agent_credential_id()
    application_agent = client.get_application_agent_credential(application_agent_credential_id)
    captured = capsys.readouterr()

    assert application_agent is not None
    assert "invalid or expired access_token" not in captured.out


def test_get_application_agent_credential_empty():
    client = ConfigClient()
    assert client is not None

    application_agent_credential_id = data.get_application_agent_credential_id()

    def mocked_get_application_agent_credential(request: pb2.ReadApplicationAgentCredentialRequest):
        return None

    client.stub.ReadApplicationAgentCredential = mocked_get_application_agent_credential
    application_agent_credential = client.get_application_agent_credential(application_agent_credential_id)

    assert application_agent_credential is None


def test_register_application_agent_credential_jwk_success(capsys):
    client = ConfigClient()
    assert client is not None

    application_agent_id = data.get_application_agent_id()
    default_tenant_id = data.get_tenant_id()
    right_now = str(int(time.time()))
    jwk = None
    t = datetime.now().timestamp()
    expire_time_in_seconds = int(t) + 2678400

    application_agent_credential = client.register_application_agent_credential_jwk(application_agent_id,
                                                                                    "automation-"+right_now, jwk,
                                                                                    expire_time_in_seconds,
                                                                                    default_tenant_id, [])
    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert application_agent_credential is not None
    assert isinstance(application_agent_credential, RegisterApplicationAgentCredential)


def test_register_application_agent_credential_jwk_empty():
    client = ConfigClient()
    assert client is not None

    application_agent_id = data.get_application_agent_id()
    default_tenant_id = data.get_tenant_id()
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
                                                                                    default_tenant_id, [])

    assert application_agent_credential is None


def test_register_application_agent_credential_jwk_exception(capsys):
    client = ConfigClient()
    assert client is not None

    application_agent_id = data.get_application_agent_id()
    default_tenant_id = data.get_tenant_id()
    right_now = str(int(time.time()))
    jwk = None
    t = datetime.now().timestamp()
    expire_time_in_seconds = int(t) + 2678400

    application_agent_credential = client.register_application_agent_credential_jwk(application_agent_id,
                                                                                    "automation-"+right_now, "automation",
                                                                                    expire_time_in_seconds,
                                                                                    default_tenant_id, [])

    captured = capsys.readouterr()
    assert "expected bytes, str found" in captured.err


def test_register_application_agent_credential_pem_success(capsys):
    client = ConfigClient()
    assert client is not None

    application_agent_id = data.get_application_agent_id()
    default_tenant_id = data.get_tenant_id()
    right_now = str(int(time.time()))
    pem = None
    t = datetime.now().timestamp()
    expire_time_in_seconds = int(t) + 2678400

    application_agent_credential = client.register_application_agent_credential_pem(application_agent_id,
                                                                                    "automation-"+right_now, pem,
                                                                                    expire_time_in_seconds,
                                                                                    default_tenant_id, [])
    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert application_agent_credential is not None
    assert isinstance(application_agent_credential, RegisterApplicationAgentCredential)


def test_register_application_agent_credential_pem_empty():
    client = ConfigClient()
    assert client is not None

    application_agent_id = data.get_application_agent_id()
    default_tenant_id = data.get_tenant_id()
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
                                                                                    default_tenant_id, [])

    assert application_agent_credential is None


def test_register_application_agent_credential_pem_exception(capsys):
    client = ConfigClient()
    assert client is not None

    application_agent_id = data.get_application_agent_id()
    default_tenant_id = data.get_tenant_id()
    right_now = str(int(time.time()))
    pem = "automation"
    t = datetime.now().timestamp()
    expire_time_in_seconds = int(t) + 2678400

    application_agent_credential = client.register_application_agent_credential_pem(application_agent_id,
                                                                                    "automation-"+right_now, pem,
                                                                                    expire_time_in_seconds,
                                                                                    default_tenant_id, [])

    captured = capsys.readouterr()
    assert "expected bytes, str found" in captured.err


def test_del_application_agent_credential_success(capsys):
    client = ConfigClient()
    assert client is not None

    application_agent_credential_id = data.get_application_agent_credential_id()
    right_now = str(int(time.time()))
    bookmark = "RkI6a2N3US9RdnpsOGI4UWlPZU5OIGTHNTUQxcGNvU3NuZmZrQT09-r9S5McchAnB0Gz8oMjg_pWxPPdAZTJpaoNKq6HAAng"

    def mocked_delete_application_agent_credential(request: pb2.DeleteApplicationAgentCredentialRequest):
        return bookmark

    client.stub.DeleteApplicationAgentCredential = mocked_delete_application_agent_credential
    response = client.delete_application_agent_credential(application_agent_credential_id, [] )
    captured = capsys.readouterr()
    # assert "method DeleteDocument not implemented"
    assert response is not None


def test_del_application_agent_wrong_application_agent_id(capsys):
    client = ConfigClient()
    assert client is not None

    application_agent_credential_id= data.get_application_id()
    response = client.delete_application_agent_credential(application_agent_credential_id, [] )
    captured = capsys.readouterr()
    assert ("invalid id value was provided for id" in captured.err)


def test_del_application_agent_empty():
    client = ConfigClient()
    assert client is not None

    id = "gid:AAAAAjLRnbbaJE53rrjm_NJXyO"

    def mocked_delete_application_agent_credential(request: pb2.DeleteApplicationAgentRequest):
        return None

    client.stub.DeleteApplicationAgentCredential = mocked_delete_application_agent_credential
    response = client.delete_application_agent_credential(id, [])

    assert response is None
