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


def create_email_service_config_node(self, location, name, display_name, description, email_service_config,
                                     bookmarks=[]):
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


def read_config_node(self, config_node_id, bookmarks=[]):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.ReadConfigNode(
            pb2.ReadConfigNodeRequest(
                id=str(config_node_id), bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return ConfigNode.deserialize(response.config_node)


def update_email_service_config_node(self, config_node_id, etag, display_name, description, email_service_config,
                                     bookmarks=[]):
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


def create_auth_flow_config_node(self, location, name, display_name, description, auth_flow_config,
                                 bookmarks=[]):
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


def update_auth_flow_config_node(self, config_node_id, etag, display_name, description, auth_flow_config,
                                 bookmarks=[]):
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
                     source,
                     default):
    """
    create AuthFlowConfig
    :param self:
    :param source_format: AuthFlowConfig.Format enum value
    :param source: bytes of json string
    :param default: google.protobuf.BoolValue
    :return:
    """
    sys.excepthook = logger.handle_excepthook
    try:
        auth_flow_config = model_pb2.AuthFlowConfig(
            source_format=source_format,
            source=bytes(source),
            default=wrappers.BoolValue(value=default)
            )
        return auth_flow_config
    except Exception as exception:
        return logger.logger_error(exception)


def create_oauth2_client_config_node(self, location, name, display_name, description, oauth2_client_config,
                                     bookmarks=[]):
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


def update_oauth2_client_config_node(self, config_node_id, etag, display_name, description, oauth2_client_config,
                                     bookmarks=[]):
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


def create_webauthn_provider_config_node(self, location, name, display_name, description, webauthn_provider_config,
                                         bookmarks=[]):
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


def update_webauthn_provider_config_node(self, config_node_id, etag, display_name, description, webauthn_provider_config,
                                         bookmarks=[]):
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


def create_authorization_policy_config_node(self, location, name, display_name, description,
                                            authorization_policy_config, bookmarks=[]):
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


def update_authorization_policy_config_node(self, config_node_id, etag, display_name, description,
                                            authorization_policy_config,
                                            bookmarks=[]):
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
    try:
        conveyances = [c.value for c in ConveyancePreference]
        if conveyance not in conveyances:
            raise TypeError("conveyance must be a member of ConveyancePreference")
        return True
    except Exception as exception:
        return logger.logger_error(exception)


def validate_user_verification(self, user_verification_requirement):
    try:
        user_verification_requirements = [u.value for u in UserVerificationRequirement]
        if user_verification_requirement not in user_verification_requirements:
            raise TypeError("user_verification_requirements must be a member of UserVerificationRequirement")
        return True
    except Exception as exception:
        return logger.logger_error(exception)


def validate_authenticator_attachment(self, authenticator_attachment):
    try:
        authenticator_attachments = [a.value for a in AuthenticatorAttachment]
        if authenticator_attachment not in authenticator_attachments:
            raise TypeError("authenticator_attachment must be a member of AuthenticatorAttachment")
        return True
    except Exception as exception:
        return logger.logger_error(exception)


def validate_authorization_policy_status(self, status):
    try:
        statuses = [s.value for s in Status]
        if status not in statuses:
            raise TypeError("status must be a member of AuthorizationPolicyConfig.Status")
        return True
    except Exception as exception:
        return logger.logger_error(exception)


def create_readid_provider_config_node(self, location, name, display_name, description, readid_provider_config,
                                       bookmarks=[]):
    """
    create ReadID provider
    :param self:
    :param location: appSpace GID id
    :param name: String min_len: 2, max_len: 63, pattern: "^[a-z](?:[-a-z0-9]{0,61}[a-z0-9])$"
    :param display_name: String
    :param description: String
    :param readid_provider_config: ReadIDProviderConfig object
    :param bookmarks: list
    :return:
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.CreateConfigNode(
            pb2.CreateConfigNodeRequest(
                location=location,
                name=name,
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                readid_provider_config=readid_provider_config,
                bookmarks=bookmarks
            )
        )
        return CreateConfigNode.deserialize(response)
    except Exception as exception:
        return logger.logger_error(exception)


def update_readid_provider_config_node(self, config_node_id, etag, display_name, description, readid_provider_config,
                                       bookmarks=[]):
    """
    update readID provider
    :param self:
    :param config_node_id: config node gid ID
    :param etag: string
    :param display_name: string
    :param description: string
    :param readid_provider_config: ReadIDProviderConfig object
    :param bookmarks:
    :return:
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.UpdateConfigNode(
            pb2.UpdateConfigNodeRequest(
                id=config_node_id,
                etag=wrappers.StringValue(value=etag),
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                readid_provider_config=readid_provider_config,
                bookmarks=bookmarks
            )
        )
        return UpdateConfigNode.deserialize(response)
    except Exception as exception:
        return logger.logger_error(exception)


def readid_provider_config(self,
                           submitter_secret,
                           manager_secret,
                           submitter_password,
                           host_address,
                           property_map={},
                           unique_property_name=None ):
    """
    create ReadIDProviderConfig object
    :param submitter_secret: string min_len: 36 required
    :param manager_secret: string min_len: 36 required
    :param submitter_password: string min_len: 4 required
    :param host_address: string valid url, starts from https://, required
    :param property_map: map string, ReadIDProviderConfig.Property
    :param unique_property_name: string
    :return: ReadIDProviderConfig object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        read_id_provider = model_pb2.ReadIDProviderConfig(
            submitter_secret=str(submitter_secret),
            manager_secret=str(manager_secret),
            submitter_password=str(submitter_password),
            host_address=str(host_address),
            property_map=property_map,
            unique_property_name=unique_property_name
            )
        return read_id_provider
    except Exception as exception:
        return logger.logger_error(exception)


def readid_property(self, expression, enabled):
    """
    create ReadIDProviderConfig.Property
    :param self:
    :param expression: string min_len: 4 max_len: 512
    :param enabled: bool
    :return: ReadIDProviderConfig.Property object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        property = model_pb2.ReadIDProviderConfig.Property(
            expression=str(expression),
            enabled=bool(enabled)
            )
        return property
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
