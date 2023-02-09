from indykite_sdk.identity import helper
from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
from indykite_sdk.indykite.identity.v1beta2 import model_pb2 as model
import sys
import indykite_sdk.utils.logger as logger


def patch_properties(self, digital_twin_id, tenant_id, fields_in_dict):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.PatchDigitalTwin(
            pb2.PatchDigitalTwinRequest(
                id=pb2.DigitalTwinIdentifier(
                    digital_twin=model.DigitalTwin(
                        id=str(digital_twin_id),
                        tenant_id=str(tenant_id)
                    )
                ),
                operations=helper.create_property_batch_operations(fields_in_dict)
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return response


def patch_properties_by_token(self, token, fields_in_dict):
    sys.excepthook = logger.handle_excepthook
    try:
        if len(token) < 32:
            raise Exception("Token must be 32 chars or more.")
    except Exception as exception:
        return logger.logger_error(exception)

    try:
        # identifier = pb2.DigitalTwinIdentifier()
        # identifier.access_token = token

        response = self.stub.PatchDigitalTwin(
            pb2.PatchDigitalTwinRequest(
                id=pb2.DigitalTwinIdentifier(access_token=token),
                operations=helper.create_property_batch_operations(fields_in_dict)
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return "The patch operation was success: " + str(response)
