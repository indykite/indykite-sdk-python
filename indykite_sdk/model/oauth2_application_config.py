from indykite_sdk.indykite.config.v1beta1.model_pb2 import OAuth2ApplicationConfig, GrantType, ResponseType, ClientSubjectType, TokenEndpointAuthMethod


class OAuth2ApplicationConfig:
    @classmethod
    def deserialize(cls, message_config):
        if message_config is None:
            return None

        oauth2_application_config = OAuth2ApplicationConfig(
            str(message_config.display_name),
            list(str(message_config.redirect_uris)),
            str(message_config.owner),
            str(message_config.policy_uri),
            str(message_config.terms_of_service_uri),
            str(message_config.client_uri),
            str(message_config.logo_uri),
            str(message_config.user_support_email_address),
            ClientSubjectType(message_config.subject_type),
            list(str(message_config.scopes)),
            TokenEndpointAuthMethod(message_config.token_endpoint_auth_method),
            str(message_config.token_endpoint_auth_signing_alg)
        )
        if message_config.HasField('client_id'):
            oauth2_application_config.client_id = str(message_config.client_id)

        if message_config.HasField('description'):
            oauth2_application_config.description = str(message_config.description)

        if message_config.HasField('allowed_cors_origins'):
            oauth2_application_config.allowed_cors_origins = list(str(message_config.allowed_cors_origins))

        if message_config.HasField('additional_contacts'):
            oauth2_application_config.additional_contacts = list(str(message_config.additional_contacts))

        if message_config.HasField('sector_identifier_uri'):
            oauth2_application_config.sector_identifier_uri = str(message_config.sector_identifier_uri)

        if message_config.HasField('grant_types'):
            oauth2_application_config.grant_types = list(GrantType(message_config.grant_types))

        if message_config.HasField('response_types'):
            oauth2_application_config.response_types = list(ResponseType(message_config.response_types))

        if message_config.HasField('audiences'):
            oauth2_application_config.audiences = list(str(message_config.audiences))

        if message_config.HasField('userinfo_signed_response_alg'):
            oauth2_application_config.userinfo_signed_response_alg = str(message_config.userinfo_signed_response_alg)

    def __init__(self,
                 display_name,
                 redirect_uris,
                 owner,
                 policy_uri,
                 terms_of_service_uri,
                 client_uri,
                 logo_uri,
                 user_support_email_address,
                 subject_type,
                 scopes,
                 token_endpoint_auth_method,
                 token_endpoint_auth_signing_alg):

        self.display_name = display_name
        self.redirect_uris = redirect_uris
        self.owner = owner
        self.policy_uri = policy_uri
        self.terms_of_service_uri = terms_of_service_uri
        self.client_uri = client_uri
        self.logo_uri = logo_uri
        self.user_support_email_address = user_support_email_address
        self.subject_type = subject_type
        self.scopes = scopes
        self.token_endpoint_auth_method = token_endpoint_auth_method
        self.token_endpoint_auth_signing_alg = token_endpoint_auth_signing_alg
        self.client_id = None
        self.description = None
        self.allowed_cors_origins = None
        self.additional_contacts = None
        self.sector_identifier_uri = None
        self.grant_types = None
        self.response_types = None
        self.audiences = None
        self.userinfo_signed_response_alg = None

