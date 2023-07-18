from indykite_sdk.identity import IdentityClient
from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
from indykite_sdk.indykite.identity.v1beta2 import model_pb2 as model
from indykite_sdk.indykite.identity.v1beta2.import_pb2 import CredentialReference
import os


def test_create_custom_login_token_error(capsys):
    client = IdentityClient()
    assert client is not None
    digital_twin = model.DigitalTwin(
        id=str("ANYTHING"),
        tenant_id=str(os.getenv('ANYTHING'))
    )

    def mocked_create_custom_login_token_error(request: pb2.CreateCustomLoginTokenRequest):
        raise Exception("something went wrong")

    client.stub.CreateCustomLoginToken = mocked_create_custom_login_token_error

    response = client.create_custom_login_token(digital_twin, None, None)
    captured = capsys.readouterr()
    assert "something went wrong" in captured.err


def test_create_custom_login_token():
    digital_twin = model.DigitalTwin(
        id=str(os.getenv('DIGITAL_TWIN')),
        tenant_id=str(os.getenv('TENANT_ID'))
    )
    client = IdentityClient()
    assert client is not None

    def mocked_create_custom_login_token(request: pb2.CreateCustomLoginTokenRequest):
        assert request.digital_twin == digital_twin
        return pb2.CreateCustomLoginTokenResponse()

    client.stub.CreateCustomLoginToken = mocked_create_custom_login_token
    response = client.create_custom_login_token(digital_twin, {"t_claim": "test"}, {"s_claim": "test"})

    assert response is not None


def test_create_custom_login_token_credential():
    credential_reference = CredentialReference(
        provider_id=str(os.getenv('OAUTH2_PROVIDER')),
        uid=str("unique_identifier")
    )
    client = IdentityClient()
    assert client is not None

    def mocked_create_custom_login_token(request: pb2.CreateCustomLoginTokenRequest):
        assert request.credential_reference == credential_reference
        return pb2.CreateCustomLoginTokenResponse()

    client.stub.CreateCustomLoginToken = mocked_create_custom_login_token
    response = client.create_custom_login_token(credential_reference, {"t_claim": "test"}, {"s_claim": "test"})

    assert response is not None


def test_create_custom_login_token_property():
    client = IdentityClient()
    assert client is not None
    property_filter = client.property_filter("email", "testem@example.com", os.getenv('TENANT_ID'))

    def mocked_create_custom_login_token(request: pb2.CreateCustomLoginTokenRequest):
        assert request.property_filter == property_filter
        return pb2.CreateCustomLoginTokenResponse()

    client.stub.CreateCustomLoginToken = mocked_create_custom_login_token
    response = client.create_custom_login_token(property_filter, {"t_claim": "test"}, {"s_claim": "test"})

    assert response is not None
