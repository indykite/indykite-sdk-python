from indykite_sdk.identity import helper
from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
from indykite_sdk.indykite.identity.v1beta2 import model_pb2 as model
import sys
import indykite_sdk.utils.logger as logger


def patch_properties(self, digital_twin_id, tenant_id, operations, admin_token=None, force_delete=False):
    """
    patch digital twin property
    :param self:
    :param digital_twin_id: string GID id
    :param tenant_id: string GID id
    :param operations: list of PropertyBatchOperation objects
    :param admin_token: string
    :param force_delete: boolean
    :return: PatchDigitalTwinResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.PatchDigitalTwin(
            pb2.PatchDigitalTwinRequest(
                id=model.DigitalTwinIdentifier(
                    digital_twin=model.DigitalTwin(
                        id=str(digital_twin_id),
                        tenant_id=str(tenant_id)
                    )
                ),
                operations=helper.create_property_batch_operations(operations),
                admin_token=admin_token,
                force_delete=force_delete
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return response


def patch_properties_by_token(self, token, operations, admin_token=None, force_delete=False):
    """
    patch digital twin property by token
    :param self:
    :param token: access token as string
    :param operations: list of PropertyBatchOperation objects
    :param admin_token:
    :param force_delete:
    :return:
    """
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
                id=model.DigitalTwinIdentifier(access_token=token),
                operations=helper.create_property_batch_operations(operations),
                admin_token=admin_token,
                force_delete=force_delete
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return response
