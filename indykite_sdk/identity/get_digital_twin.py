import uuid

from indykite_sdk.identity import helper
from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
from indykite_sdk.indykite.identity.v1beta2 import model_pb2 as model
from indykite_sdk.utils.deserialize_digital_twin_with_token_info import deserialize_digital_twin_with_token_info
import sys
import indykite_sdk.utils.logger as logger


def get_digital_twin(self, digital_twin_id, tenant_id, fields):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.GetDigitalTwin(
            pb2.GetDigitalTwinRequest(
                id=pb2.DigitalTwinIdentifier(
                    digital_twin=model.DigitalTwin(
                        id=str(digital_twin_id),
                        tenant_id=str(tenant_id)
                    )
                ),
                properties=helper.create_property_mask(fields)
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    return deserialize_digital_twin_with_token_info(response)


def get_digital_twin_by_token(self, token, fields):
    sys.excepthook = logger.handle_excepthook
    try:
        if len(token) < 32:
            raise Exception("Token must be 32 chars or more.")
    except Exception as exception:
        print(exception)
        return None

    try:
        response = self.stub.GetDigitalTwin(
                pb2.GetDigitalTwinRequest(
                    id=pb2.DigitalTwinIdentifier(access_token=token),
                    properties=helper.create_property_mask(fields)
                )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    return deserialize_digital_twin_with_token_info(response)
