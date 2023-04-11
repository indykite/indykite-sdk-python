from indykite_sdk.utils import timestamp_to_date
from google.protobuf.json_format import MessageToJson, MessageToDict
import indykite_sdk.utils.logger as logger


class WhatAuthorizedResponse:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None

        try:
            message_dict = MessageToDict(message, preserving_proto_field_name=True)
            if message_dict and message_dict["decisions"]:
                what_authorized_response = WhatAuthorizedResponse(
                    decision_time=timestamp_to_date(message.decision_time),
                    decisions=message_dict["decisions"]
                )
            return what_authorized_response
        except Exception as exception:
            return logger.logger_error(exception)

    def __init__(self, decision_time, decisions):
        self.decision_time = decision_time,
        self.decisions = decisions


class WhatAuthorizedResourceTypes:
    def __init__(self, type, actions=[]):
        self.type = type
        self.actions = actions


class WhatAuthorizedDecisions:
    def __init__(self, decision, allow_action):
        self.decision = decision
        self.allow_action = allow_action


class WhatAuthorizedResponseActions:
    def __init__(self, resources=[]):
        self.resources = resources


class WhatAuthorizedResponseResources:
    def __init__(self, external_id):
        self.external_id = external_id


class WhatAuthorizedResponseResourceTypes:
    def __init__(self, actions={}):
        self.type = type
        self.actions = actions
