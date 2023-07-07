from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
from indykite_sdk.model.digital_twin_kind import DigitalTwinKind
from indykite_sdk.model.register_digital_twin_without_credential import RegisterDigitalTwinWithoutCredential
import sys
import indykite_sdk.utils.logger as logger


def register_digital_twin_without_credential(self, tenant_id, kind, tags, properties, bookmarks=[]):
    """
    register digital twin without credentials
    :param self:
    :param tenant_id: string GID id
    :param kind: string from enum
    :param tags: string from enum
    :param properties: list of Property object
    :param bookmarks: list of strings
    :return: deserialized RegisterDigitalTwinWithoutCredentialResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        if kind and validate_kind(kind):
            response = self.stub.RegisterDigitalTwinWithoutCredential(
                pb2.RegisterDigitalTwinWithoutCredentialRequest(
                    tenant_id=str(tenant_id),
                    digital_twin_kind=kind,
                    digital_twin_tags=tags,
                    properties=properties,
                    bookmarks=bookmarks
                )
            )
            return RegisterDigitalTwinWithoutCredential.deserialize(response)
        return None
    except Exception as exception:
        return logger.logger_error(exception)


def validate_kind(kind):
    """
    validate kind value
    :param kind: string from enum
    :return: bool
    """
    try:
        kinds = [k.value for k in DigitalTwinKind]
        if kind in kinds:
            return True
        return False
    except Exception as exception:
        return logger.logger_error(exception)
