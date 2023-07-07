from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
from indykite_sdk.indykite.identity.v1beta2 import model_pb2 as model
from indykite_sdk.model.digital_twin import DigitalTwinCore
from indykite_sdk.indykite.objects.v1beta1 import struct_pb2 as struct
import sys
import indykite_sdk.utils.logger as logger


def verify_digital_twin_email(self, token):
    """
    verify digital twin email
    confirms that the message from start_digital_twin_email_verification function was sent
    and user visited the link
    :param self:
    :param token: string
    :return: deserialized VerifyDigitalTwinEmailResponse.DigitalTwin
    """
    sys.excepthook = logger.handle_excepthook
    try:
        if len(token) < 32:
            raise Exception("Token must be 32 chars or more.")
    except Exception as exception:
        return logger.logger_error(exception)

    try:
        response = self.stub.VerifyDigitalTwinEmail(
            pb2.VerifyDigitalTwinEmailRequest(token=token)
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return DigitalTwinCore.deserialize(response.digital_twin)


def start_digital_twin_email_verification(self, dt_id, tenant_id, email, attributes={}):
    """
    start DT email verification by sending a message with a link
    to verify the control over the notification channel
    :param self:
    :param dt_id: string GID id
    :param tenant_id: string GID id
    :param email: string
    :param attributes: dict
    :return: success message
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.StartDigitalTwinEmailVerification(
            pb2.StartDigitalTwinEmailVerificationRequest(
                digital_twin=model.DigitalTwin(
                    id=str(dt_id),
                    tenant_id=str(tenant_id)
                ),
                email=email,
                attributes=struct.MapValue(fields=attributes)
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return "Email was sent to: " + email
