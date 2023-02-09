from indykite_sdk.indykite.identity.v1beta1 import identity_management_api_pb2 as pb2
from indykite_sdk.model.token_info import TokenInfo
import sys
import indykite_sdk.utils.logger as logger


def introspect_token(self, user_token):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.TokenIntrospect(pb2.TokenIntrospectRequest(token=user_token))
    except Exception as exception:
        return logger.logger_error(exception)

    if not response or not response.active:
        return None

    return TokenInfo.deserialize(response.token_info)
