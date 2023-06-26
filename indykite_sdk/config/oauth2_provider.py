from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from indykite_sdk.model.create_oauth2_provider import CreateOAuth2Provider
from indykite_sdk.model.update_oauth2_provider import UpdateOAuth2Provider
from indykite_sdk.model.oauth2_provider import OAuth2Provider
import sys
import indykite_sdk.utils.logger as logger


def create_oauth2_provider(self,
                           app_space_id,
                           name,
                           display_name,
                           description,
                           config,
                           bookmarks=[]):
    """
    create OAuth2 provider
    :param self:
    :param app_space_id: string gid id
    :param name: string pattern: ^[a-z](?:[-a-z0-9]{0,61}[a-z0-9])$
    :param display_name: string
    :param description: string
    :param config: OAuth2ProviderConfig object
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized CreateOAuth2Provider instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.CreateOAuth2Provider(
            pb2.CreateOAuth2ProviderRequest(
                app_space_id=app_space_id,
                name=name,
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description),
                config= config,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return CreateOAuth2Provider.deserialize(response)


def read_oauth2_provider(self, oauth2_provider_id, bookmarks=[]):
    """
    read OAuth2 provider
    :param self:
    :param oauth2_provider_id: string gid id
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized OAuth2Provider instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.ReadOAuth2Provider(
            pb2.ReadOAuth2ProviderRequest(
                id=str(oauth2_provider_id),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return OAuth2Provider.deserialize(response.oauth2_provider)


def update_oauth2_provider(self,
                           oauth2_provider_id,
                           etag,
                           display_name,
                           description,
                           config,
                           bookmarks=[]):
    """
    update OAuth2 provider
    :param self:
    :param oauth2_provider_id: string gid id
    :param etag: string
    :param display_name: string
    :param description: string
    :param config: OAuth2ProviderConfig object
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized UpdateOAuth2Provider instance
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.UpdateOAuth2Provider(
            pb2.UpdateOAuth2ProviderRequest(
                id=oauth2_provider_id,
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
    return UpdateOAuth2Provider.deserialize(response)


def delete_oauth2_provider(self, oauth2_provider_id, etag, bookmarks=[]):
    """
    delete OAuth2 provider
    :param self:
    :param oauth2_provider_id: string gid id
    :param etag: string
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: DeleteOAuth2ProviderResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.DeleteOAuth2Provider(
            pb2.DeleteOAuth2ProviderRequest(
                id=str(oauth2_provider_id),
                etag=wrappers.StringValue(value=etag),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return response
