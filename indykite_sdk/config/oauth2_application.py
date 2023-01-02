from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from indykite_sdk.model.create_oauth2_application import CreateOAuth2Application
from indykite_sdk.model.update_oauth2_application import UpdateOAuth2Application


def create_oauth2_application(self, oauth2_provider_id, name, display_name, description,
                              config, bookmarks=[]):

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
        print(exception)
        return None

    if not response:
        return None

    return CreateOAuth2Application.deserialize(response)


def read_oauth2_application(self, oauth2_application_id, bookmarks=[]):
    try:
        response = self.stub.ReadOAuth2Application(
            pb2.ReadOAuth2ApplicationRequest(
                id=str(oauth2_application_id), bookmarks=bookmarks
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return response.oauth2_application


def update_oauth2_application(self, oauth2_application_id, etag, display_name, description,
                              config, bookmarks=[]):

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
        print(exception)
        return None

    if not response:
        return None

    return UpdateOAuth2Application.deserialize(response)


def delete_oauth2_application(self, oauth2_application_id, etag, bookmarks=[]):
    try:
        response = self.stub.DeleteOAuth2Application(
            pb2.DeleteOAuth2ApplicationRequest(
                id=str(oauth2_application_id),
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
