from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from indykite_sdk.model.create_oauth2_application import CreateOAuth2Application
from indykite_sdk.model.update_oauth2_application import UpdateOAuth2Application
from indykite_sdk.model.oauth2_application import OAuth2Application
import sys
import indykite_sdk.utils.logger as logger


def create_oauth2_application(self,
                              oauth2_provider_id,
                              name,
                              display_name,
                              description,
                              config,
                              bookmarks=[]):
    """
    create OAuth2 application
    :param self:
    :param oauth2_provider_id: string gid id
    :param name: string pattern: ^[a-z](?:[-a-z0-9]{0,61}[a-z0-9])$
    :param display_name: string
    :param description: string
    :param config: OAuth2ApplicationConfig object
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized CreateOAuth2Application instance (client secret will only appear once here)
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.CreateOAuth2Application(
            pb2.CreateOAuth2ApplicationRequest(
                oauth2_provider_id=oauth2_provider_id,
                name=name,
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                config=config,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return CreateOAuth2Application.deserialize(response)


def read_oauth2_application(self, oauth2_application_id, bookmarks=[]):
    """
    read OAuth2 application
    :param self:
    :param oauth2_application_id: string gid id
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return:
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.ReadOAuth2Application(
            pb2.ReadOAuth2ApplicationRequest(
                id=str(oauth2_application_id),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return OAuth2Application.deserialize(response.oauth2_application)


def update_oauth2_application(self,
                              oauth2_application_id,
                              etag,
                              display_name,
                              description,
                              config,
                              bookmarks=[]):
    """
    update OAUth2 application
    :param self:
    :param oauth2_application_id: string gid id
    :param etag: string
    :param display_name: string
    :param description: string
    :param config: OAuth2ApplicationConfig object
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized UpdateOAuth2Application instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.UpdateOAuth2Application(
            pb2.UpdateOAuth2ApplicationRequest(
                id=oauth2_application_id,
                etag=wrappers.StringValue(value=etag),
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                config=config,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return UpdateOAuth2Application.deserialize(response)


def delete_oauth2_application(self, oauth2_application_id, etag, bookmarks=[]):
    """
    delete OAuth2 application
    :param self:
    :param oauth2_application_id: string gid id
    :param etag: string
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: DeleteOAuth2ApplicationResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.DeleteOAuth2Application(
            pb2.DeleteOAuth2ApplicationRequest(
                id=str(oauth2_application_id),
                etag=wrappers.StringValue(value=etag),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return response
