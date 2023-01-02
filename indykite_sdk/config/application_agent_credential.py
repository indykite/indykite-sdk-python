from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.application_agent_credential import ApplicationAgentCredential
from indykite_sdk.model.register_application_agent_credential import RegisterApplicationAgentCredential
from google.protobuf.timestamp_pb2 import Timestamp


def get_application_agent_credential(self, application_agent_credential_id):
    try:
        response = self.stub.ReadApplicationAgentCredential(
            pb2.ReadApplicationAgentCredentialRequest(
                id=str(application_agent_credential_id)
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return ApplicationAgentCredential.deserialize(response.application_agent_credential)


def register_application_agent_credential_jwk(self, application_agent_id, display_name, jwk_in_bytes, expire_time_in_seconds,
                                              default_tenant_id, bookmarks=[]):

    try:
        response = self.stub.RegisterApplicationAgentCredential(
            pb2.RegisterApplicationAgentCredentialRequest(
                application_agent_id=application_agent_id, display_name=display_name,
                jwk=jwk_in_bytes, expire_time=Timestamp(seconds=expire_time_in_seconds),
                default_tenant_id=str(default_tenant_id), bookmarks=bookmarks
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return RegisterApplicationAgentCredential.deserialize(response)


def register_application_agent_credential_pem(self, application_agent_id, display_name, pem_in_bytes, expire_time_in_seconds,
                                              default_tenant_id, bookmarks=[]):

    try:
        response = self.stub.RegisterApplicationAgentCredential(
            pb2.RegisterApplicationAgentCredentialRequest(
                application_agent_id=application_agent_id, display_name=display_name,
                pem=pem_in_bytes, expire_time=Timestamp(seconds=expire_time_in_seconds),
                default_tenant_id=str(default_tenant_id), bookmarks=bookmarks
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return RegisterApplicationAgentCredential.deserialize(response)


def delete_application_agent_credential(self, application_agent_credential_id, bookmarks):

    try:
        response = self.stub.DeleteApplicationAgentCredential(
            pb2.DeleteApplicationAgentCredentialRequest(
                id=application_agent_credential_id, bookmarks=bookmarks
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return response
