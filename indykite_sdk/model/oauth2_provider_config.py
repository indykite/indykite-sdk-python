class OAuth2ProviderConfig:
    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None
        fields = [desc.name for desc, val in message_config.ListFields()]
        oauth2_provider_config = OAuth2ProviderConfig(
            [str(r) for r in message_config.grant_types],
            [str(r) for r in message_config.response_types],
            [str(r) for r in message_config.scopes],
            [str(r) for r in message_config.token_endpoint_auth_method],
            [str(r) for r in message_config.token_endpoint_auth_signing_alg]
        )
        if "front_channel_login_uri" in fields:
            front_channel_login_uri = {}
            for k, v in message_config.front_channel_login_uri.items():
                front_channel_login_uri[k] = v
            oauth2_provider_config.front_channel_login_uri = front_channel_login_uri

        if "front_channel_consent_uri" in fields:
            front_channel_consent_uri = {}
            for k, v in message_config.front_channel_consent_uri.items():
                front_channel_consent_uri[k] = v
            oauth2_provider_config.front_channel_consent_uri = front_channel_consent_uri

        if "request_uris" in fields:
            oauth2_provider_config.request_uris = [
                str(r)
                for r in message_config.request_uris
            ]

        if "request_object_signing_alg" in fields:
            oauth2_provider_config.request_object_signing_alg = [
                str(r)
                for r in message_config.request_object_signing_alg
            ]
        return oauth2_provider_config

    def __init__(self,
                 grant_types,
                 response_types,
                 scopes,
                 token_endpoint_auth_method,
                 token_endpoint_auth_signing_alg):

        self.grant_types = grant_types
        self.response_types = response_types
        self.scopes = scopes
        self.token_endpoint_auth_method = token_endpoint_auth_method
        self.token_endpoint_auth_signing_alg = token_endpoint_auth_signing_alg
        self.front_channel_login_uri = None
        self.front_channel_consent_uri = None
        self.request_uris = None
        self.request_object_signing_alg = None
