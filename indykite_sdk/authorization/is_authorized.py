from indykite_sdk.indykite.authorization.v1beta1 import authorization_service_pb2 as pb2
from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2_ident
from indykite_sdk.indykite.identity.v1beta2 import model_pb2 as model
from indykite_sdk.indykite.objects.v1beta1 import struct_pb2 as pb2_struct


def is_authorized_digital_twin(self, digital_twin_id, tenant_id, resources=[], actions=[]):
    try:
        response = self.stub.IsAuthorized(
            pb2.IsAuthorizedRequest(
                digital_twin_identifier=pb2_ident.DigitalTwinIdentifier(
                    digital_twin=model.DigitalTwin(
                        id=str(digital_twin_id),
                        tenant_id=str(tenant_id)
                    )
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


def is_authorized_property_filter(self, type_filter, value, resources=[], actions=[]):
    try:
        response = self.stub.IsAuthorized(
            pb2.IsAuthorizedRequest(
                digital_twin_identifier=pb2_ident.DigitalTwinIdentifier(
                    property_filter=pb2_ident.PropertyFilter(
                        type=str(type_filter),
                        value=pb2_struct.Value(string_value=value)
                    )
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
