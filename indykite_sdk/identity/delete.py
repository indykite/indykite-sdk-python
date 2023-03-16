from indykite_sdk.model.digital_twin import DigitalTwinCore
from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
from indykite_sdk.indykite.identity.v1beta2 import model_pb2 as model
import sys
import indykite_sdk.utils.logger as logger


def del_digital_twin(self, digital_twin_id, tenant_id):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.DeleteDigitalTwin(
            pb2.DeleteDigitalTwinRequest(
                id=model.DigitalTwinIdentifier(
                    digital_twin=model.DigitalTwin(
                        id=str(digital_twin_id),
                        tenant_id=str(tenant_id)
                    )
                )
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return DigitalTwinCore.deserialize(response.digital_twin)


def del_digital_twin_by_token(self, token):
    sys.excepthook = logger.handle_excepthook
    try:
        if len(token) < 32:
            raise Exception("Token must be 32 chars or more.")
    except Exception as exception:
        return logger.logger_error(exception)

    try:
        response = self.stub.DeleteDigitalTwin(
                pb2.DeleteDigitalTwinRequest(
                    id=model.DigitalTwinIdentifier(access_token=token)
                )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return DigitalTwinCore.deserialize(response.digital_twin)
