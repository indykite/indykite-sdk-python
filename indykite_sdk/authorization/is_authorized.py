from indykite_sdk.indykite.authorization.v1beta1 import authorization_service_pb2 as pb2
from indykite_sdk.indykite.objects.v1beta1 import struct_pb2 as pb2_struct
from indykite_sdk.indykite.authorization.v1beta1 import model_pb2 as pb2_model
from indykite_sdk.model.is_authorized import IsAuthorizedResponse
import sys
import indykite_sdk.utils.logger as logger


def is_authorized_digital_twin(self, digital_twin_id, resources=[], input_params={}, policy_tags=[]):
    """
    verify subject identified by digital twin id has access to resources
    :param self:
    :param digital_twin_id: gid id
    :param resources: array of Resource objects
    :param input_params: map values of InputParam objects
    :param policy_tags: array of strings
    :return: deserialized IsAuthorizedResponse object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.IsAuthorized(
            pb2.IsAuthorizedRequest(
                subject=pb2_model.Subject(
                    digital_twin_id=pb2_model.DigitalTwin(
                        id=str(digital_twin_id)
                    )
                ),
                resources=request_resource(resources),
                input_params=request_input_params(input_params),
                policy_tags=policy_tags
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return IsAuthorizedResponse.deserialize(response)


def is_authorized_token(self, access_token, resources=[], input_params={}, policy_tags=[]):
    """
    verify subject identified by access token has access to resources
    :param self:
    :param access_token: user token
    :param resources: array of Resource objects
    :param input_params: map values of InputParam objects
    :param policy_tags: array of strings
    :return: deserialized IsAuthorizedResponse object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.IsAuthorized(
            pb2.IsAuthorizedRequest(
                subject=pb2_model.Subject(
                    indykite_access_token=str(access_token)
                ),
                resources=request_resource(resources),
                input_params=request_input_params(input_params),
                policy_tags=policy_tags
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return IsAuthorizedResponse.deserialize(response)


def is_authorized_property_filter(self, type_filter, value, resources=[], input_params={}, policy_tags=[]):
    """
    verify subject identified by property has access to resources
    :param self:
    :param type_filter: type property string
    :param value: string
    :param resources: array of Resource objects
    :param input_params: map values of InputParam objects
    :param policy_tags: array of strings
    :return: deserialized IsAuthorizedResponse object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.IsAuthorized(
            pb2.IsAuthorizedRequest(
                subject=pb2_model.Subject(
                    digital_twin_property=pb2_model.Property(
                        type=str(type_filter),
                        value=pb2_struct.Value(string_value=value)
                    )
                ),
                resources=request_resource(resources),
                input_params=request_input_params(input_params),
                policy_tags=policy_tags
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return IsAuthorizedResponse.deserialize(response)


def is_authorized_external_id(self, type, external_id, resources=[], input_params={}, policy_tags=[]):
    """
    verify subject identified by type and external_id has access to resources
    :param self:
    :param type: string max_len: 64  pattern: "^[a-zA-Z]*$"
    :param external_id: string
    :param resources: array of Resource objects
    :param input_params: map values of InputParam objects
    :param policy_tags: array of strings
    :return: deserialized IsAuthorizedResponse object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.IsAuthorized(
            pb2.IsAuthorizedRequest(
                subject=pb2_model.Subject(
                    external_id=pb2_model.ExternalID(
                        type=str(type),
                        external_id=str(external_id)
                    )
                ),
                resources=request_resource(resources),
                input_params=request_input_params(input_params),
                policy_tags=policy_tags
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return IsAuthorizedResponse.deserialize(response)


def request_resource(resources):
    return [
        pb2.IsAuthorizedRequest.Resource(external_id=r.external_id, type=r.type, actions=list(r.actions))
        for r in resources
    ]


def request_input_params(input_params):
    input_params_dict = {
        k: pb2_model.InputParam(string_value=str(v))
        for k, v in input_params.items()
    }
    return input_params_dict
