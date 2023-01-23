import time

from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
from indykite_sdk.identity import IdentityClient
from indykite_sdk.model.consent import CreateConsentResponse
from indykite_sdk.indykite.identity.v1beta2 import consent_pb2
from helpers import data


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
    assert isinstance(response, pb2.CreateConsentResponse)


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
    pii_principal_id = "gid:AAAAFc-ZvSrJlE8GsTHI1WtxFqY"
    properties = ["property_name"]

    response = client.create_consent(pii_processor_id, pii_principal_id, properties)
    captured = capsys.readouterr()

    assert "consent for this PiiProcessor and PiiPrincipal combination already exist" in captured.out


def test_create_consent_fail_invalid_pii_processor_id(capsys):
    client = IdentityClient()
    assert client is not None

    pii_processor_id = "gid:AAAAFJ6iGHyG8Ee8tIvW7DQ1hkE"
    pii_principal_id = "gid:AAAAFJ6iGHyG8Ee8tIvW7DQ1hkE"
    properties = ["property_name"]

    consent = client.create_consent(pii_processor_id, pii_principal_id, properties)
    captured = capsys.readouterr()

    assert consent is None
    assert "invalid pii processor identifier" in captured.out


def test_consent_list_success():
    client = IdentityClient()
    assert client is not None

    pii_principal_id = data.get_digital_twin()

    consent = client.list_consents(pii_principal_id)

    assert consent is not None
    for c in consent:
        print(c.consent_receipt)
        assert isinstance(c.consent_receipt, consent_pb2.ConsentReceipt)


def test_consent_list_no_pii():
    client = IdentityClient()
    assert client is not None

    consent = client.list_consents(["bbbb"])
    assert consent is None


def test_consent_list_wrong_pii(capsys):
    client = IdentityClient()
    assert client is not None

    pii_principal_id = "gid:AAAAFJ6iGHyG8Ee8tIvW7DQ1hkE"

    consent = client.list_consents(pii_principal_id)
    captured = capsys.readouterr()

    assert consent is None
    assert "invalid pii principal" in captured.out



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


def test_revoke_consent_wrong_consent_id():
    client = IdentityClient()
    assert client is not None

    pii_principal_id = data.get_digital_twin()
    consent_ids = ["f414b2b3-b9ed-49c3-b754e-5077d2dcdda2"]
    consent_response = client.revoke_consent(pii_principal_id, consent_ids)
    assert consent_response is None


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
