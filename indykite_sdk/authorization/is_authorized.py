from indykite_sdk.indykite.authorization.v1beta1 import authorization_service_pb2 as pb2
from indykite_sdk.indykite.identity.v1beta2 import attributes_pb2 as attributes
from indykite_sdk.indykite.identity.v1beta2 import model_pb2 as model
from indykite_sdk.indykite.objects.v1beta1 import struct_pb2 as pb2_struct
from indykite_sdk.indykite.authorization.v1beta1 import model_pb2 as pb2_model
from indykite_sdk.model.is_authorized import IsAuthorizedResponse
import sys
import indykite_sdk.utils.logger as logger


def is_authorized_digital_twin(self, digital_twin_id, tenant_id, resources=[], input_params={}, policy_tags=[]):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.IsAuthorized(
            pb2.IsAuthorizedRequest(
                subject=pb2_model.Subject(
                    digital_twin_identifier=model.DigitalTwinIdentifier(
                        digital_twin=model.DigitalTwin(
                            id=str(digital_twin_id),
                            tenant_id=str(tenant_id)
                        )
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
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.IsAuthorized(
            pb2.IsAuthorizedRequest(
                subject=pb2_model.Subject(
                    digital_twin_identifier=model.DigitalTwinIdentifier(
                        access_token=str(access_token)
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


def is_authorized_property_filter(self, type_filter, value, resources=[], input_params={}, policy_tags=[]):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.IsAuthorized(
            pb2.IsAuthorizedRequest(
                subject=pb2_model.Subject(
                    digital_twin_identifier=model.DigitalTwinIdentifier(
                        property_filter=attributes.PropertyFilter(
                            type=str(type_filter),
                            value=pb2_struct.Value(string_value=value)
                        )
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
        pb2.IsAuthorizedRequest.Resource(id=r.id, type=r.type, actions=list(r.actions))
        for r in resources
    ]


def request_input_params(input_params):
    input_params_dict = {
        k: pb2_model.InputParam(string_value=str(v))
        for k, v in input_params.items()
    }
    return input_params_dict

