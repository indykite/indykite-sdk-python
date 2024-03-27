import json
from indykite_sdk.indykite.trusted_data.access.v1beta1 import trusted_data_access_api_pb2 as pb2
from indykite_sdk.trusted_data.access import TrustedDataAccessClient
from helpers import data


def test_grant_consent_by_id_success():
    client = TrustedDataAccessClient()
    assert client is not None

    user_id = data.get_identity_node()
    consent_id = data.get_consent_config_node_id()
    revoke_after_use = False

    def mocked_grant_consent(request: pb2.GrantConsentRequest):
        assert request.user_id == user_id
        return pb2.GrantConsentResponse()

    client.stub.GrantConsent = mocked_grant_consent
    response = client.grant_consent_by_id(user_id, consent_id,revoke_after_use)

    assert response is not None
    assert isinstance(response, pb2.GrantConsentResponse)


def test_grant_consent_by_id_empty():
    client = TrustedDataAccessClient()
    assert client is not None

    user_id = data.get_identity_node()
    consent_id = data.get_consent_config_node_id()
    revoke_after_use = False

    def mocked_grant_consent(request: pb2.GrantConsentRequest):
        return None

    client.stub.GrantConsent = mocked_grant_consent
    response = client.grant_consent_by_id(user_id, consent_id,revoke_after_use)

    assert response is None


def test_grant_consent_by_id_already_exists(capsys):
    client = TrustedDataAccessClient()
    assert client is not None

    user_id = data.get_identity_node()
    consent_id = data.get_consent_config_node_id()
    revoke_after_use = False

    response = client.grant_consent_by_id(user_id, consent_id, revoke_after_use)
    captured = capsys.readouterr()
    assert "consent for this user and consent combination already exists" in captured.err


def test_grant_consent_by_id_fail_invalid_consent_id(capsys):
    client = TrustedDataAccessClient()
    assert client is not None

    user_id = data.get_identity_node()
    consent_id = "gid:AAAAFJ6iGHyG8Ee8tIvW7DQ1hkE"
    revoke_after_use = False

    consent = client.grant_consent_by_id(user_id, consent_id, revoke_after_use)
    captured = capsys.readouterr()
    assert "invalid consent identifier" in captured.err


def test_grant_consent_by_token_success():
    client = TrustedDataAccessClient()
    assert client is not None

    user_token = data.get_verification_bearer()
    consent_id = data.get_consent_config_node_id()
    revoke_after_use = False

    def mocked_grant_consent(request: pb2.GrantConsentRequest):
        assert request.user_token == user_token
        return pb2.GrantConsentResponse()

    client.stub.GrantConsent = mocked_grant_consent
    response = client.grant_consent_by_id(user_token, consent_id,revoke_after_use)

    assert response is not None
    assert isinstance(response, pb2.GrantConsentResponse)


def test_grant_consent_by_token_empty():
    client = TrustedDataAccessClient()
    assert client is not None

    user_token = data.get_verification_bearer()
    consent_id = data.get_consent_config_node_id()
    revoke_after_use = False

    def mocked_grant_consent(request: pb2.GrantConsentRequest):
        return None

    client.stub.GrantConsent = mocked_grant_consent
    response = client.grant_consent_by_id(user_token, consent_id,revoke_after_use)

    assert response is None


def test_grant_consent_by_token_already_exists(capsys):
    client = TrustedDataAccessClient()
    assert client is not None

    user_token = data.get_verification_bearer()
    consent_id = data.get_consent_config_node_id()
    revoke_after_use = False

    response = client.grant_consent_by_id(user_token, consent_id, revoke_after_use)
    captured = capsys.readouterr()
    assert "consent for this user and consent combination already exists" in captured.err


def test_grant_consent_by_token_fail_invalid_consent_id(capsys):
    client = TrustedDataAccessClient()
    assert client is not None

    user_token = data.get_verification_bearer()
    consent_id = "gid:AAAAFJ6iGHyG8Ee8tIvW7DQ1hkE"
    revoke_after_use = False

    consent = client.grant_consent_by_id(user_token, consent_id, revoke_after_use)
    captured = capsys.readouterr()
    assert "invalid consent identifier" in captured.err


def test_revoke_consent_by_id_success():
    client = TrustedDataAccessClient()
    assert client is not None

    user_id = data.get_identity_node()
    consent_id = data.get_consent_config_node_id()

    def mocked_revoke_consent(request: pb2.RevokeConsentRequest):
        assert request.user_id == user_id
        return pb2.RevokeConsentResponse()

    client.stub.RevokeConsent = mocked_revoke_consent
    response = client.revoke_consent_by_id(user_id, consent_id)

    assert response is not None
    assert isinstance(response, pb2.RevokeConsentResponse)


def test_revoke_consent_by_id_empty():
    client = TrustedDataAccessClient()
    assert client is not None

    user_id = data.get_identity_node()
    consent_id = data.get_consent_config_node_id()

    def mocked_revoke_consent(request: pb2.RevokeConsentRequest):
        return None

    client.stub.RevokeConsent = mocked_revoke_consent
    response = client.revoke_consent_by_id(user_id, consent_id)

    assert response is None


def test_revoke_consent_by_id_invalid_consent_id(capsys):
    client = TrustedDataAccessClient()
    assert client is not None

    user_id = data.get_identity_node()
    consent_id = "gid:AAAAFJ6iGHyG8Ee8tIvW7DQ1hkE"

    consent = client.revoke_consent_by_id(user_id, consent_id)
    captured = capsys.readouterr()
    assert "invalid consent identifier" in captured.err


def test_revoke_consent_by_token_success():
    client = TrustedDataAccessClient()
    assert client is not None

    user_token = data.get_verification_bearer()
    consent_id = data.get_consent_config_node_id()

    def mocked_revoke_consent(request: pb2.RevokeConsentRequest):
        assert request.user_token == user_token
        return pb2.RevokeConsentResponse()

    client.stub.RevokeConsent = mocked_revoke_consent
    response = client.revoke_consent_by_id(user_token, consent_id)

    assert response is not None
    assert isinstance(response, pb2.RevokeConsentResponse)


def test_revoke_consent_by_token_empty():
    client = TrustedDataAccessClient()
    assert client is not None

    user_token = data.get_verification_bearer()
    consent_id = data.get_consent_config_node_id()

    def mocked_revoke_consent(request: pb2.RevokeConsentRequest):
        return None

    client.stub.RevokeConsent = mocked_revoke_consent
    response = client.revoke_consent_by_id(user_token, consent_id)

    assert response is None


def test_revoke_consent_by_token_invalid_consent_id(capsys):
    client = TrustedDataAccessClient()
    assert client is not None

    user_token = data.get_verification_bearer()
    consent_id = "gid:AAAAFJ6iGHyG8Ee8tIvW7DQ1hkE"

    consent = client.revoke_consent_by_id(user_token, consent_id)
    captured = capsys.readouterr()
    assert "invalid consent identifier" in captured.err


def test_access_consented_data_success():
    client = TrustedDataAccessClient()
    assert client is not None

    consent_id = data.get_consent_config_node_id()
    user_id = data.get_identity_node()

    def mocked_access_consented_data(request: pb2.AccessConsentedDataRequest):
        assert request.user_id == user_id
        assert request.consent_id == consent_id
        return pb2.AccessConsentedDataResponse()

    client.stub.AccessConsentedData = mocked_access_consented_data
    response = client.access_consented_data(consent_id, user_id)

    assert response is not None
    assert isinstance(response, pb2.AccessConsentedDataResponse)


def test_access_consented_data_empty():
    client = TrustedDataAccessClient()
    assert client is not None

    consent_id = data.get_consent_config_node_id()
    user_id = data.get_identity_node()

    def mocked_access_consented_data(request: pb2.GrantConsentRequest):
        return None

    client.stub.GrantConsent = mocked_access_consented_data
    response = client.access_consented_data(consent_id,user_id)

    assert response is None


def test_grant_access_consented_data_invalid_consent_id(capsys):
    client = TrustedDataAccessClient()
    assert client is not None

    consent_id = "gid:AAAAFJ6iGHyG8Ee8tIvW7DQ1hkE"
    user_id = data.get_identity_node()

    consent = client.access_consented_data(consent_id, user_id)
    captured = capsys.readouterr()
    assert "invalid consent identifier" in captured.err
