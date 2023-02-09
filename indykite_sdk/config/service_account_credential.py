from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.service_account_credential import ServiceAccountCredential
from indykite_sdk.model.register_service_account_credential import RegisterServiceAccountCredential
from google.protobuf.timestamp_pb2 import Timestamp
import sys
import indykite_sdk.utils.logger as logger


def get_service_account_credential(self, service_account_credential_id):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.ReadServiceAccountCredential(
            pb2.ReadServiceAccountCredentialRequest(
                id=str(service_account_credential_id)
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return ServiceAccountCredential.deserialize(response.service_account_credential)


def register_service_account_credential_jwk(self, service_account_id, display_name, jwk_in_bytes, expire_time_in_seconds,
                                            bookmarks=[]):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.RegisterServiceAccountCredential(
            pb2.RegisterServiceAccountCredentialRequest(
                service_account_id=service_account_id, display_name=display_name,
                jwk=jwk_in_bytes, expire_time=Timestamp(seconds=expire_time_in_seconds),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return RegisterServiceAccountCredential.deserialize(response)


def register_service_account_credential_pem(self, service_account_id, display_name, pem_in_bytes, expire_time_in_seconds,
                                            bookmarks=[]):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.RegisterServiceAccountCredential(
            pb2.RegisterServiceAccountCredentialRequest(
                service_account_id=service_account_id, display_name=display_name,
                pem=pem_in_bytes, expire_time=Timestamp(seconds=expire_time_in_seconds),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return RegisterServiceAccountCredential.deserialize(response)


def delete_service_account_credential(self, service_account_credential_id, bookmarks):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.DeleteServiceAccountCredential(
            pb2.DeleteServiceAccountCredentialRequest(
                id=service_account_credential_id, bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return response
