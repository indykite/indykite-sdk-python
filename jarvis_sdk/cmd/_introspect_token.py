from jarvis_sdk.indykite.identity.v1beta1 import identity_management_api_pb2 as pb2


def introspect_token(self, user_token):
    try:
        response = self.stub.TokenIntrospect(
            pb2.TokenIntrospectRequest(token=user_token)
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    if not response.active:
        return None

    return response.token_info
