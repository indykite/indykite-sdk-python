from indykite_sdk.utils import timestamp_to_date
from google.protobuf.json_format import MessageToJson, MessageToDict


class IsAuthorizedResponse:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None

        message_dict = MessageToDict(message, preserving_proto_field_name=True)
        if message_dict and message_dict["decisions"]:
            is_authorized_response = IsAuthorizedResponse(
                decision_time=timestamp_to_date(message.decision_time),
                decisions=message_dict["decisions"]
            )
        else:
            is_authorized_response = IsAuthorizedResponse(decision_time=None, decisions={})
        return is_authorized_response

    def __init__(self, decision_time, decisions):
        self.decision_time = decision_time,
        self.decisions = decisions


class IsAuthorizedResource:

    def __init__(self, id: any, label):
        self.id = id
        self.label = label


class IsAuthorizedDecisions:
    def __init__(self, decision, allow_action):
        self.decision = decision
        self.allow_action = allow_action


class IsAuthorizedActions:
    def __init__(self, action, is_allowed):
        self.action = action
        self.is_allowed = is_allowed

