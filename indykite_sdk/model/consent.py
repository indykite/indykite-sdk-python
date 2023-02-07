from indykite_sdk.utils import timestamp_to_date
from google.protobuf.json_format import MessageToDict


class PiiProcessor:
    def __init__(self, pii_processor_id, display_name):
        self.pii_processor_id = pii_processor_id
        self.display_name = display_name
        self.description = None
        self.owner = None
        self.policy_uri = None
        self.terms_of_service_uri = None
        self.client_uri = None
        self.logo_uri = None
        self.user_support_email_address = None
        self.additional_contacts = None


class PiiController:
    def __init__(self, pii_controller_id, display_name):
        self.pii_controller_id = pii_controller_id
        self.display_name = display_name


class ConsentReceipt:
    def __init__(self, pii_principal_id, pii_processor):
        self.pii_principal_id = pii_principal_id
        self.pii_processor = pii_processor
        self.items = None


class Item:
    def __init__(self, consent_id, pii_controller, consented_at_time, properties):
        self.consent_id = consent_id
        self.pii_controller = pii_controller
        self.consented_at_time = consented_at_time
        self.properties = properties


class CreateConsentRequest:
    def __init__(self, pii_processor_id, pii_principal_id, properties):
        self.pii_processor_id = pii_processor_id
        self.pii_principal_id = pii_principal_id
        self.properties = properties


class CreateConsentResponse:
    @classmethod
    def deserialize(cls, message):
        if message is None:

            return None

        create_consent = CreateConsentResponse(
            str(message.consent_id),
        )

        return create_consent

    def __init__(self, consent_id):
        self.consent_id = consent_id


class ConsentApproval:
    def __init__(self, grant_scopes, granted_audiences, session, remember, remember_for):
        self.grant_scopes = grant_scopes
        self.granted_audiences = granted_audiences
        self.session = session
        self.remember = remember
        self.remember_for = remember_for


class ConsentRequestSessionData:
    def __init__(self, access_token, id_token, userinfo):
        self.access_token = access_token
        self.id_token = id_token
        self.userinfo = userinfo

