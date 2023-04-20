from indykite_sdk.utils import timestamp_to_date
from google.protobuf.json_format import MessageToJson, MessageToDict
import indykite_sdk.utils.logger as logger


class WhoAuthorizedResponse:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None

        try:
            message_dict = MessageToDict(message, preserving_proto_field_name=True)
            if message_dict and message_dict["decisions"]:
                who_authorized_response = WhoAuthorizedResponse(
                    decision_time=timestamp_to_date(message.decision_time),
                    decisions=message_dict["decisions"]
                )
            return who_authorized_response
        except Exception as exception:
            return logger.logger_error(exception)

    def __init__(self, decision_time, decisions):
        self.decision_time = decision_time,
        self.decisions = decisions


class WhoAuthorizedResource:

    def __init__(self, id: any, type, actions=[]):
        self.id = id
        self.type = type
        self.actions = actions


class WhoAuthorizedResponseResourceType:

    def __init__(self, resources={}):
        self.resources = resources


class WhoAuthorizedResponseResource:

    def __init__(self, actions={}):
        self.actions = actions


class WhoAuthorizedResponseAction:
    def __init__(self, subjects=[]):
        self.subjects = subjects


class WhoAuthorizedResponseSubject:
    def __init__(self, external_id=None):
        self.external_id = external_id
