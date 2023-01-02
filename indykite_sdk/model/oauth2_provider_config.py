from indykite_sdk.indykite.config.v1beta1.model_pb2 import OAuth2ProviderConfig, GrantType, ResponseType, TokenEndpointAuthMethod
from google.protobuf.json_format import MessageToDict


class OAuth2ProviderConfig:
    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None

        oauth2_client_config = OAuth2ProviderConfig(
            list(GrantType(message_config.grant_types)),
            list(ResponseType(message_config.response_types)),
            list(message_config.scopes),
            list(TokenEndpointAuthMethod(message_config.token_endpoint_auth_method)),
            list(message_config.token_endpoint_auth_signing_alg),
            MessageToDict(message_config.front_channel_login_uri),
            MessageToDict(message_config.front_channel_consent_uri)
        )
        if message_config.HasField('request_uris'):
            oauth2_client_config.request_uris = list(message_config.request_uris)

        if message_config.HasField('request_object_signing_alg'):
            oauth2_client_config.request_object_signing_alg = message_config.request_object_signing_alg

        return oauth2_client_config

    def __init__(self,
                 grant_types,
                 response_types,
                 scopes,
                 token_endpoint_auth_method,
                 token_endpoint_auth_signing_alg,
                 front_channel_login_uri,
                 front_channel_consent_uri):

        self.grant_types = grant_types
        self.response_types = response_types
        self.scopes = scopes
        self.token_endpoint_auth_method = token_endpoint_auth_method
        self.token_endpoint_auth_signing_alg = token_endpoint_auth_signing_alg
        self.front_channel_login_uri = front_channel_login_uri
        self.front_channel_consent_uri = front_channel_consent_uri
        self.request_uris = None
        self.request_object_signing_alg = None
