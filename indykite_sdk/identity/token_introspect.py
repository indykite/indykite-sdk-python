import sys
from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
from indykite_sdk.model.token_info import IdentityTokenInfo, ThirdPartyIdentityTokenInfo
import indykite_sdk.utils.logger as logger


def token_introspect(self, user_token):
    """
    token introspection
    :param self:
    :param user_token: user's authentication token
    :return: deserialized TokenInfo object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.TokenIntrospect(pb2.TokenIntrospectRequest(token=user_token))
    except Exception as exception:
        return logger.logger_error(exception)

    if not response or not response.active:
        return None

    if response.identity_token_info:
        return IdentityTokenInfo.deserialize(response.identity_token_info)
    elif response.third_party_identity_token:
        return ThirdPartyIdentityTokenInfo.deserialize(response.third_party_identity_token)
    return None
