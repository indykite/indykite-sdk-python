from indykite_sdk.indykite.authorization.v1beta1 import authorization_service_pb2 as pb2
from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2_ident


def is_authorized_token(self, access_token, resources=[], actions=[]):
    try:
        response = self.stub.IsAuthorized(
            pb2.IsAuthorizedRequest(
                digital_twin_identifier=pb2_ident.DigitalTwinIdentifier(
                    access_token=str(access_token)
                ),
                resources=request_resource(resources),
                actions=actions
            )
        )
    except Exception as exception:
        print(exception)
        return None

    if not response:
        return None

    return response


def request_resource(resources):
    res = []
    for r in resources:
        res.append(pb2.IsAuthorizedRequest.Resource(id=r.id, label=r.label))
    return res
