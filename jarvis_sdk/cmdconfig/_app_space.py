import uuid

from jarvis_sdk.cmdconfig import helper
from jarvis_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from jarvis_sdk.indykite.config.v1beta1 import model_pb2 as model
from jarvis_sdk.model.app_space import ApplicationSpace
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier


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


