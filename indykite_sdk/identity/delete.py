from indykite_sdk.model.digital_twin import DigitalTwinCore
from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
from indykite_sdk.indykite.identity.v1beta2 import model_pb2 as model
import sys
import indykite_sdk.utils.logger as logger


def del_digital_twin(self, digital_twin_id, tenant_id, admin_token=""):
    """
    delete DT by id
    :param self:
    :param digital_twin_id: DT gid id string
    :param tenant_id: tenant gid id string
    :param admin_token: token as string
    :return: DigitalTwin object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.DeleteDigitalTwin(
            pb2.DeleteDigitalTwinRequest(
                id=model.DigitalTwinIdentifier(
                    digital_twin=model.DigitalTwin(
                        id=str(digital_twin_id),
                        tenant_id=str(tenant_id)
                    )
                ),
                admin_token=admin_token
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return DigitalTwinCore.deserialize(response.digital_twin)


def del_digital_twin_by_token(self, token):
    """
    delete DT by token
    :param self:
    :param token: user token
    :return: DigitalTwin object
    """
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


def del_digital_twin_by_property(self, property_filter):
    """
    delete DT by property
    :param self:
    :param property_filter: PropertyFilter attribute
    :return: DigitalTwin object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.DeleteDigitalTwin(
                pb2.DeleteDigitalTwinRequest(
                    id=model.DigitalTwinIdentifier(property_filter=property_filter)
                )
        )
        if not response:
            return None

        return DigitalTwinCore.deserialize(response.digital_twin)
    except Exception as exception:
        return logger.logger_error(exception)
