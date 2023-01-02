from indykite_sdk.identity import IdentityClient
from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2


def test_enrich_token_error():
    client = IdentityClient()
    assert client is not None

    def mocked_enrich_token_error(request: pb2.EnrichTokenRequest):
        raise Exception("something went wrong")

    client.stub.EnrichToken = mocked_enrich_token_error

    response = client.enrich_token("mocked-token", None, None)

    assert response is None


def test_enrich_token():
    token = "mocked-token"
    client = IdentityClient()
    assert client is not None

    def mocked_enrich_token(request: pb2.EnrichTokenRequest):
        assert request.access_token == token
        return pb2.EnrichTokenResponse()

    client.stub.EnrichToken = mocked_enrich_token

    response = client.enrich_token(token, {"t_claim": "test"}, {"s_claim": "test"})

    assert response is not None
