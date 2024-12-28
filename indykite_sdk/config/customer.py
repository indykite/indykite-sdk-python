from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.customer import Customer
import sys
import indykite_sdk.utils.logger as logger


def read_customer_by_id(self, customer_id):
    """
    get Customer object from customer id
    :param self:
    :param customer_id: string gid id
    :return: Customer object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.ReadCustomer(
            pb2.ReadCustomerRequest(
                id=str(customer_id)
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return Customer.deserialize(response.customer)


def read_customer_by_name(self, customer_name):
    """
    get Customer object from customer name
    :param self:
    :param customer_name: string
    :return: Customer object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.ReadCustomer(
            pb2.ReadCustomerRequest(
                name=str(customer_name)
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return Customer.deserialize(response.customer)
