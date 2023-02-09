from indykite_sdk.identity import IdentityClient
from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
from helpers import data
from helpers import api_requests


def test_change_password_short_token(capsys):
    token = "short_token"
    password = data.get_new_password()

    client = IdentityClient()
    assert client is not None

    response = client.change_password(token, password)
    captured = capsys.readouterr()

    assert "Token must be 32 chars or more" in captured.err


def test_change_password_expired_token(capsys):
    token = data.get_expired_token()
    password = data.get_new_password()

    client = IdentityClient()
    assert client is not None

    response = client.change_password(token, password)
    captured = capsys.readouterr()

    assert "invalid or expired access_token" in captured.err


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
    digital_twin_id = api_requests.generate_random_gid()
    tenant_id = data.get_tenant()
    password = data.get_new_password()

    client = IdentityClient()
    assert client is not None

    response = client.change_password_of_user(digital_twin_id, tenant_id, password)
    captured = capsys.readouterr()

    assert "id is not valid DigitalTwin identifier" in captured.err


def test_password_of_user_wrong_tenant_id(capsys):
    digital_twin_id = api_requests.generate_random_gid()
    tenant_id = "gid:AAAAD1DBxqIze0UniM-vaogDx6Y"
    password = data.get_new_password()

    client = IdentityClient()
    assert client is not None

    response = client.change_password_of_user(digital_twin_id, tenant_id, password)
    captured = capsys.readouterr()

    assert "id is not valid DigitalTwin identifier" in captured.err


def test_password_of_user_nonexisting_twin_id(capsys):
    digital_twin_id = api_requests.generate_random_gid()
    tenant_id = data.get_tenant()
    password = data.get_new_password()

    client = IdentityClient()
    assert client is not None

    response = client.change_password_of_user(digital_twin_id, tenant_id, password)
    captured = capsys.readouterr()

    assert "id is not valid DigitalTwin identifier" in captured.err


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
