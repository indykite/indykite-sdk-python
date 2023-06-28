from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.application import Application
from indykite_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from indykite_sdk.model.create_application import CreateApplication
from indykite_sdk.model.update_application import UpdateApplication
import sys
import indykite_sdk.utils.logger as logger


def read_application_by_id(self, application_id, bookmarks=[]):
    """
    get an Application object with an id
    :param self:
    :param application_id: string gid id
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: Application object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.ReadApplication(
            pb2.ReadApplicationRequest(
                id=str(application_id),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return Application.deserialize(response.application)


def read_application_by_name(self, app_space_id, application_name, bookmarks=[]):
    """
    get an Application object with a name
    :param self:
    :param app_space_id: string gid id
    :param application_name: string
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: Application object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.ReadApplication(
            pb2.ReadApplicationRequest(
                name=UniqueNameIdentifier(
                    location=app_space_id,
                    name=application_name
                ),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return Application.deserialize(response.application)


def create_application(self, app_space_id, name, display_name, description="", bookmarks=[]):
    """
    create an Application
    :param self:
    :param app_space_id: string gid id
    :param name: string pattern: ^[a-z](?:[-a-z0-9]{0,61}[a-z0-9])$
    :param display_name: string
    :param description: string
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized CreateApplicationResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.CreateApplication(
            pb2.CreateApplicationRequest(
                app_space_id=app_space_id,
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

    return CreateApplication.deserialize(response, app_space_id, name)


def update_application(self, application_id, etag, display_name, description="", bookmarks=[]):
    """
    update existing Application
    :param self:
    :param application_id: string gid id
    :param etag: string
    :param display_name: string
    :param description: string
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized UpdateApplicationResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.UpdateApplication(
            pb2.UpdateApplicationRequest(
                id=application_id,
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

    return UpdateApplication.deserialize(response)


def list_applications(self, app_space_id, match=[], bookmarks=[]):
    """
    list App which match exact name in match param
    :param self:
    :param app_space_id: string gid id
    :param match: list of strings
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: ListApplicationResponse object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        streams = self.stub.ListApplications(
            pb2.ListApplicationsRequest(
                app_space_id=app_space_id,
                match=match,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not streams:
        return None

    responses = []
    try:
        for response in streams:
            responses.append(response)
    except Exception as exception:
        return logger.logger_error(exception)

    return responses


def delete_application(self, application_id, etag, bookmarks):
    """
    delete an application
    :param self:
    :param application_id: string gid id
    :param etag: string
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: DeleteApplicationResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.DeleteApplication(
            pb2.DeleteApplicationRequest(
                id=application_id,
                etag=wrappers.StringValue(value=etag),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return response
