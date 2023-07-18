from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
from google.protobuf import struct_pb2
import sys
import indykite_sdk.utils.logger as logger
from indykite_sdk.indykite.identity.v1beta2 import attributes_pb2 as attributes
from indykite_sdk.indykite.identity.v1beta2 import model_pb2 as model
from indykite_sdk.indykite.identity.v1beta2 import import_pb2
from indykite_sdk.model.create_custom_login_token import CreateCustomLoginToken


def create_custom_login_token(self, uid: any, token_claims: dict, session_claims: dict):
    """
    CreateCustomLoginToken creates a signed custom authentication token with the specified user ID
    :param self:
    :param uid: DigitalTwin, PropertyFilter or CredentialReference
    :param token_claims: dictionary
    :param session_claims: dict
    :return: deserialized CreateCustomLoginTokenResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        token_struct = struct_pb2.Struct()
        if token_claims is not None:
            token_struct.update(token_claims)

        session_struct = struct_pb2.Struct()
        if session_claims is not None:
            session_struct.update(session_claims)

        if isinstance(uid, model.DigitalTwin):
            response = self.stub.CreateCustomLoginToken(
                pb2.CreateCustomLoginTokenRequest(
                    digital_twin=uid,
                    token_claims=token_struct,
                    session_claims=session_struct,
                )
            )
        elif isinstance(uid, attributes.PropertyFilter):
            response = self.stub.CreateCustomLoginToken(
                pb2.CreateCustomLoginTokenRequest(
                    property_filter=uid,
                    token_claims=token_struct,
                    session_claims=session_struct,
                )
            )
        elif isinstance(uid, import_pb2.CredentialReference):
            response = self.stub.CreateCustomLoginToken(
                pb2.CreateCustomLoginTokenRequest(
                    credential_reference=uid,
                    token_claims=token_struct,
                    session_claims=session_struct,
                )
            )
        else:
            raise Exception("uid is not valid")
        return CreateCustomLoginToken.deserialize(response) if response else None

    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None
