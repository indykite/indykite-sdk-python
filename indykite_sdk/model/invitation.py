from indykite_sdk.indykite.identity.v1beta2.model_pb2 import Invitation, DigitalTwin
from indykite_sdk.utils import timestamp_to_date
from google.protobuf.json_format import MessageToDict


class Invitation:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        invitation = Invitation(
            tenant_id=str(message.tenant_id),
            reference_id = str(message.reference_id),
            state = message.state)
        if message.HasField('invite_at_time'):
            invitation.invite_at_time = timestamp_to_date(message.invite_at_time)
        if message.HasField('expire_time'):
            invitation.expire_time = timestamp_to_date(message.expire_time)
        if message.HasField('message_attributes'):
            invitation.message_attributes = MessageToDict(message.message_attributes)
        if message.HasField('accepted_by'):
            invitation.accepted_by = DigitalTwin(id=message.accepted_by.id,
                                                 tenant_id=message.accepted_by.tenant_id,
                                                 kind=message.accepted_by.kind,
                                                 state=message.accepted_by.state,
                                                 tags=message.accepted_by.tags)

        if message.HasField('email'):
            invitation.email = str(message.email)
        if message.HasField('mobile'):
            invitation.mobile = str(message.mobile)

        return invitation

    def __init__(self, tenant_id, reference_id, state):

        self.tenant_id = tenant_id
        self.reference_id = reference_id
        self.state = state
        self.invite_at_time = None
        self.expire_time = None
        self.message_attributes = None
        self.accepted_by = None
        self.email = None
        self.mobile = None
