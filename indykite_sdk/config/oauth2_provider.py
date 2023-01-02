from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from indykite_sdk.model.create_oauth2_provider import CreateOAuth2Provider
from indykite_sdk.model.update_oauth2_provider import UpdateOAuth2Provider


def create_oauth2_provider(self, app_space_id, name, display_name, description, config,
                           bookmarks=[]):

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
        print(exception)
        return None

    if not response:
        return None

    return CreateOAuth2Provider.deserialize(response)


def read_oauth2_provider(self, oauth2_provider_id, bookmarks=[]):
    try:
        response = self.stub.ReadOAuth2Provider(
            pb2.ReadOAuth2ProviderRequest(
                id=str(oauth2_provider_id), bookmarks=bookmarks
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return response.oauth2_provider


def update_oauth2_provider(self, oauth2_provider_id, etag, display_name, description, config,
                           bookmarks=[]):

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
        print(exception)
        return None

    if not response:
        return None

    return UpdateOAuth2Provider.deserialize(response)


def delete_oauth2_provider(self, oauth2_provider_id, etag, bookmarks=[]):
    try:
        response = self.stub.DeleteOAuth2Provider(
            pb2.DeleteOAuth2ProviderRequest(
                id=str(oauth2_provider_id),
                etag=wrappers.StringValue(value=etag),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return response
