from indykite_sdk.indykite.authorization.v1beta1 import authorization_service_pb2 as pb2
from indykite_sdk.indykite.identity.v1beta2 import attributes_pb2 as attributes
from indykite_sdk.indykite.identity.v1beta2 import model_pb2 as model
from indykite_sdk.indykite.objects.v1beta1 import struct_pb2 as pb2_struct
from indykite_sdk.indykite.authorization.v1beta1 import model_pb2 as pb2_model
from indykite_sdk.model.what_authorized import WhatAuthorizedResponse
import sys
import indykite_sdk.utils.logger as logger


def what_authorized_digital_twin(self, digital_twin_id, tenant_id, resource_types=[], input_params={}, policy_tags=[]):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.WhatAuthorized(
            pb2.WhatAuthorizedRequest(
                subject=pb2_model.Subject(
                    digital_twin_identifier=model.DigitalTwinIdentifier(
                        digital_twin=model.DigitalTwin(
                            id=str(digital_twin_id),
                            tenant_id=str(tenant_id)
                        )
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
                    digital_twin_identifier=model.DigitalTwinIdentifier(
                        access_token=str(access_token)
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


def what_authorized_property_filter(self, type_filter, value, resource_types=[], input_params={}, policy_tags=[]):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.WhatAuthorized(
            pb2.WhatAuthorizedRequest(
                subject=pb2_model.Subject(
                    digital_twin_identifier=model.DigitalTwinIdentifier(
                        property_filter=attributes.PropertyFilter(
                            type=str(type_filter),
                            value=pb2_struct.Value(string_value=value)
                        )
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
        k: pb2_model.InputParam(string_value=str(v))
        for k, v in input_params.items()
    }
    return input_params_dict
