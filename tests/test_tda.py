import pytest

from indykite_sdk.indykite.tda.v1beta1 import trusted_data_access_api_pb2 as pb2
from indykite_sdk.model.data_access import DataAccessResponse, ListConsentsResponse
from indykite_sdk.indykite.knowledge.objects.v1beta1 import ikg_pb2 as objects
from indykite_sdk.tda import DataAccessClient
from helpers import data, api_requests


@pytest.fixture
def client():
    return DataAccessClient()


def test_grant_consent_success(client):
    user_id = data.get_identity_node_consent()
    consent_id = data.get_consent_config_node_id()
    validity_period = 86400
    user = {"user_id": user_id}

    def mocked_grant_consent(request: pb2.GrantConsentRequest):
        assert request.user == user
        assert request.consent_id == consent_id
        assert request.validity_period == validity_period
        return pb2.GrantConsentResponse()

    client.stub.GrantConsent = mocked_grant_consent
    response = client.grant_consent(user, consent_id, validity_period)
    assert response is not None


def test_grant_consent_empty(client):
    user_id = data.get_identity_node_consent()
    consent_id = data.get_consent_config_node_id()
    validity_period = 86400
    user = {"user_id": user_id}

    def mocked_grant_consent(request: pb2.GrantConsentRequest):
        return None

    client.stub.GrantConsent = mocked_grant_consent
    response = client.grant_consent(user, consent_id, validity_period)
    assert response is None


def test_grant_consent_fail_invalid_user_id(client, capsys):
    user_id = "gid:AAAAFJ6iGHyG8Ee8tIvW7DQ1hkE"
    consent_id = data.get_consent_config_node_id()
    validity_period = 86400
    user = {"user_id": user_id}

    consent = client.grant_consent(user, consent_id, validity_period)
    captured = capsys.readouterr()
    assert "INVALID_ARGUMENT" in captured.err


def test_list_consents_success(client):
    user_id = data.get_identity_node_consent()
    user = {"user_id": user_id}
    application_id = data.get_application_id()
    consents = client.list_consents(user, application_id)
    assert isinstance(consents, ListConsentsResponse)


def test_list_consents_no_user(client, capsys):
    application_id = data.get_application_id()
    consents = client.list_consents(["bbbb"], application_id)
    captured = capsys.readouterr()
    assert "invalid ListConsentsRequest.User: value is required" in captured.err


def test_list_consents_wrong_user(client, capsys):
    user_id = "gid:AAAAFJ6iGHyG8Ee8tIvW7DQ1hkE"
    user = {"user_id": user_id}
    application_id = data.get_application_id()

    consent = client.list_consents(user, application_id)
    captured = capsys.readouterr()
    assert "INVALID_ARGUMENT" in captured.err


def test_list_consents_empty(client):
    user_id = data.get_identity_node_consent()
    user = {"user_id": user_id}
    application_id = data.get_application_id()

    def mocked_list_consents(request: pb2.ListConsentsRequest):
        return None

    client.stub.ListConsents = mocked_list_consents
    consent = client.list_consents(user, application_id)
    assert consent is None


def test_revoke_consent_success(client):
    user_id = data.get_identity_node_consent()
    consent_id = data.get_consent_config_node_id()
    user = {"user_id": user_id}

    def mocked_revoke_consent(request: pb2.RevokeConsentRequest):
        assert request.user == user
        assert request.consent_id == consent_id
        return pb2.RevokeConsentResponse()

    client.stub.RevokeConsent = mocked_revoke_consent
    response = client.revoke_consent(user, consent_id)
    assert response is not None


def test_revoke_consent_empty(client):
    user_id = data.get_identity_node_consent()
    consent_id = data.get_consent_config_node_id()
    user = {"user_id": user_id}

    def mocked_revoke_consent(request: pb2.RevokeConsentRequest):
        return None

    client.stub.RevokeConsent = mocked_revoke_consent
    response = client.revoke_consent(user, consent_id)
    assert response is None


def test_revoke_consent_fail_invalid_user_id(client, capsys):
    user_id = "gid:AAAAFJ6iGHyG8Ee8tIvW7DQ1hkE"
    consent_id = data.get_consent_config_node_id()
    user = {"user_id": user_id}

    consent = client.revoke_consent(user, consent_id)
    captured = capsys.readouterr()
    assert "INVALID_ARGUMENT" in captured.err


def test_data_access_success(client):
    user_id = data.get_identity_node_consent()
    user = {"user_id": user_id}
    application_id = data.get_application_id()
    consent_id = data.get_consent_config_node_id()
    nodes = client.data_access(consent_id, application_id, user)
    assert isinstance(nodes, DataAccessResponse)


def test_data_access_external_id_success(client):
    user = {"external_id": {"external_id": "AVySECNxRkUSNrt", "type": "Person"}}
    application_id = data.get_application_id()
    consent_id = data.get_consent_config_node_id()
    nodes = client.data_access(consent_id, application_id, user)
    assert isinstance(nodes, DataAccessResponse)


def test_data_access_no_user(client, capsys):
    user = {}
    application_id = data.get_application_id()
    consent_id = data.get_consent_config_node_id()
    nodes = client.data_access(consent_id, application_id, user)
    captured = capsys.readouterr()
    assert "ERROR" in captured.err


def test_data_access_wrong_user(client, capsys):
    user_id = "gid:AAAAFJ6iGHyG8Ee8tIvW7DQ1hkE"
    user = {"user_id": user_id}
    application_id = data.get_application_id()
    consent_id = data.get_consent_config_node_id()
    nodes = client.data_access(consent_id, application_id, user)
    captured = capsys.readouterr()
    assert "INVALID_ARGUMENT" in captured.err


def test_data_access_external_id_wrong_user(client, capsys):
    user = {"external_id": data.get_identity_node_external_id()}
    application_id = data.get_application_id()
    consent_id = data.get_consent_config_node_id()
    nodes = client.data_access(consent_id, application_id, user)
    captured = capsys.readouterr()
    assert "should be a dictionary" in captured.err


def test_data_access_property_wrong_user(client, capsys):
    user = {"property": "last_name"}
    application_id = data.get_application_id()
    consent_id = data.get_consent_config_node_id()
    nodes = client.data_access(consent_id, application_id, user)
    captured = capsys.readouterr()
    assert "should be a dictionary" in captured.err


def test_data_access_other_wrong_user(client, capsys):
    user = {"other": "last_name"}
    application_id = data.get_application_id()
    consent_id = data.get_consent_config_node_id()
    nodes = client.data_access(consent_id, application_id, user)
    captured = capsys.readouterr()
    assert "Key should be" in captured.err


def test_data_access_empty(client):
    user_id = data.get_identity_node_consent()
    user = {"user_id": user_id}
    application_id = data.get_application_id()
    consent_id = data.get_consent_config_node_id()
    nodes = client.data_access(consent_id, application_id, user)

    def mocked_data_access(request: pb2.DataAccessRequest):
        return None

    client.stub.DataAccess = mocked_data_access
    consent = client.data_access(consent_id, application_id, user)

    assert consent is None
