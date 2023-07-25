import json
from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
from indykite_sdk.identity import IdentityClient
from indykite_sdk.model.consent import CreateConsentResponse
from indykite_sdk.indykite.identity.v1beta2 import consent_pb2
from helpers import data, api_requests


def test_create_consent_success():
    client = IdentityClient()
    assert client is not None

    pii_processor_id = data.get_oauth2_application_id()
    pii_principal_id = data.get_digital_twin()
    properties = ["property_name"]

    def mocked_create_consent(request: pb2.CreateConsentRequest):
        assert request.pii_principal_id == pii_principal_id
        return pb2.CreateConsentResponse()

    client.stub.CreateConsent = mocked_create_consent
    response = client.create_consent(pii_processor_id, pii_principal_id, properties)

    assert response is not None
    assert isinstance(response, CreateConsentResponse)


def test_create_consent_empty():
    client = IdentityClient()
    assert client is not None

    pii_processor_id = data.get_oauth2_application_id()
    pii_principal_id = data.get_digital_twin()
    properties = ["property_name"]

    def mocked_create_consent(request: pb2.CreateConsentRequest):
        return None

    client.stub.CreateConsent = mocked_create_consent
    response = client.create_consent(pii_processor_id, pii_principal_id, properties)

    assert response is None


def test_create_consent_already_exists(capsys):
    client = IdentityClient()
    assert client is not None

    pii_processor_id = data.get_oauth2_application_id()
    pii_principal_id = "gid:AAAAFXRNmDlB-k18rx7iBXJlEos"
    properties = ["property_name"]

    response = client.create_consent(pii_processor_id, pii_principal_id, properties)
    captured = capsys.readouterr()
    assert "consent for this PiiProcessor and PiiPrincipal combination already exist" in captured.err


def test_create_consent_fail_invalid_pii_processor_id(capsys):
    client = IdentityClient()
    assert client is not None

    pii_processor_id = "gid:AAAAFJ6iGHyG8Ee8tIvW7DQ1hkE"
    pii_principal_id = "gid:AAAAFJ6iGHyG8Ee8tIvW7DQ1hkE"
    properties = ["property_name"]

    consent = client.create_consent(pii_processor_id, pii_principal_id, properties)
    captured = capsys.readouterr()
    assert "invalid pii processor identifier" in captured.err


def test_consent_list_success():
    client = IdentityClient()
    assert client is not None

    pii_principal_id = data.get_digital_twin_consent()

    consent = client.list_consents(pii_principal_id)

    assert consent is not None
    for c in consent:
        assert isinstance(c.consent_receipt, consent_pb2.ConsentReceipt)


def test_consent_list_no_pii(capsys):
    client = IdentityClient()
    assert client is not None

    consent = client.list_consents(["bbbb"])
    captured = capsys.readouterr()
    assert "bad argument" in captured.err


def test_consent_list_wrong_pii(capsys):
    client = IdentityClient()
    assert client is not None

    pii_principal_id = "gid:AAAAFJ6iGHyG8Ee8tIvW7DQ1hkE"

    consent = client.list_consents(pii_principal_id)
    captured = capsys.readouterr()
    assert "invalid pii principal" in captured.err


def test_consent_list_empty():
    client = IdentityClient()
    assert client is not None

    pii_principal_id = data.get_digital_twin()

    def mocked_list_consents(request: pb2.ListConsentsRequest):
        return None

    client.stub.ListConsents = mocked_list_consents
    consent = client.list_consents(pii_principal_id)

    assert consent is None


def test_revoke_consent_success(capsys):
    client = IdentityClient()
    assert client is not None

    pii_principal_id = data.get_digital_twin()
    consent_ids = ["f42db2b3-b9ed-49c3-bdee-5077d2dcdda2"]

    def mocked_revoke_consent(request: pb2.RevokeConsentRequest):
        assert request.pii_principal_id == pii_principal_id
        assert request.consent_ids == consent_ids
        return pb2.RevokeConsentResponse()

    client.stub.RevokeConsent = mocked_revoke_consent
    consent_response = client.revoke_consent(pii_principal_id, consent_ids)

    assert consent_response is not None


def test_revoke_consent_wrong_consent_id(capsys):
    client = IdentityClient()
    assert client is not None

    pii_principal_id = data.get_digital_twin()
    consent_ids = ["f414b2b3-b9ed-49c3-b754e-5077d2dcdda2"]
    consent_response = client.revoke_consent(pii_principal_id, consent_ids)
    captured = capsys.readouterr()
    assert "invalid RevokeConsentRequest.ConsentIds" in captured.err


def test_revoke_consent_empty():
    client = IdentityClient()
    assert client is not None

    pii_principal_id = data.get_digital_twin()
    consent_ids = ["f42db2b3-b9ed-49c3-bdee-5077d2dcdda2"]

    def mocked_revoke_consent(request: pb2.RevokeConsentRequest):
        return None

    client.stub.RevokeConsent = mocked_revoke_consent
    consent_response = client.revoke_consent(pii_principal_id, consent_ids)

    assert consent_response is None


def test_check_challenge_success(capsys):
    client = IdentityClient()
    assert client is not None

    challenge = "AjEdsU2PQHuMZVV8Ruz2sQ"
    client_id = api_requests.generate_random_gid()
    scopes = [pb2.ScopeItem(name="openid", display_name="", description="", required=False)]
    request_url = "http://www.example.com/oauth"
    audiences = [pb2.AudienceItem(
        user_support_email_address="support@localhost.com",
        client_id="bf48ee66-49bf-414a-829c-e2463802a71e",
        display_name="Consent page"
    )]
    app_space_id = api_requests.generate_random_gid()
    acrs = []
    subject_identifier = "Subject"
    skip = False

    def mocked_check_challenge(request: pb2.CheckOAuth2ConsentChallengeRequest):
        assert request.challenge == challenge
        return pb2.CheckOAuth2ConsentChallengeResponse(
            client_id=client_id,
            app_space_id=app_space_id,
            audiences=audiences,
            scopes=scopes,
            acrs=acrs,
            request_url=request_url,
            skip=skip,
            subject_identifier=subject_identifier
        )

    client.stub.CheckOAuth2ConsentChallenge = mocked_check_challenge
    consent_response = client.check_oauth2_consent_challenge(challenge)

    assert consent_response.client_id == client_id


def test_check_challenge_empty(capsys):
    client = IdentityClient()
    assert client is not None
    challenge = "AjEdsU2PQHuMZVV8Ruz2sQ"

    def mocked_check_challenge(request: pb2.CheckOAuth2ConsentChallengeRequest):
        assert request.challenge == challenge
        return None

    client.stub.CheckOAuth2ConsentChallenge = mocked_check_challenge
    consent_response = client.check_oauth2_consent_challenge(challenge)

    assert consent_response is None


def test_check_challenge_exception(capsys):
    client = IdentityClient()
    assert client is not None

    challenge = "BBB"
    consent_response = client.check_oauth2_consent_challenge(challenge)
    captured = capsys.readouterr()
    assert "invalid CheckOAuth2ConsentChallengeRequest.Challenge" in captured.err


def test_consent_verifier_approval_success(capsys):
    client = IdentityClient()
    assert client is not None

    consent_challenge = "AjEdsU2PQHuMZVV8Ruz2sQ"
    verifier = "2qNSyff7ToarEwv_sw3EXQ"
    authorization_endpoint = "https://www.indykite.com/o/oauth2/endpoint"

    def mocked_consent_verifier_approval(request: pb2.CreateOAuth2ConsentVerifierRequest):
        assert request.consent_challenge == consent_challenge
        return pb2.CreateOAuth2ConsentVerifierResponse(
            verifier=verifier,
            authorization_endpoint=authorization_endpoint
        )

    client.stub.CreateOAuth2ConsentVerifier = mocked_consent_verifier_approval
    consent_response = client.create_oauth2_consent_verifier_approval(consent_challenge)
    assert consent_response.verifier == verifier


def test_consent_verifier_approval_empty(capsys):
    client = IdentityClient()
    assert client is not None
    consent_challenge = "AjEdsU2PQHuMZVV8Ruz2sQ"

    def mocked_consent_verifier_approval(request: pb2.CreateOAuth2ConsentVerifierRequest):
        assert request.consent_challenge == consent_challenge
        return None

    client.stub.CreateOAuth2ConsentVerifier = mocked_consent_verifier_approval
    consent_response = client.create_oauth2_consent_verifier_approval(consent_challenge)
    assert consent_response is None


def test_consent_verifier_approval_exception(capsys):
    client = IdentityClient()
    assert client is not None

    consent_challenge = "BBB"
    consent_response = client.create_oauth2_consent_verifier_approval(consent_challenge)
    captured = capsys.readouterr()
    assert "invalid CreateOAuth2ConsentVerifierRequest.ConsentChallenge" in captured.err


def test_consent_verifier_denial_success(capsys):
    client = IdentityClient()
    assert client is not None

    consent_challenge = "AjEdsU2PQHuMZVV8Ruz2sQ"
    verifier = "2qNSyff7ToarEwv_sw3EXQ"
    authorization_endpoint = "https://www.indykite.com/o/oauth2/endpoint"

    def mocked_consent_verifier_denial(request: pb2.CreateOAuth2ConsentVerifierRequest):
        assert request.consent_challenge == consent_challenge
        return pb2.CreateOAuth2ConsentVerifierResponse(
            verifier=verifier,
            authorization_endpoint=authorization_endpoint
        )

    client.stub.CreateOAuth2ConsentVerifier = mocked_consent_verifier_denial
    consent_response = client.create_oauth2_consent_verifier_denial(consent_challenge)
    assert consent_response.verifier == verifier


def test_consent_verifier_denial_empty(capsys):
    client = IdentityClient()
    assert client is not None
    consent_challenge = "AjEdsU2PQHuMZVV8Ruz2sQ"

    def mocked_consent_verifier_denial(request: pb2.CreateOAuth2ConsentVerifierRequest):
        assert request.consent_challenge == consent_challenge
        return None

    client.stub.CreateOAuth2ConsentVerifier = mocked_consent_verifier_denial
    consent_response = client.create_oauth2_consent_verifier_denial(consent_challenge)
    assert consent_response is None


def test_consent_verifier_denial_exception(capsys):
    client = IdentityClient()
    assert client is not None

    consent_challenge = "BBB"
    consent_response = client.create_oauth2_consent_verifier_denial(consent_challenge)
    captured = capsys.readouterr()
    assert "invalid CreateOAuth2ConsentVerifierRequest.ConsentChallenge" in captured.err
