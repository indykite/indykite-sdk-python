from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
from google.protobuf import struct_pb2
import sys
import indykite_sdk.utils.logger as logger


def enrich_token(self, user_token: str, token_claims: dict, session_claims: dict):
    """
    enrich token
    :param self:
    :param user_token: dict
    :param token_claims: dict
    :param session_claims: dict
    :return: EnrichTokenResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        token_struct = struct_pb2.Struct()
        if token_claims is not None:
            token_struct.update(token_claims)

        session_struct = struct_pb2.Struct()
        if session_claims is not None:
            session_struct.update(session_claims)

        response = self.stub.EnrichToken(
            pb2.EnrichTokenRequest(
                access_token=user_token,
                token_claims=token_struct,
                session_claims=session_struct,
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return response
