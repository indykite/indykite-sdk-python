from indykite_sdk.identity import IdentityClient
from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2 as pb2
from indykite_sdk.model.invitation import Invitation
from helpers import data
import uuid
from datetime import datetime


def test_create_email_invitation_wrong_tenant_id(capsys):
    tenant_id = "gid:AAAAAbHLUExsxkqsqRoI93amR30"
    reference_id = str(uuid.uuid4())
    email = "test+testing@indykite.com"

    client = IdentityClient()
    assert client is not None

    response = client.create_email_invitation(tenant_id, reference_id, email, invite_at_time=None, expire_time=None, message_attributes=None)
    captured = capsys.readouterr()
    assert "tenantID is not valid tenant identifier" in captured.err


def test_create_email_invitation_wrong_email(capsys):
    tenant_id = data.get_tenant()
    reference_id = str(uuid.uuid4())
    message_attributes = {"attr1": 12.25}
    email = "test"

    client = IdentityClient()
    assert client is not None

    response = client.create_email_invitation(tenant_id, reference_id, email, invite_at_time=None, expire_time=None,
                                              message_attributes=message_attributes)
    captured = capsys.readouterr()
    assert "invalid CreateInvitationRequest.Email: value length must be between 5 and 255 runes" in captured.err


def test_create_email_invitation_date_past(capsys):
    tenant_id = data.get_tenant()
    reference_id = str(uuid.uuid4())
    email = "test+testing@indykite.com"
    t = datetime.now().timestamp()
    invite_at_time_in_seconds = int(t) - 3600
    expire_time_in_seconds = invite_at_time_in_seconds + 172800
    message_attributes = {"attr1": True}
    client = IdentityClient()
    assert client is not None

    response = client.create_email_invitation(tenant_id, reference_id, email, invite_at_time_in_seconds,
                                              expire_time_in_seconds,
                                              message_attributes)
    captured = capsys.readouterr()
    assert "invalid CreateInvitationRequest.InviteAtTime: value must be greater than now" in captured.err


def test_create_email_invitation_expire_before_invite(capsys):
    tenant_id = data.get_tenant()
    reference_id = str(uuid.uuid4())
    email = "test+testing@indykite.com"
    t = datetime.now().timestamp()
    invite_at_time_in_seconds = int(t) + 3600
    expire_time_in_seconds = invite_at_time_in_seconds - 1800
    message_attributes = {"attr1": bytes("hello", 'utf-8')}
    client = IdentityClient()
    assert client is not None

    response = client.create_email_invitation(tenant_id, reference_id, email, invite_at_time_in_seconds,
                                              expire_time_in_seconds,
                                              message_attributes)
    captured = capsys.readouterr()
    assert "expire_time must be at least 1 hour after invite_at_time" in captured.err


def test_create_email_invitation_wrong_attributes(capsys):
    tenant_id = data.get_tenant()
    reference_id = str(uuid.uuid4())
    email = "test+testing@indykite.com"
    message_attributes = [1,2]
    client = IdentityClient()
    assert client is not None

    response = client.create_email_invitation(tenant_id, reference_id, email, None, None,
                                              message_attributes)
    captured = capsys.readouterr()
    assert "'list' object has no attribute 'items'" in captured.err


def test_create_email_invitation_success(capsys):
    tenant_id = data.get_tenant()
    reference_id = str(uuid.uuid4())
    email = "test+testing@indykite.com"
    t = datetime.now().timestamp()
    invite_at_time_in_seconds = int(t) + 3600
    expire_time_in_seconds = invite_at_time_in_seconds + 172800  # now + 2 days example
    message_attributes = {"attr1": "value1"}

    client = IdentityClient()
    assert client is not None

    response = client.create_email_invitation(tenant_id, reference_id, email, invite_at_time_in_seconds,
                                              expire_time_in_seconds,
                                              message_attributes)

    assert response


def test_create_email_invitation_empty(capsys):
    client = IdentityClient()
    assert client is not None

    tenant_id = data.get_tenant()
    reference_id = str(uuid.uuid4())
    email = "test+testing@indykite.com"

    def mocked_create_email_invitation(request: pb2.CreateInvitationRequest):
        return None

    client.stub.CreateInvitation = mocked_create_email_invitation
    response = client.create_email_invitation(tenant_id, reference_id, email, None, None, None)

    assert response is None


def test_create_mobile_invitation_success(capsys):
    tenant_id = data.get_tenant()
    reference_id = str(uuid.uuid4())
    mobile = "47852369"
    t = datetime.now().timestamp()
    invite_at_time_in_seconds = int(t) + 3600
    expire_time_in_seconds = invite_at_time_in_seconds + 172800  # now + 2 days example
    message_attributes = {"attr1": "value1"}

    client = IdentityClient()
    assert client is not None

    response = client.create_mobile_invitation(tenant_id, reference_id, mobile, invite_at_time_in_seconds,
                                               expire_time_in_seconds, message_attributes)
    captured = capsys.readouterr()
    assert "only email invitation is supported for now" in captured.err


def test_create_mobile_invitation_empty(capsys):
    client = IdentityClient()
    assert client is not None

    tenant_id = data.get_tenant()
    reference_id = str(uuid.uuid4())
    mobile = "47852369"

    def mocked_create_mobile_invitation(request: pb2.CreateInvitationRequest):
        return None

    client.stub.CreateInvitation = mocked_create_mobile_invitation
    response = client.create_mobile_invitation(tenant_id, reference_id, mobile, None, None, None)

    assert response is None


def test_check_invitation_state_success(capsys):
    tenant_id = data.get_tenant()
    reference_id = str(uuid.uuid4())
    email = "test+testing@indykite.com"

    client = IdentityClient()
    assert client is not None

    response = client.create_email_invitation(tenant_id, reference_id, email, None, None, None)
    assert response

    response_check = client.check_invitation_state(reference_id, None)
    assert isinstance(response_check, Invitation)


def test_check_invitation_state_two_identifiers(capsys):
    reference_id = str(uuid.uuid4())
    invitation_token = data.get_expired_token()

    client = IdentityClient()
    assert client is not None

    response_check = client.check_invitation_state(reference_id, invitation_token)
    captured = capsys.readouterr()
    assert "You can not specify both the reference ID and the invitation token" in captured.err


def test_check_invitation_state_no_identifiers(capsys):
    client = IdentityClient()
    assert client is not None

    response_check = client.check_invitation_state(None, None)
    captured = capsys.readouterr()
    assert "You have not specified any identifier: neither reference ID nor invitation token" in captured.err


def test_check_invitation_state_wrong_token(capsys):
    invitation_token = data.get_expired_token()

    client = IdentityClient()
    assert client is not None

    response_check = client.check_invitation_state(None, invitation_token)
    captured = capsys.readouterr()
    assert "invalid token format" in captured.err


def test_check_invitation_state_non_existing_reference(capsys):
    reference_id = str(uuid.uuid4())
    client = IdentityClient()
    assert client is not None

    response_check = client.check_invitation_state(reference_id, None)
    captured = capsys.readouterr()
    assert "invitation not found" in captured.err


def test_resend_invitation_non_existing_reference(capsys):
    reference_id = str(uuid.uuid4())
    client = IdentityClient()
    assert client is not None

    response_resend = client.resend_invitation(reference_id)
    captured = capsys.readouterr()
    assert "invitation does not exist" in captured.err


def test_resend_invitation_success(capsys):
    tenant_id = data.get_tenant()
    reference_id = str(uuid.uuid4())
    email = "test+testing10@indykite.com"

    client = IdentityClient()
    assert client is not None

    response = client.create_email_invitation(tenant_id, reference_id, email, None, None, None)
    assert response

    response_resend = client.resend_invitation(reference_id)
    fields = [desc.name for desc, val in response_resend.ListFields()]
    assert len(fields) == 0


def test_cancel_invitation_non_existing_reference(capsys):
    reference_id = str(uuid.uuid4())
    client = IdentityClient()
    assert client is not None

    response_check = client.cancel_invitation(reference_id)
    captured = capsys.readouterr()
    assert "invitation does not exist" in captured.err


def test_cancel_invitation_success(capsys):
    tenant_id = data.get_tenant()
    reference_id = str(uuid.uuid4())
    email = "test+testing20@indykite.com"

    client = IdentityClient()
    assert client is not None

    response = client.create_email_invitation(tenant_id, reference_id, email, None, None, None)
    assert response

    response_resend = client.cancel_invitation(reference_id)
    fields = [desc.name for desc, val in response_resend.ListFields()]
    assert len(fields) == 0
