from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
from indykite_sdk.model.token_info import TokenInfo
from indykite_sdk.model.session_introspect import SessionIntrospect
import sys
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

    return TokenInfo.deserialize(response.token_info)


def session_introspect(self, tenant_id, access_token):
    """
    session introspection
    :param self:
    :param tenant_id: string GID id
    :param access_token: user's authentication token
    :return: deserialized SessionIntrospectResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.SessionIntrospect(pb2.SessionIntrospectRequest(tenant_id=tenant_id, token=access_token))
        if not response :
            return None
        return SessionIntrospect.deserialize(response)
    except Exception as exception:
        return logger.logger_error(exception)
