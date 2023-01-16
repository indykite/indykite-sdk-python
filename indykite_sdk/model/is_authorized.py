from indykite_sdk.utils import timestamp_to_date
from google.protobuf.json_format import MessageToDict


class IsAuthorizedResponse:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None

        is_authorized_response = IsAuthorizedResponse(
            decision_time=timestamp_to_date(message.decision_time),
            decisions=MessageToDict(message.decisions)
        )

        return is_authorized_response

    def __init__(self, decision_time, decisions):
        self.decision_time = decision_time,
        self.decisions = decisions


class IsAuthorizedResource:

    def __init__(self, id: any, label):
        self.id = id
        self.label = label


class IsAuthorizedDecisions:

    def __init__(self, id: any, label):
        self.id = id
        self.label = label


