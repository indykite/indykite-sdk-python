import uuid

from indykite_sdk.identity import helper
from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
from indykite_sdk.indykite.identity.v1beta2 import model_pb2 as model
from indykite_sdk.utils.deserialize_digital_twin_with_token_info import deserialize_digital_twin_with_token_info
from indykite_sdk.utils.message_to_value import arg_to_value
from indykite_sdk.indykite.identity.v1beta2 import attributes_pb2 as attributes
import sys
import indykite_sdk.utils.logger as logger


def get_digital_twin(self, digital_twin_id, tenant_id, fields):
    """
    get a digital twin with a DigitalTwin object
    :param self:
    :param digital_twin_id: string gid id
    :param tenant_id: string gid id
    :param fields: [] of PropertyMask
    :return: deserialized GetDigitalTwinResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.GetDigitalTwin(
            pb2.GetDigitalTwinRequest(
                id=model.DigitalTwinIdentifier(
                    digital_twin=model.DigitalTwin(
                        id=str(digital_twin_id),
                        tenant_id=str(tenant_id)
                    )
                ),
                properties=helper.create_property_mask(fields)
            )
        )
        return deserialize_digital_twin_with_token_info(response)
    except Exception as exception:
        return logger.logger_error(exception)


def get_digital_twin_by_token(self, token, fields):
    """
    get a digital twin with its token
    :param self:
    :param token: string
    :param fields: [] of PropertyMask
    :return: deserialized GetDigitalTwinResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        if len(token) < 32:
            raise Exception("Token must be 32 chars or more.")
    except Exception as exception:
        return logger.logger_error(exception)

    try:
        response = self.stub.GetDigitalTwin(
                pb2.GetDigitalTwinRequest(
                    id=model.DigitalTwinIdentifier(access_token=token),
                    properties=helper.create_property_mask(fields)
                )
        )
        return deserialize_digital_twin_with_token_info(response)
    except Exception as exception:
        return logger.logger_error(exception)


def get_digital_twin_by_property(self, property_filter, fields):
    """
    get a digital twin with a filter on its properties
    :param self:
    :param property_filter: PropertyFilter object
    :param fields: [] of PropertyMask
    :return: deserialized GetDigitalTwinResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.GetDigitalTwin(
                pb2.GetDigitalTwinRequest(
                    id=model.DigitalTwinIdentifier(property_filter=property_filter),
                    properties=helper.create_property_mask(fields)
                )
        )
        return deserialize_digital_twin_with_token_info(response)
    except Exception as exception:
        return logger.logger_error(exception)


def property_filter(self, type, value, tenant_id):
    """
    create PropertyFilter object
    :param self:
    :param type: string
    :param value: Value
    :param tenant_id: string gid
    :return: PropertyFilter object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        property_filter = attributes.PropertyFilter(
            type=type,
            value=arg_to_value(value),
            tenant_id=tenant_id
        )
        return property_filter
    except Exception as exception:
        return logger.logger_error(exception)
