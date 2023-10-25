from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from indykite_sdk.model.create_config_node import CreateConfigNode
from indykite_sdk.model.update_config_node import UpdateConfigNode
from indykite_sdk.model.config_node import ConfigNode
from indykite_sdk.model.conveyance_preference import ConveyancePreference
from indykite_sdk.model.user_verification_requirement import UserVerificationRequirement
from indykite_sdk.model.authenticator_attachment import AuthenticatorAttachment
from indykite_sdk.model.authorization_policy_config_status import Status
from indykite_sdk.indykite.config.v1beta1 import model_pb2
import sys
import indykite_sdk.utils.logger as logger


def create_email_service_config_node(self,
                                     location,
                                     name,
                                     display_name,
                                     description,
                                     email_service_config,
                                     bookmarks=[]):
    """
    create email service
    :param self:
    :param location: string gid id
    :param name: string pattern: ^[a-z](?:[-a-z0-9]{0,61}[a-z0-9])$
    :param display_name: string
    :param description: string
    :param email_service_config: EmailServiceConfig object
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized CreateConfigNode instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.CreateConfigNode(
            pb2.CreateConfigNodeRequest(
                location=location,
                name=name,
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                email_service_config=email_service_config,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return CreateConfigNode.deserialize(response)


def read_config_node(self, config_node_id, bookmarks=[], version=0):
    """
    read a specific config node
    :param self:
    :param config_node_id: string gid id
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :param version: int
    :return: deserialized ConfigNode instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.ReadConfigNode(
            pb2.ReadConfigNodeRequest(
                id=str(config_node_id),
                bookmarks=bookmarks,
                version=version
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return ConfigNode.deserialize(response.config_node)


def update_email_service_config_node(self,
                                     config_node_id,
                                     etag,
                                     display_name,
                                     description,
                                     email_service_config,
                                     bookmarks=[]):
    """
    update email service
    :param self:
    :param config_node_id: string gid id
    :param etag: string
    :param display_name: string
    :param description: string
    :param email_service_config: EmailServiceConfig object
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized UpdateConfigNode instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.UpdateConfigNode(
            pb2.UpdateConfigNodeRequest(
                id=config_node_id,
                etag=wrappers.StringValue(value=etag),
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                email_service_config=email_service_config,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return UpdateConfigNode.deserialize(response)


def delete_config_node(self, config_node_id, etag, bookmarks=[]):
    """
    delete a specific config node
    :param self:
    :param config_node_id: string gid id
    :param etag: etag
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: DeleteConfigNodeResponse object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.DeleteConfigNode(
            pb2.DeleteConfigNodeRequest(
                id=str(config_node_id),
                etag=wrappers.StringValue(value=etag),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return response


def create_auth_flow_config_node(self,
                                 location,
                                 name,
                                 display_name,
                                 description,
                                 auth_flow_config,
                                 bookmarks=[]):
    """
    create auth flow
    :param self:
    :param location: string gid id
    :param name: string pattern: ^[a-z](?:[-a-z0-9]{0,61}[a-z0-9])$
    :param display_name: string
    :param description: string
    :param auth_flow_config: AuthFlowConfig object
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized CreateConfigNode instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.CreateConfigNode(
            pb2.CreateConfigNodeRequest(
                location=location,
                name=name,
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                auth_flow_config=auth_flow_config,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return CreateConfigNode.deserialize(response)


def update_auth_flow_config_node(self,
                                 config_node_id,
                                 etag,
                                 display_name,
                                 description,
                                 auth_flow_config,
                                 bookmarks=[]):
    """
    update auth flow
    :param self:
    :param config_node_id: string gid id
    :param etag: string
    :param display_name: string
    :param description: string
    :param auth_flow_config: AuthFlowConfig object
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized UpdateConfigNode instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.UpdateConfigNode(
            pb2.UpdateConfigNodeRequest(
                id=config_node_id,
                etag=wrappers.StringValue(value=etag),
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                auth_flow_config=auth_flow_config,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return UpdateConfigNode.deserialize(response)


def auth_flow_config(self, source_format,
                     source):
    """
    create AuthFlowConfig
    :param self:
    :param source_format: AuthFlowConfig.Format enum value
    :param source: bytes of json string
    :return:
    """
    sys.excepthook = logger.handle_excepthook
    try:
        auth_flow_config = model_pb2.AuthFlowConfig(
            source_format=source_format,
            source=bytes(source)
            )
        return auth_flow_config
    except Exception as exception:
        return logger.logger_error(exception)


def create_oauth2_client_config_node(self,
                                     location,
                                     name,
                                     display_name,
                                     description,
                                     oauth2_client_config,
                                     bookmarks=[]):
    """
    create oauth2 client
    :param self:
    :param location: string gid id
    :param name: string pattern: ^[a-z](?:[-a-z0-9]{0,61}[a-z0-9])$
    :param display_name: string
    :param description: string
    :param oauth2_client_config: OAuth2ClientConfig object
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized CreateConfigNode instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.CreateConfigNode(
            pb2.CreateConfigNodeRequest(
                location=location,
                name=name,
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                oauth2_client_config=oauth2_client_config,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return CreateConfigNode.deserialize(response)


def update_oauth2_client_config_node(self,
                                     config_node_id,
                                     etag,
                                     display_name,
                                     description,
                                     oauth2_client_config,
                                     bookmarks=[]):
    """
    update OAuth2 client
    :param self:
    :param config_node_id: string gid id
    :param etag: string
    :param display_name: string
    :param description: string
    :param oauth2_client_config: OAuth2ClientConfig object
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized UpdateConfigNode instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.UpdateConfigNode(
            pb2.UpdateConfigNodeRequest(
                id=config_node_id,
                etag=wrappers.StringValue(value=etag),
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                oauth2_client_config=oauth2_client_config,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return UpdateConfigNode.deserialize(response)


def create_webauthn_provider_config_node(self,
                                         location,
                                         name,
                                         display_name,
                                         description,
                                         webauthn_provider_config,
                                         bookmarks=[]):
    """
    create webauthn provider
    :param self:
    :param location: string gid id
    :param name: string pattern: ^[a-z](?:[-a-z0-9]{0,61}[a-z0-9])$
    :param display_name: string
    :param description: string
    :param webauthn_provider_config: WebAuthnProviderConfig object
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized CreateConfigNode instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        if webauthn_provider_config and webauthn_provider_config.attestation_preference:
            self.validate_conveyance(webauthn_provider_config.attestation_preference)
        if webauthn_provider_config and webauthn_provider_config.user_verification:
            self.validate_user_verification(webauthn_provider_config.attestation_preference)
        if webauthn_provider_config and webauthn_provider_config.authenticator_attachment:
            self.validate_authenticator_attachment(webauthn_provider_config.authenticator_attachment)

        response = self.stub.CreateConfigNode(
            pb2.CreateConfigNodeRequest(
                location=location,
                name=name,
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                webauthn_provider_config=webauthn_provider_config,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return CreateConfigNode.deserialize(response)


def update_webauthn_provider_config_node(self,
                                         config_node_id,
                                         etag,
                                         display_name,
                                         description,
                                         webauthn_provider_config,
                                         bookmarks=[]):
    """
    update webauthn provider
    :param self:
    :param config_node_id: string gid id
    :param etag: string
    :param display_name: string
    :param description: string
    :param webauthn_provider_config: WebAuthnProviderConfig object
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized UpdateConfigNode instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        if webauthn_provider_config and webauthn_provider_config.attestation_preference:
            self.validate_conveyance(webauthn_provider_config.attestation_preference)
        if webauthn_provider_config and webauthn_provider_config.user_verification:
            self.validate_user_verification(webauthn_provider_config.user_verification)
        if webauthn_provider_config and webauthn_provider_config.authenticator_attachment:
            self.validate_authenticator_attachment(webauthn_provider_config.authenticator_attachment)

        response = self.stub.UpdateConfigNode(
            pb2.UpdateConfigNodeRequest(
                id=config_node_id,
                etag=wrappers.StringValue(value=etag),
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                webauthn_provider_config=webauthn_provider_config,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return UpdateConfigNode.deserialize(response)


def webauthn_provider_config(self, relying_parties,
                             attestation_preference,
                             authenticator_attachment,
                             require_resident_key,
                             user_verification,
                             registration_timeout,
                             authentication_timeout):
    """
    create WebAuthnProviderConfig
    :param self:
    :param relying_parties: map<string, string>
    :param attestation_preference: ConveyancePreference enum value
    :param authenticator_attachment: AuthenticatorAttachment enum value
    :param require_resident_key: bool
    :param user_verification: UserVerificationRequirement enum value
    :param registration_timeout: google.protobuf.Duration (google.protobuf.duration_pb2.Duration)
    :param authentication_timeout: google.protobuf.Duration (google.protobuf.duration_pb2.Duration)
    :return: WebAuthnProviderConfig object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        webauthn_provider = model_pb2.WebAuthnProviderConfig(
            relying_parties=relying_parties,
            attestation_preference=attestation_preference,
            authenticator_attachment=authenticator_attachment,
            require_resident_key=bool(require_resident_key),
            user_verification=user_verification,
            registration_timeout=registration_timeout,
            authentication_timeout=authentication_timeout
            )
        return webauthn_provider
    except Exception as exception:
        return logger.logger_error(exception)


def create_authorization_policy_config_node(self,
                                            location,
                                            name,
                                            display_name,
                                            description,
                                            authorization_policy_config,
                                            bookmarks=[]):
    """
    create authorization policy
    :param self:
    :param location: string gid id
    :param name: string pattern: ^[a-z](?:[-a-z0-9]{0,61}[a-z0-9])$
    :param display_name: string
    :param description: string
    :param authorization_policy_config: AuthorizationPolicyConfig object
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized CreateConfigNode instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        valid = True
        if authorization_policy_config and authorization_policy_config.status:
            valid = self.validate_authorization_policy_status(authorization_policy_config.status)
        if valid:
            response = self.stub.CreateConfigNode(
                pb2.CreateConfigNodeRequest(
                    location=location,
                    name=name,
                    display_name=wrappers.StringValue(value=display_name),
                    description=wrappers.StringValue(value=description),
                    authorization_policy_config=authorization_policy_config,
                    bookmarks=bookmarks
                )
            )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return CreateConfigNode.deserialize(response)


def update_authorization_policy_config_node(self,
                                            config_node_id,
                                            etag,
                                            display_name,
                                            description,
                                            authorization_policy_config,
                                            bookmarks=[]):
    """
    update authorization policy
    :param self:
    :param config_node_id: string gid id
    :param etag: string
    :param display_name: string
    :param description: string
    :param authorization_policy_config: AuthorizationPolicyConfig object
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized UpdateConfigNode instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        valid = True
        if authorization_policy_config and authorization_policy_config.status:
            valid = self.validate_authorization_policy_status(authorization_policy_config.status)
        if valid:
            response = self.stub.UpdateConfigNode(
                pb2.UpdateConfigNodeRequest(
                    id=config_node_id,
                    etag=wrappers.StringValue(value=etag),
                    display_name=wrappers.StringValue(value=display_name),
                    description=wrappers.StringValue(value=description),
                    authorization_policy_config= authorization_policy_config,
                    bookmarks=bookmarks
                )
            )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return UpdateConfigNode.deserialize(response)


def authorization_policy_config(self, policy, status, tags=[]):
    """
    create AuthorizationPolicyConfig
    :param self:
    :param policy: JSON string format
    :param status: AuthorizationPolicyConfig.Status
    :param tags: list of strings
    :return: AuthorizationPolicyConfig object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        policy_config = model_pb2.AuthorizationPolicyConfig(
            policy=str(policy),
            status=status,
            tags=tags
            )
        return policy_config
    except Exception as exception:
        return logger.logger_error(exception)


def validate_conveyance(self, conveyance):
    """
    validate conveyance
    :param self:
    :param conveyance: string
    :return: True if valid or raises error
    """
    try:
        conveyances = [c.value for c in ConveyancePreference]
        if conveyance not in conveyances:
            raise TypeError("conveyance must be a member of ConveyancePreference")
        return True
    except Exception as exception:
        return logger.logger_error(exception)


def validate_user_verification(self, user_verification_requirement):
    """
    validate user verification requirement
    :param self:
    :param user_verification_requirement: string
    :return: True if valid or raises error
    """
    try:
        user_verification_requirements = [u.value for u in UserVerificationRequirement]
        if user_verification_requirement not in user_verification_requirements:
            raise TypeError("user_verification_requirements must be a member of UserVerificationRequirement")
        return True
    except Exception as exception:
        return logger.logger_error(exception)


def validate_authenticator_attachment(self, authenticator_attachment):
    """
    validate authenticator attachment
    :param self:
    :param authenticator_attachment: string
    :return: True if valid or raises error
    """
    try:
        authenticator_attachments = [a.value for a in AuthenticatorAttachment]
        if authenticator_attachment not in authenticator_attachments:
            raise TypeError("authenticator_attachment must be a member of AuthenticatorAttachment")
        return True
    except Exception as exception:
        return logger.logger_error(exception)


def validate_authorization_policy_status(self, status):
    """
    validate status
    :param self:
    :param status: string
    :return: True if valid or raises error
    """
    try:
        statuses = [s.value for s in Status]
        if status not in statuses:
            raise TypeError("status must be a member of AuthorizationPolicyConfig.Status")
        return True
    except Exception as exception:
        return logger.logger_error(exception)


def create_knowledge_graph_schema_config_node(self, location, name, display_name, description,
                                              knowledge_graph_schema_config,
                                              bookmarks=[]):
    """
    create a schema and a KG DB
    :param self:
    :param location: appSpace GID id
    :param name: String min_len: 2, max_len: 63, pattern: "^[a-z](?:[-a-z0-9]{0,61}[a-z0-9])$"
    :param display_name: String
    :param description: String
    :param knowledge_graph_schema_config: KnowledgeGraphSchemaConfig object
    :param bookmarks: []
    :return: CreateConfigNodeResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.CreateConfigNode(
            pb2.CreateConfigNodeRequest(
                location=location,
                name=name,
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                knowledge_graph_schema_config=knowledge_graph_schema_config,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return CreateConfigNode.deserialize(response)


def update_knowledge_graph_schema_config_node(self, config_node_id, etag, display_name, description,
                                              knowledge_graph_schema_config,
                                              bookmarks=[]):
    """
    Update a knowledge graph config node
    :param self:
    :param config_node_id: config node gid ID
    :param etag: string
    :param display_name: string
    :param description: string
    :param knowledge_graph_schema_config: KnowledgeGraphSchemaConfig object
    :param bookmarks: []
    :return: UpdateConfigNodeResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.UpdateConfigNode(
            pb2.UpdateConfigNodeRequest(
                id=config_node_id,
                etag=wrappers.StringValue(value=etag),
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                knowledge_graph_schema_config= knowledge_graph_schema_config,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return UpdateConfigNode.deserialize(response)


def knowledge_graph_schema_config(self, schema):
    """
    create KnowledgeGraphSchemaConfig object
    :param schema: string (stringified json)
    :return: KnowledgeGraphSchemaConfig object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        knowledge_graph_schema = model_pb2.KnowledgeGraphSchemaConfig(
            schema=str(schema)
            )
        return knowledge_graph_schema
    except Exception as exception:
        return logger.logger_error(exception)


def list_config_node_versions(self, id_config_node):
    """
    list config nodes versions of the specified config node
    :param self:
    :param id_config_node: string gid id
    :return: list of deserialized ConfigNode instances
    """
    sys.excepthook = logger.handle_excepthook
    try:
        list_config_nodes = self.stub.ListConfigNodeVersions(
            pb2.ListConfigNodeVersionsRequest(
                id=id_config_node
            )
        )
        if not list_config_nodes:
            return None
        res = [ConfigNode.deserialize(config_node) for config_node in list_config_nodes.config_nodes]
        return res
    except Exception as exception:
        return logger.logger_error(exception)
