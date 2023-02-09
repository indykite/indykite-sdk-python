from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
from indykite_sdk.indykite.identity.v1beta2 import model_pb2 as model
import sys
import indykite_sdk.utils.logger as logger


def change_password(self, token, new_password):
    sys.excepthook = logger.handle_excepthook
    try:
        if len(token) < 32:
            raise Exception("Token must be 32 chars or more.")
    except Exception as exception:
        return logger.logger_error(exception)

    try:
        response = self.stub.ChangePassword(
            pb2.ChangePasswordRequest(
                token=token,
                password=new_password,
                ignore_policy=2
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return "The password has been changed successfully"


def change_password_of_user(self, digital_twin_id, tenant_id, new_password):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.ChangePassword(
            pb2.ChangePasswordRequest(
                digital_twin=model.DigitalTwin(
                    id=str(digital_twin_id),
                    tenant_id=str(tenant_id)
                ),
                password=new_password
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return "The password has been changed successfully"
