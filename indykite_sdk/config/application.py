from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.application import Application
from indykite_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from indykite_sdk.model.create_application import CreateApplication
from indykite_sdk.model.update_application import UpdateApplication


def get_application_by_id(self, application_id):
    try:
        response = self.stub.ReadApplication(
            pb2.ReadApplicationRequest(
                id=str(application_id)
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return Application.deserialize(response.application)


def get_application_by_name(self, app_space_id, application_name):

    try:
        response = self.stub.ReadApplication(
            pb2.ReadApplicationRequest(
                name=UniqueNameIdentifier(location = app_space_id, name = application_name)
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return Application.deserialize(response.application)


def create_application(self, app_space_id, name, display_name, description="", bookmarks=[]):

    try:
        response = self.stub.CreateApplication(
            pb2.CreateApplicationRequest(
                app_space_id=app_space_id, name=name, display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description), bookmarks=bookmarks
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return CreateApplication.deserialize(response)


def update_application(self, application_id, etag, display_name, description="", bookmarks=[]):

    try:
        response = self.stub.UpdateApplication(
            pb2.UpdateApplicationRequest(
                id=application_id,etag=wrappers.StringValue(value=etag),
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description), bookmarks=bookmarks
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return UpdateApplication.deserialize(response)


def list_applications(self, app_space_id, match=[], bookmarks=[]):

    try:
        streams = self.stub.ListApplications(
            pb2.ListApplicationsRequest(
                app_space_id=app_space_id,match=match,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not streams:
        return None

    responses = []
    try:
        for response in streams:
            responses.append(response)
    except Exception as exception:
        print(exception)
        return None

    return responses


def delete_application(self, application_id, etag, bookmarks):

    try:
        response = self.stub.DeleteApplication(
            pb2.DeleteApplicationRequest(
                id=application_id, etag=wrappers.StringValue(value=etag),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return response
