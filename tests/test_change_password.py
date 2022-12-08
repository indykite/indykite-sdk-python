from jarvis_sdk.cmd import IdentityClient
from jarvis_sdk.indykite.identity.v1beta1 import identity_management_api_pb2 as pb2
from tests.helpers import data


def test_change_password_short_token(capsys):
    token = "short_token"
    password = data.get_new_password()

    client = IdentityClient()
    assert client is not None

    response = client.change_password(token, password)
    captured = capsys.readouterr()

    assert captured.out == "Token must be 32 chars or more.\n"
    assert response is None


def test_change_password_expired_token(capsys):
    token = data.get_expired_token()
    password = data.get_new_password()

    client = IdentityClient()
    assert client is not None

    response = client.change_password(token, password)
    captured = capsys.readouterr()

    assert "invalid or expired access_token" in captured.out
    assert response is None


def test_change_password_success(registration):
    token = registration[0]
    password = data.get_new_password()

    client = IdentityClient()
    assert client is not None

    def mocked_change_password(request: pb2.ChangePasswordRequest):
        assert request.token == token
        return pb2.ChangePasswordResponse()

    client.stub.ChangePassword = mocked_change_password
    response = client.change_password(token, password)
    assert response == "The password has been changed successfully"


def test_password_of_user_wrong_twin_id(capsys):
    digital_twin_id = "696e6479-6b69-465-8000-010f00000000"
    tenant_id = data.get_tenant()
    password = data.get_new_password()

    client = IdentityClient()
    assert client is not None

    response = client.change_password_of_user(digital_twin_id, tenant_id, password)
    captured = capsys.readouterr()

    assert (
        captured.out == "The digital twin id is not in UUID4 format:\nbadly formed hexadecimal UUID string\n"
    )
    assert response is None


def test_password_of_user_wrong_tenant_id(capsys):
    digital_twin_id = "696e6479-6b69-4465-8000-010f00000000"
    tenant_id = "696e6479-6b6-4465-8000-010f00000000"
    password = data.get_new_password()

    client = IdentityClient()
    assert client is not None

    response = client.change_password_of_user(digital_twin_id, tenant_id, password)
    captured = capsys.readouterr()

    assert captured.out == "The tenant id is not in UUID4 format:\nbadly formed hexadecimal UUID string\n"
    assert response is None


def test_password_of_user_nonexisting_twin_id(capsys):
    digital_twin_id = "e1e9f07d-fc6e-4629-84d1-8d23836524ba"
    tenant_id = data.get_tenant()
    password = data.get_new_password()

    client = IdentityClient()
    assert client is not None

    response = client.change_password_of_user(digital_twin_id, tenant_id, password)
    captured = capsys.readouterr()

    assert "digital_twin was not found" in captured.out
    assert response is None


def test_password_of_user_success(capsys):
    digital_twin_id = data.get_digital_twin()
    tenant_id = data.get_tenant()
    password = data.get_new_password()

    client = IdentityClient()
    assert client is not None

    def mocked_change_password_of_user(request: pb2.ChangePasswordRequest):
        assert request.password == password
        return pb2.ChangePasswordResponse()

    client.stub.ChangePassword = mocked_change_password_of_user
    response = client.change_password_of_user(digital_twin_id, tenant_id, password)

    assert response is not None
    assert response == "The password has been changed successfully"
