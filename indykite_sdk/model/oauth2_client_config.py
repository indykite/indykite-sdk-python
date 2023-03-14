class OAuth2ClientConfig:
    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None
        fields = [desc.name for desc, val in message_config.ListFields()]

        oauth2_client_config = OAuth2ClientConfig(
            str(message_config.provider_type),
            str(message_config.client_id),
            str(message_config.client_secret),
            list(message_config.redirect_uri)
        )
        if "default_scopes" in fields:
            oauth2_client_config.default_scopes = list(message_config.default_scopes)

        if "allowed_scopes" in fields:
            oauth2_client_config.allowed_scopes = list(message_config.allowed_scopes)

        if "allow_signup" in fields:
            oauth2_client_config.allow_signup = bool(message_config.allow_signup)

        if "issuer" in fields:
            oauth2_client_config.issuer = str(message_config.issuer)

        if "authorization_endpoint" in fields:
            oauth2_client_config.authorization_endpoint = str(message_config.authorization_endpoint)

        if "token_endpoint" in fields:
            oauth2_client_config.token_endpoint = str(message_config.token_endpoint)

        if "discovery_url" in fields:
            oauth2_client_config.discovery_url = str(message_config.discovery_url)

        if "userinfo_endpoint" in fields:
            oauth2_client_config.userinfo_endpoint = str(message_config.userinfo_endpoint)

        if "jwks_uri" in fields:
            oauth2_client_config.jwks_uri = str(message_config.jwks_uri)

        if "image_url" in fields:
            oauth2_client_config.image_url = str(message_config.image_url)

        if "tenant" in fields:
            oauth2_client_config.tenant = str(message_config.tenant)

        if "hosted_domain" in fields:
            oauth2_client_config.hosted_domain = str(message_config.hosted_domain)

        if "auth_style" in fields:
            oauth2_client_config.auth_style = str(message_config.auth_style)

        if "private_key_pem" in fields:
            oauth2_client_config.private_key_pem = str(bytes=message_config.private_key_pem)

        if "private_key_id" in fields:
            oauth2_client_config.private_key_id = str(message_config.private_key_id)

        if "team_id" in fields:
            oauth2_client_config.team_id = str(message_config.team_id)

        return oauth2_client_config

    def __init__(self, provider_type, client_id, client_secret, redirect_uri):

        self.provider_type = provider_type
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.default_scopes = None
        self.allowed_scopes = None
        self.allow_signup = None
        self.issuer = None
        self.authorization_endpoint = None
        self.token_endpoint = None
        self.discovery_url = None
        self.userinfo_endpoint = None
        self.jwks_uri = None
        self.image_url = None
        self.tenant = None
        self.hosted_domain = None
        self.auth_style = None
        self.private_key_pem = None
        self.private_key_id = None
        self.team_id = None



