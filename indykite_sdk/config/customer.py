from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.customer import Customer


def get_customer_by_id(self, customer_id):
    try:
        response = self.stub.ReadCustomer(
            pb2.ReadCustomerRequest(
                id=str(customer_id)
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return Customer.deserialize(response.customer)


def get_customer_by_name(self, customer_name):

    try:
        response = self.stub.ReadCustomer(
            pb2.ReadCustomerRequest(
                name=str(customer_name)
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return Customer.deserialize(response.customer)


