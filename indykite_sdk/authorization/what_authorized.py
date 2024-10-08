import sys

from indykite_sdk.indykite.authorization.v1beta1 import authorization_service_pb2 as pb2
from indykite_sdk.indykite.objects.v1beta1 import struct_pb2 as pb2_struct
from indykite_sdk.indykite.authorization.v1beta1 import model_pb2 as pb2_model
from indykite_sdk.model.what_authorized import WhatAuthorizedResponse
from indykite_sdk.utils.message_to_value import param_to_inputparam
import indykite_sdk.utils.logger as logger


def what_authorized_digital_twin(self, digital_twin_id, resource_types=[], input_params={}, policy_tags=[]):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.WhatAuthorized(
            pb2.WhatAuthorizedRequest(
                subject=pb2_model.Subject(
                    digital_twin_id=pb2_model.DigitalTwin(
                        id=str(digital_twin_id)
                    )
                ),
                resource_types=request_resource_type(resource_types),
                input_params=request_input_params(input_params),
                policy_tags=policy_tags
            )
        )
        if not response:
            return None
        return WhatAuthorizedResponse.deserialize(response)
    except Exception as exception:
        return logger.logger_error(exception)


def what_authorized_token(self, access_token, resource_types=[], input_params={}, policy_tags=[]):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.WhatAuthorized(
            pb2.WhatAuthorizedRequest(
                subject=pb2_model.Subject(
                    access_token=str(access_token)
                ),
                resource_types=request_resource_type(resource_types),
                input_params=request_input_params(input_params),
                policy_tags=policy_tags
            )
        )
        if not response:
            return None
        return WhatAuthorizedResponse.deserialize(response)
    except Exception as exception:
        return logger.logger_error(exception)


def what_authorized_property_filter(self, type_filter, value, resource_types=[], input_params={}, policy_tags=[]):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.WhatAuthorized(
            pb2.WhatAuthorizedRequest(
                subject=pb2_model.Subject(
                    digital_twin_property=pb2_model.Property(
                        type=str(type_filter),
                        value=pb2_struct.Value(string_value=value)
                    )
                ),
                resource_types=request_resource_type(resource_types),
                input_params=request_input_params(input_params),
                policy_tags=policy_tags
            )
        )
        if not response:
            return None
        return WhatAuthorizedResponse.deserialize(response)
    except Exception as exception:
        return logger.logger_error(exception)


def what_authorized_external_id(self, type, external_id, resource_types=[], input_params={}, policy_tags=[]):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.WhatAuthorized(
            pb2.WhatAuthorizedRequest(
                subject=pb2_model.Subject(
                    external_id=pb2_model.ExternalID(
                        type=str(type),
                        external_id=str(external_id)
                    )
                ),
                resource_types=request_resource_type(resource_types),
                input_params=request_input_params(input_params),
                policy_tags=policy_tags
            )
        )
        if not response:
            return None
        return WhatAuthorizedResponse.deserialize(response)
    except Exception as exception:
        return logger.logger_error(exception)


def request_resource_type(resource_types):
    return [
        pb2.WhatAuthorizedRequest.ResourceType(type=r.type, actions=list(r.actions))
        for r in resource_types
    ]


def request_input_params(input_params):
    input_params_dict = {
        k: param_to_inputparam(v)
        for k, v in input_params.items()
    }
    return input_params_dict
