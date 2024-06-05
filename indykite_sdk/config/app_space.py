from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.app_space import ApplicationSpace
from indykite_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from indykite_sdk.model.create_app_space import CreateApplicationSpace
from indykite_sdk.model.update_app_space import UpdateApplicationSpace
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
