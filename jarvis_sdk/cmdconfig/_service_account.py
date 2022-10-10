from jarvis_sdk.cmdconfig import helper
from jarvis_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from jarvis_sdk.indykite.config.v1beta1 import model_pb2 as model
from jarvis_sdk.model.service_account import ServiceAccount


def get_service_account(self,service_account=None):
    try:
        if service_account:
            service_account_id = str(service_account)
        else:
            if self.credentials.get('serviceAccountId'):
                service_account_id = self.credentials.get('serviceAccountId')
            else:
                raise Exception("Missing service account")
    except Exception as exception:
        print(exception)
        return None

    try:
        response = self.stub.ReadServiceAccount(
            pb2.ReadServiceAccountRequest(
                id=str(service_account_id)
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    service_account = ServiceAccount.deserialize(response.service_account)

    return service_account

