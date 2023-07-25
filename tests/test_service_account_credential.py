import time

from indykite_sdk.config import ConfigClient
from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.register_service_account_credential import RegisterServiceAccountCredential
from helpers import data
from datetime import datetime


def test_read_service_account_credential_wrong_id(capsys):
    service_account_credential_id = "aaaaaaaaaaaaaaa"

    client = ConfigClient()
    assert client is not None

    response = client.read_service_account_credential(service_account_credential_id)
    captured = capsys.readouterr()
    assert("invalid ReadServiceAccountCredentialRequest.Id: value length must be between 22 and 254 runes, inclusive" in captured.err)


def test_read_service_account_credential_success(capsys):
    client = ConfigClient()
    assert client is not None

    service_account_credential_id = data.get_service_account_credential_id()
    service_account = client.read_service_account_credential(service_account_credential_id)
    captured = capsys.readouterr()

    assert service_account is not None
    assert "invalid or expired access_token" not in captured.out


def test_read_service_account_credential_empty():
    client = ConfigClient()
    assert client is not None

    service_account_credential_id = data.get_service_account_credential_id()

    def mocked_read_service_account_credential(request: pb2.ReadServiceAccountCredentialRequest):
        return None

    client.stub.ReadServiceAccountCredential = mocked_read_service_account_credential
    service_account_credential = client.read_service_account_credential(service_account_credential_id)

    assert service_account_credential is None


def test_register_service_account_credential_jwk_success(capsys):
    client = ConfigClient()
    assert client is not None

    service_account_id = data.get_service_account_id()
    right_now = str(int(time.time()))
    jwk = None
    t = datetime.now().timestamp()
    expire_time_in_seconds = int(t) + 2678400

    service_account_credential = client.register_service_account_credential_jwk(service_account_id,
                                                                                    "automation-"+right_now, jwk,
                                                                                    expire_time_in_seconds,
                                                                                     [])
    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert service_account_credential is not None
    assert isinstance(service_account_credential, RegisterServiceAccountCredential)


def test_register_service_account_credential_jwk_empty():
    client = ConfigClient()
    assert client is not None

    service_account_id = data.get_service_account_id()
    right_now = str(int(time.time()))
    jwk = None
    t = datetime.now().timestamp()
    expire_time_in_seconds = int(t) + 2678400

    def mocked_register_service_account_credential(request: pb2.RegisterServiceAccountCredentialRequest):
        return None

    client.stub.RegisterServiceAccountCredential = mocked_register_service_account_credential
    service_account_credential = client.register_service_account_credential_jwk(service_account_id,
                                                                                    "automation-"+right_now, jwk,
                                                                                    expire_time_in_seconds,[])

    assert service_account_credential is None


def test_register_service_account_credential_jwk_exception(capsys):
    client = ConfigClient()
    assert client is not None

    service_account_id = data.get_service_account_id()
    right_now = str(int(time.time()))
    jwk = None
    t = datetime.now().timestamp()
    expire_time_in_seconds = int(t) + 2678400

    service_account_credential = client.register_service_account_credential_jwk(service_account_id,
                                                                                    "automation-"+right_now, "automation",
                                                                                    expire_time_in_seconds,[])

    captured = capsys.readouterr()
    assert "expected bytes, str found" in captured.err


def test_register_service_account_credential_pem_success(capsys):
    client = ConfigClient()
    assert client is not None

    service_account_id = data.get_service_account_id()
    right_now = str(int(time.time()))
    pem = None
    t = datetime.now().timestamp()
    expire_time_in_seconds = int(t) + 2678400

    service_account_credential = client.register_service_account_credential_pem(service_account_id,
                                                                                    "automation-"+right_now, pem,
                                                                                    expire_time_in_seconds,[])
    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert service_account_credential is not None
    assert isinstance(service_account_credential, RegisterServiceAccountCredential)


def test_register_service_account_credential_pem_empty():
    client = ConfigClient()
    assert client is not None

    service_account_id = data.get_service_account_id()
    right_now = str(int(time.time()))
    pem = None
    t = datetime.now().timestamp()
    expire_time_in_seconds = int(t) + 2678400

    def mocked_register_service_account_credential(request: pb2.RegisterServiceAccountCredentialRequest):
        return None

    client.stub.RegisterServiceAccountCredential = mocked_register_service_account_credential
    service_account_credential = client.register_service_account_credential_pem(service_account_id,
                                                                                    "automation-"+right_now, pem,
                                                                                    expire_time_in_seconds,[])

    assert service_account_credential is None


def test_register_service_account_credential_pem_exception(capsys):
    client = ConfigClient()
    assert client is not None

    service_account_id = data.get_service_account_id()
    right_now = str(int(time.time()))
    pem = "automation"
    t = datetime.now().timestamp()
    expire_time_in_seconds = int(t) + 2678400

    service_account_credential = client.register_service_account_credential_pem(service_account_id,
                                                                                    "automation-"+right_now, pem,
                                                                                    expire_time_in_seconds,[])

    captured = capsys.readouterr()
    assert "expected bytes, str found" in captured.err


def test_del_service_account_credential_success(capsys):
    client = ConfigClient()
    assert client is not None

    service_account_credential_id = data.get_service_account_credential_id()
    right_now = str(int(time.time()))
    etag = "HcQ77D8CUWV"
    bookmark = "RkI6a2N3US9RdnpsOGI4UWlPZU5OIGTHNTUQxcGNvU3NuZmZrQT09-r9S5McchAnB0Gz8oMjg_pWxPPdAZTJpaoNKq6HAAng"

    def mocked_delete_service_account_credential(request: pb2.DeleteServiceAccountCredentialRequest):
        return bookmark

    client.stub.DeleteServiceAccountCredential = mocked_delete_service_account_credential
    response = client.delete_service_account_credential(service_account_credential_id, etag, [])
    captured = capsys.readouterr()
    assert response is not None


def test_del_service_account_wrong_service_account_id(capsys):
    client = ConfigClient()
    assert client is not None

    service_account_credential_id = data.get_service_account_id()
    etag = "HcQ77D8CUWV"
    response = client.delete_service_account_credential(service_account_credential_id, etag, [] )
    captured = capsys.readouterr()
    assert "invalid id value was provided for id" in captured.err


def test_del_service_account_empty():
    client = ConfigClient()
    assert client is not None

    id = "gid:AAAAAjLRnbbaJE53rrjm_NJXyO"
    etag = "HcQ77D8CUWV"

    def mocked_delete_service_account_credential(request: pb2.DeleteServiceAccountRequest):
        return None

    client.stub.DeleteServiceAccountCredential = mocked_delete_service_account_credential
    response = client.delete_service_account_credential(id, etag, [])

    assert response is None
