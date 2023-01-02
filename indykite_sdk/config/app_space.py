from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.app_space import ApplicationSpace
from indykite_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from indykite_sdk.model.create_app_space import CreateApplicationSpace
from indykite_sdk.model.update_app_space import UpdateApplicationSpace


def get_app_space_by_id(self, app_space_id):
    try:
        response = self.stub.ReadApplicationSpace(
            pb2.ReadApplicationSpaceRequest(
                id=str(app_space_id)
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return ApplicationSpace.deserialize(response.app_space)


def get_app_space_by_name(self, customer_id, app_space_name):

    try:
        response = self.stub.ReadApplicationSpace(
            pb2.ReadApplicationSpaceRequest(
                name=UniqueNameIdentifier(location = customer_id, name = app_space_name)
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return ApplicationSpace.deserialize(response.app_space)


def create_app_space(self, customer_id, name, display_name, description="", bookmarks=[]):

    try:
        response = self.stub.CreateApplicationSpace(
            pb2.CreateApplicationSpaceRequest(
                customer_id=customer_id,name=name, display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description), bookmarks=bookmarks
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return CreateApplicationSpace.deserialize(response)


def update_app_space(self, app_space_id, etag, display_name, description="", bookmarks=[]):

    try:
        response = self.stub.UpdateApplicationSpace(
            pb2.UpdateApplicationSpaceRequest(
                id=app_space_id,etag=wrappers.StringValue(value=etag),
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description), bookmarks=bookmarks
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return UpdateApplicationSpace.deserialize(response)


def list_app_spaces(self, customer_id, match=[], bookmarks=[]):

    try:
        streams = self.stub.ListApplicationSpaces(
            pb2.ListApplicationSpacesRequest(
                customer_id=customer_id,match=match,
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


def delete_app_space(self, app_space_id, etag, bookmarks):

    try:
        response = self.stub.DeleteApplicationSpace(
            pb2.DeleteApplicationSpaceRequest(
                id=app_space_id, etag=wrappers.StringValue(value=etag),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return response
