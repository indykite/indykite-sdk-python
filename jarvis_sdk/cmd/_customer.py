import uuid

from jarvis_sdk.cmd import helper
from jarvis_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from jarvis_sdk.indykite.config.v1beta1 import model_pb2 as model


def get_customer_by_id(self, customer_id, token):
    try:
        customer = uuid.UUID(customer_id, version=4)
    except Exception as exception:
        print("The customer id is not in UUID4 format:")
        print(exception)
        return None

    try:
        response = self.config_stub.ReadCustomer(
            pb2.ReadCustomerRequest(
                id=customer_id
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return response

