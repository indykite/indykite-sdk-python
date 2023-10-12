from indykite_sdk.indykite.authorization.v1beta1 import authorization_service_pb2 as pb2
from indykite_sdk.indykite.authorization.v1beta1 import model_pb2 as pb2_model
from indykite_sdk.model.who_authorized import WhoAuthorizedResponse
import sys
import indykite_sdk.utils.logger as logger


def who_authorized(self,  resources=[], input_params={}, policy_tags=[]):
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.WhoAuthorized(
            pb2.WhoAuthorizedRequest(
                resources=request_resource(resources),
                input_params=request_input_params(input_params),
                policy_tags=policy_tags
            )
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return WhoAuthorizedResponse.deserialize(response)


def request_resource(resources):
    return [
        pb2.WhoAuthorizedRequest.Resource(external_id=r.external_id, type=r.type, actions=list(r.actions))
        for r in resources
    ]


def request_input_params(input_params):
    input_params_dict = {
        k: pb2_model.InputParam(string_value=str(v))
        for k, v in input_params.items()
    }
    return input_params_dict
