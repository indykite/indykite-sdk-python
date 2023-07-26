from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.app_space import ApplicationSpace
from indykite_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from indykite_sdk.model.create_app_space import CreateApplicationSpace
from indykite_sdk.model.update_app_space import UpdateApplicationSpace
from indykite_sdk.model.read_app_space_config import ReadApplicationSpaceConfig
from indykite_sdk.model.update_app_space_config import UpdateApplicationSpaceConfig
from indykite_sdk.indykite.config.v1beta1.model_pb2 import ApplicationSpaceConfig, UniquePropertyConstraint, \
    UsernamePolicy
import sys
import indykite_sdk.utils.logger as logger


def read_app_space_by_id(self, app_space_id, bookmarks=[]):
    """
    get AppSpace object from id
    :param self:
    :param app_space_id: string gid id
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: AppSpace object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.ReadApplicationSpace(
            pb2.ReadApplicationSpaceRequest(
                id=str(app_space_id),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return ApplicationSpace.deserialize(response.app_space)


def read_app_space_by_name(self, customer_id, app_space_name, bookmarks=[]):
    """
    get AppSpace object from name
    :param self:
    :param customer_id: string gid id
    :param app_space_name: string
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: AppSpace object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.ReadApplicationSpace(
            pb2.ReadApplicationSpaceRequest(
                name=UniqueNameIdentifier(
                    location=customer_id,
                    name=app_space_name
                ),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return ApplicationSpace.deserialize(response.app_space)


def create_app_space(self, customer_id, name, display_name, description="", bookmarks=[]):
    """
    create new AppSpace
    :param self:
    :param customer_id: string gid id
    :param name: string pattern: ^[a-z](?:[-a-z0-9]{0,61}[a-z0-9])$
    :param display_name: string
    :param description: string
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized CreateApplicationSpaceResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.CreateApplicationSpace(
            pb2.CreateApplicationSpaceRequest(
                customer_id=customer_id,
                name=name,
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return CreateApplicationSpace.deserialize(response)


def update_app_space(self, app_space_id, etag, display_name, description="", bookmarks=[]):
    """
    update existing AppSpace
    :param self:
    :param app_space_id: string gid id
    :param etag: string
    :param display_name: string
    :param description: string
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized UpdateApplicationSpaceResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.UpdateApplicationSpace(
            pb2.UpdateApplicationSpaceRequest(
                id=app_space_id,
                etag=wrappers.StringValue(value=etag),
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return UpdateApplicationSpace.deserialize(response)


def list_app_spaces(self, customer_id, match=[], bookmarks=[]):
    """
    list AppSpaces which match exact name in match param
    :param self:
    :param customer_id: string gid id
    :param match: list of strings
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: ListApplicationSpacesResponse object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        streams = self.stub.ListApplicationSpaces(
            pb2.ListApplicationSpacesRequest(
                customer_id=customer_id,
                match=match,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not streams:
        return None

    try:
        res = [ApplicationSpace.deserialize(response.app_space) for response in streams]
        return res
    except Exception as exception:
        return logger.logger_error(exception)


def delete_app_space(self, app_space_id, etag, bookmarks):
    """
    delete an AppSpace
    :param self:
    :param app_space_id: string gid id
    :param etag: string
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: DeleteApplicationSpaceResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.DeleteApplicationSpace(
            pb2.DeleteApplicationSpaceRequest(
                id=app_space_id,
                etag=wrappers.StringValue(value=etag),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return response


def read_app_space_config(self, app_space_id, bookmarks=[]):
    """
    get ApplicationSpaceConfig object from appSpace id
    :param self:
    :param app_space_id: string gid id
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized ReadApplicationSpaceResponse object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.ReadApplicationSpaceConfig(
            pb2.ReadApplicationSpaceConfigRequest(
                id=str(app_space_id),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return ReadApplicationSpaceConfig.deserialize(response)


def update_app_space_config(self, app_space_id, etag, app_space_config, bookmarks=[]):
    """
    get ApplicationSpaceConfig object from app_space_id
    :param self:
    :param app_space_id: string gid id
    :param etag: string
    :param app_space_config: ApplicationSpaceConfig
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized UpdateApplicationSpaceConfigResponse object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.UpdateApplicationSpaceConfig(
            pb2.UpdateApplicationSpaceConfigRequest(
                id=str(app_space_id),
                etag=wrappers.StringValue(value=etag),
                config=app_space_config,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return UpdateApplicationSpaceConfig.deserialize(response)


def create_app_space_config(
    self,
    default_tenant_id=None,
    default_auth_flow_id=None,
    default_email_service_id=None,
    unique_property_constraints={},
    username_policy=None
):
    """
    get ApplicationSpaceConfig object from default_auth_flow_id or default_email_service_id
    :param self:
    :param default_tenant_id: string gid id
    :param default_auth_flow_id: string gid id
    :param default_email_service_id: string gid id
    :param unique_property_constraints: map<string, UniquePropertyConstraint>
    :param username_policy: UsernamePolicy
    :return: ApplicationSpaceConfig
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = ApplicationSpaceConfig(
            default_tenant_id=default_tenant_id,
            default_auth_flow_id=default_auth_flow_id,
            default_email_service_id=default_email_service_id,
            unique_property_constraints=unique_property_constraints,
            username_policy=username_policy
        )
        return response
    except Exception as exception:
        return logger.logger_error(exception)


def unique_property_constraints(self, tenant_unique, canonicalization):
    """
    create UniquePropertyConstraint
    :param self:
    :param tenant_unique: bool -> if true the value will be unique only in Tenant and not across multiple tenants
    :param canonicalization:  [] in ["unicode", "case-insensitive"]
    :return: UniquePropertyConstraint object
    """
    property = UniquePropertyConstraint(
        tenant_unique=bool(tenant_unique),
        canonicalization=canonicalization
        )
    return property
