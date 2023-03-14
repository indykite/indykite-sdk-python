from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from indykite_sdk.model.create_config_node import CreateConfigNode
from indykite_sdk.model.update_config_node import UpdateConfigNode
from indykite_sdk.model.config_node import ConfigNode
from indykite_sdk.model.conveyance_preference import ConveyancePreference
from indykite_sdk.model.user_verification_requirement import UserVerificationRequirement
from indykite_sdk.model.authenticator_attachment import AuthenticatorAttachment
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
                email_service_config= email_service_config,
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
                email_service_config= email_service_config,
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
                auth_flow_config= auth_flow_config,
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
                auth_flow_config= auth_flow_config,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return UpdateConfigNode.deserialize(response)


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
                oauth2_client_config= oauth2_client_config,
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


def create_ingest_mapping_config_node(self, location, name, display_name, description, ingest_mapping_config,
                                      bookmarks=[]):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.CreateConfigNode(
            pb2.CreateConfigNodeRequest(
                location=location,
                name=name,
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                ingest_mapping_config= ingest_mapping_config,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return CreateConfigNode.deserialize(response)


def update_ingest_mapping_config_node(self, config_node_id, etag, display_name, description, ingest_mapping_config,
                                      bookmarks=[]):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.UpdateConfigNode(
            pb2.UpdateConfigNodeRequest(
                id=config_node_id,
                etag=wrappers.StringValue(value=etag),
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                ingest_mapping_config=ingest_mapping_config,
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
            validate_conveyance(webauthn_provider_config.attestation_preference)
        if webauthn_provider_config and webauthn_provider_config.user_verification:
            validate_user_verification(webauthn_provider_config.attestation_preference)
        if webauthn_provider_config and webauthn_provider_config.authenticator_attachment:
            validate_authenticator_attachment(webauthn_provider_config.authenticator_attachment)

        response = self.stub.CreateConfigNode(
            pb2.CreateConfigNodeRequest(
                location=location,
                name=name,
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                webauthn_provider_config= webauthn_provider_config,
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
            validate_conveyance(webauthn_provider_config.attestation_preference)
        if webauthn_provider_config and webauthn_provider_config.user_verification:
            validate_user_verification(webauthn_provider_config.user_verification)
        if webauthn_provider_config and webauthn_provider_config.authenticator_attachment:
            validate_authenticator_attachment(webauthn_provider_config.authenticator_attachment)

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


def validate_conveyance(conveyance):
    try:
        conveyances = [c.value for c in ConveyancePreference]
        if conveyance not in conveyances:
            raise TypeError("conveyance must be a member of ConveyancePreference")
        return True
    except Exception as exception:
        return logger.logger_error(exception)


def validate_user_verification(user_verification_requirement):
    try:
        user_verification_requirements = [u.value for u in UserVerificationRequirement]
        if user_verification_requirement not in user_verification_requirements:
            raise TypeError("user_verification_requirements must be a member of UserVerificationRequirement")
        return True
    except Exception as exception:
        return logger.logger_error(exception)


def validate_authenticator_attachment(authenticator_attachment):
    try:
        authenticator_attachments = [a.value for a in AuthenticatorAttachment]
        if authenticator_attachment not in authenticator_attachments:
            raise TypeError("authenticator_attachment must be a member of AuthenticatorAttachment")
        return True
    except Exception as exception:
        return logger.logger_error(exception)
