from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.application_agent_credential import ApplicationAgentCredential
from indykite_sdk.model.register_application_agent_credential import RegisterApplicationAgentCredential
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from google.protobuf.timestamp_pb2 import Timestamp
import sys
import indykite_sdk.utils.logger as logger


def read_application_agent_credential(self, application_agent_credential_id, bookmarks=[]):
    """

    :param self:
    :param application_agent_credential_id: string gid id
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: Application AgentCredential object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.ReadApplicationAgentCredential(
            pb2.ReadApplicationAgentCredentialRequest(
                id=str(application_agent_credential_id),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return ApplicationAgentCredential.deserialize(response.application_agent_credential)


def register_application_agent_credential_jwk(self,
                                              application_agent_id,
                                              display_name,
                                              jwk_in_bytes,
                                              expire_time_in_seconds,
                                              default_tenant_id,
                                              bookmarks=[]):
    """
    register jwk credentials for your AppAgent
    :param self:
    :param application_agent_id: string gid id
    :param display_name: string
    :param jwk_in_bytes: bytes
    :param expire_time_in_seconds: int
    :param default_tenant_id: string gid id
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return: deserialized RegisterApplicationAgentCredential
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.RegisterApplicationAgentCredential(
            pb2.RegisterApplicationAgentCredentialRequest(
                application_agent_id=application_agent_id,
                display_name=display_name,
                jwk=jwk_in_bytes,
                expire_time=Timestamp(seconds=expire_time_in_seconds),
                default_tenant_id=str(default_tenant_id),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return RegisterApplicationAgentCredential.deserialize(response)


def register_application_agent_credential_pem(self,
                                              application_agent_id,
                                              display_name,
                                              pem_in_bytes,
                                              expire_time_in_seconds,
                                              default_tenant_id,
                                              bookmarks=[]):
    """
    register pem credentials for your AppAgent
    :param self:
    :param application_agent_id: string gid id
    :param display_name: string
    :param pem_in_bytes: bytes
    :param expire_time_in_seconds: int
    :param default_tenant_id: string gid id
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :return:
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.RegisterApplicationAgentCredential(
            pb2.RegisterApplicationAgentCredentialRequest(
                application_agent_id=application_agent_id,
                display_name=display_name,
                pem=pem_in_bytes,
                expire_time=Timestamp(seconds=expire_time_in_seconds),
                default_tenant_id=str(default_tenant_id),
                bookmarks=bookmarks
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return RegisterApplicationAgentCredential.deserialize(response)


def delete_application_agent_credential(self, application_agent_credential_id, bookmarks, etag):
    """
    delete AppAgent credentials
    :param self:
    :param application_agent_credential_id: string gid id
    :param bookmarks: list of strings with pattern: ^[a-zA-Z0-9_-]{40,}$
    :param etag: string
    :return: DeleteApplicationAgentCredentialResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.DeleteApplicationAgentCredential(
            pb2.DeleteApplicationAgentCredentialRequest(
                id=application_agent_credential_id,
                bookmarks=bookmarks,
                etag=wrappers.StringValue(value=etag)
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return response
