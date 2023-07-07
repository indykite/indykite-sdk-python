from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
import sys
from indykite_sdk.utils.logger import handle_excepthook, logger_error
from google.protobuf.timestamp_pb2 import Timestamp
from indykite_sdk.indykite.objects.v1beta1 import struct_pb2 as struct
from indykite_sdk.utils.message_to_value import arg_to_value
from indykite_sdk.model.invitation import Invitation


def create_email_invitation(self,
                            tenant_id,
                            reference_id,
                            email,
                            invite_at_time,
                            expire_time,
                            message_attributes):
    """
    create email invitation
    :param self:
    :param tenant_id: string GID id
    :param reference_id: string
    :param email: string
    :param invite_at_time: google.protobuf.Timestamp
    :param expire_time: google.protobuf.Timestamp
    :param message_attributes: dict
    :return:
    """
    sys.excepthook = handle_excepthook
    try:
        invite_at_time_seconds = None
        if invite_at_time:
            invite_at_time_seconds = Timestamp(seconds=invite_at_time)
        expire_time_seconds = None
        if expire_time:
            expire_time_seconds = Timestamp(seconds=expire_time)
        fields = {}
        if message_attributes:
            for key, value in message_attributes.items():
                fields[key] = arg_to_value(value)

        request = pb2.CreateInvitationRequest(
                tenant_id=str(tenant_id),
                reference_id=str(reference_id),
                email=str(email),
                message_attributes=struct.MapValue(fields=fields),
                invite_at_time=invite_at_time_seconds,
                expire_time=expire_time_seconds
        )
        response = self.stub.CreateInvitation(request)
        if not response:
            return None
        return response

    except Exception as exception:
        return logger_error(exception)


def create_mobile_invitation(self,
                             tenant_id,
                             reference_id,
                             mobile,
                             invite_at_time,
                             expire_time,
                             message_attributes):
    """
    create mobile invitation
    :param self:
    :param tenant_id: string GID id
    :param reference_id: string
    :param mobile: string
    :param invite_at_time: google.protobuf.Timestamp
    :param expire_time: google.protobuf.Timestamp
    :param message_attributes: dict
    :return:
    """
    # mobile not implemented yet
    sys.excepthook = handle_excepthook
    try:
        invite_at_time_seconds = None
        if invite_at_time:
            invite_at_time_seconds = Timestamp(seconds=invite_at_time)
        expire_time_seconds = None
        if expire_time:
            expire_time_seconds = Timestamp(seconds=expire_time)
        fields = {}
        if message_attributes:
            for key, value  in message_attributes.items():
                fields[key] = arg_to_value(value)

        request = pb2.CreateInvitationRequest(
                tenant_id=str(tenant_id),
                reference_id=str(reference_id),
                mobile=str(mobile),
                message_attributes=struct.MapValue(fields=fields),
                invite_at_time=invite_at_time_seconds,
                expire_time=expire_time_seconds
        )
        response = self.stub.CreateInvitation(request)
        if not response:
            return None
        return response

    except Exception as exception:
        return logger_error(exception)


def check_invitation_state(self, reference_id, invitation_token):
    """
    check invitation state: check with either reference_id or invitation_token
    :param self:
    :param reference_id: string
    :param invitation_token: token used in invitation url as string
    :return: deserialized CheckInvitationStateResponse.invitation
    """
    sys.excepthook = handle_excepthook
    try:
        if reference_id and invitation_token:
            return logger_error("You can not specify both the reference ID and the invitation token")
        elif not reference_id and not invitation_token:
            return logger_error("You have not specified any identifier: neither reference ID nor invitation token")
        response = self.stub.CheckInvitationState(
            pb2.CheckInvitationStateRequest(
                reference_id=reference_id,
                invitation_token=invitation_token
            )
        )
        return Invitation.deserialize(response.invitation)
    except Exception as exception:
        return logger_error(exception)


def resend_invitation(self, reference_id):
    """
    resend invitation
    :param self:
    :param reference_id: string
    :return: ResendInvitationResponse
    """
    sys.excepthook = handle_excepthook
    try:
        response = self.stub.ResendInvitation(
            pb2.ResendInvitationRequest(
                reference_id=reference_id
            )
        )
        return response
    except Exception as exception:
        return logger_error(exception)


def cancel_invitation(self, reference_id):
    """
    cancel invitation
    :param self:
    :param reference_id: string
    :return: CancelInvitationResponse
    """
    sys.excepthook = handle_excepthook
    try:
        response = self.stub.CancelInvitation(
            pb2.CancelInvitationRequest(
                reference_id=reference_id
            )
        )
        return response
    except Exception as exception:
        return logger_error(exception)
