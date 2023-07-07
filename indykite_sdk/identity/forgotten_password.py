from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
from indykite_sdk.indykite.identity.v1beta2 import model_pb2 as model
import sys
from indykite_sdk.utils.logger import handle_excepthook, logger_error


def start_forgotten_password_flow(self, digital_twin_id, tenant_id):
    """
    start forgotten password flow by sending message with link
    :param self:
    :param digital_twin_id: string GID id
    :param tenant_id: string GID id
    :return: True
    """
    sys.excepthook = handle_excepthook
    try:
        response = self.stub.StartForgottenPasswordFlow(
            pb2.StartForgottenPasswordFlowRequest(
                digital_twin=model.DigitalTwin(
                    id=str(digital_twin_id),
                    tenant_id=str(tenant_id)
                )
            )
        )
    except Exception as exception:
        return logger_error(exception)

    if not response:
        return None

    return True
