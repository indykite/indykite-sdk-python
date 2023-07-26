from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.customer import Customer
from indykite_sdk.model.read_customer_config import ReadCustomerConfig
from indykite_sdk.model.update_customer_config import UpdateCustomerConfig
from indykite_sdk.indykite.config.v1beta1.model_pb2 import CustomerConfig
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
import sys
import indykite_sdk.utils.logger as logger


def read_customer_by_id(self, customer_id, bookmarks=[]):
    """
    get Customer object from customer id
    :param self:
    :param customer_id: string gid id
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: Customer object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.ReadCustomer(
            pb2.ReadCustomerRequest(
                id=str(customer_id),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return Customer.deserialize(response.customer)


def read_customer_by_name(self, customer_name, bookmarks=[]):
    """
    get Customer object from customer name
    :param self:
    :param customer_name: string
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: Customer object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.ReadCustomer(
            pb2.ReadCustomerRequest(
                name=str(customer_name),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return Customer.deserialize(response.customer)


def read_customer_config(self, customer_id, bookmarks=[]):
    """
    get CustomerConfig object from customer id
    :param self:
    :param customer_id: string gid id
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized ReadCustomerConfigResponse object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.ReadCustomerConfig(
            pb2.ReadCustomerConfigRequest(
                id=str(customer_id),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return ReadCustomerConfig.deserialize(response)


def update_customer_config(self, customer_id, etag, customer_config, bookmarks=[]):
    """
    get CustomerConfig object from customer id
    :param self:
    :param customer_id: string gid id
    :param etag: string
    :param customer_config: CustomerConfig
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized UpdateCustomerConfigResponse object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.UpdateCustomerConfig(
            pb2.UpdateCustomerConfigRequest(
                id=str(customer_id),
                etag=wrappers.StringValue(value=etag),
                config=customer_config,
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
    return UpdateCustomerConfig.deserialize(response)


def create_customer_config(self, default_auth_flow_id=None, default_email_service_id=None):
    """
    get CustomerConfig object from default_auth_flow_id or default_email_service_id
    :param self:
    :param default_auth_flow_id: string gid id
    :param default_email_service_id: string gid id
    :return: customer_config: CustomerConfig
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = CustomerConfig(
            default_auth_flow_id=default_auth_flow_id,
            default_email_service_id=default_email_service_id
        )
        return response
    except Exception as exception:
        return logger.logger_error(exception)
