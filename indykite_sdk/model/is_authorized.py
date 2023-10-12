from indykite_sdk.utils import timestamp_to_date
from google.protobuf.json_format import MessageToJson, MessageToDict
import indykite_sdk.utils.logger as logger


class IsAuthorizedResponse:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None

        try:
            message_dict = MessageToDict(message, preserving_proto_field_name=True)
            if message_dict and message_dict["decisions"]:
                is_authorized_response = IsAuthorizedResponse(
                    decision_time=timestamp_to_date(message.decision_time),
                    decisions=message_dict["decisions"]
                )
            return is_authorized_response
        except Exception as exception:
            return logger.logger_error(exception)

    def __init__(self, decision_time, decisions):
        self.decision_time = decision_time,
        self.decisions = decisions


class IsAuthorizedResource:

    def __init__(self, external_id: any, type, actions=[]):
        self.external_id = external_id
        self.type = type
        self.actions = actions


class IsAuthorizedResourceTypeResponse:

    def __init__(self, resources={}):
        self.resources = resources


class IsAuthorizedResourceResponse:

    def __init__(self, actions={}):
        self.actions = actions


class IsAuthorizedActionResponse:
    def __init__(self, allow=False):
        self.allow = allow
