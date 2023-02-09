from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.service_account import ServiceAccount
from indykite_sdk.indykite.config.v1beta1.model_pb2 import UniqueNameIdentifier
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from indykite_sdk.model.create_service_account import CreateServiceAccount
from indykite_sdk.model.update_service_account import UpdateServiceAccount
import sys
import indykite_sdk.utils.logger as logger


def get_service_account(self,service_account=None):
    sys.excepthook = logger.handle_excepthook
    try:
        if service_account:
            service_account_id = str(service_account)
        else:
            if self.credentials and self.credentials.get('serviceAccountId'):
                service_account_id = self.credentials.get('serviceAccountId')
            else:
                raise Exception("Missing service account")
    except Exception as exception:
        return logger.logger_error(exception)

    try:
        response = self.stub.ReadServiceAccount(
            pb2.ReadServiceAccountRequest(
                id=str(service_account_id)
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    service_account = ServiceAccount.deserialize(response.service_account)

    return service_account


def get_service_account_by_name(self, customer_id, service_account_name):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.ReadServiceAccount(
            pb2.ReadServiceAccountRequest(
                name=UniqueNameIdentifier(location=customer_id, name=service_account_name)
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return ServiceAccount.deserialize(response.service_account)


def create_service_account(self, customer_id, name, display_name, description="", role="", bookmarks=[]):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.CreateServiceAccount(
            pb2.CreateServiceAccountRequest(
                location=customer_id,name=name, display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description), role=role, bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return CreateServiceAccount.deserialize(response)


def update_service_account(self, service_account_id, etag, display_name, description="", bookmarks=[]):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.UpdateServiceAccount(
            pb2.UpdateServiceAccountRequest(
                id=service_account_id,etag=wrappers.StringValue(value=etag),
                display_name=wrappers.StringValue(value=display_name),
                description=wrappers.StringValue(value=description), bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return UpdateServiceAccount.deserialize(response)


def delete_service_account(self, service_account_id, etag, bookmarks):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.DeleteServiceAccount(
            pb2.DeleteServiceAccountRequest(
                id=service_account_id, etag=wrappers.StringValue(value=etag),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return response
