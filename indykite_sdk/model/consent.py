from google.protobuf.json_format import MessageToDict
from indykite_sdk.utils import timestamp_to_date
from indykite_sdk.model.digital_twin import DigitalTwin
from indykite_sdk.model.scope_item import ScopeItem
from indykite_sdk.model.audience_item import AudienceItem


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


class CheckOAuth2ConsentChallengeResponse:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        check_challenge = CheckOAuth2ConsentChallengeResponse(
            str(message.client_id),
            str(message.app_space_id)
        )
        if "audiences" in fields:
            check_challenge.audiences = []
            for r in message.audiences:
                check_challenge.audiences.append(AudienceItem(
                    r.user_support_email_address if r.user_support_email_address else None,
                    r.client_id if r.user_support_email_address else None,
                    r.display_name if r.client_id else None,
                    r.description if r.description else None,
                    r.logo_url if r.logo_url else None,
                    r.homepage_url if r.homepage_url else None,
                    r.privacy_policy_url if r.privacy_policy_url else None,
                    r.tos_url if r.tos_url else None
                ))
        if "scopes" in fields:
            check_challenge.scopes = [
                ScopeItem(
                    r.name if r.name else None,
                    r.display_name if r.display_name else None,
                    r.description if r.description else None,
                    r.required if r.required else None
                )
                for r in message.scopes
            ]
        if "acrs" in fields:
            check_challenge.acrs = [
                str(r)
                for r in message.acrs
            ]
        if "request_url" in fields:
            check_challenge.request_url = str(message.request_url)
        if "skip" in fields:
            check_challenge.skip = bool(message.skip)
        if "digital_twin" in fields:
            check_challenge.digital_twin = DigitalTwin(message.digital_twin.id, message.digital_twin.tenant_id,
                                                       message.digital_twin.kind, message.digital_twin.state,[])
        if "subject_identifier" in fields:
            check_challenge.subject_identifier = str(message.subject_identifier)
        if "authenticated_at" in fields:
            check_challenge.authenticated_at = timestamp_to_date(message.authenticated_at)
        if "requested_at" in fields:
            check_challenge.requested_at = timestamp_to_date(message.requested_at)
        if "context" in fields:
            check_challenge.context = MessageToDict(message.context)
        return check_challenge

    def __init__(self, client_id, app_space_id):
        self.client_id = client_id
        self.app_space_id = app_space_id
        self.audiences = None
        self.scopes = None
        self.acrs = None
        self.request_url = None
        self.skip = None
        self.digital_twin = None
        self.subject_identifier = None
        self.authenticated_at = None
        self.requested_at = None
        self.context = None


class CreateOAuth2ConsentVerifierResponse:
    @classmethod
    def deserialize(cls, message):
        if message is None:
            return None
        fields = [desc.name for desc, val in message.ListFields()]
        consent_verifier = CreateOAuth2ConsentVerifierResponse(
            str(message.verifier) if message.verifier else None,
            str(message.authorization_endpoint) if message.authorization_endpoint else None
        )
        return consent_verifier

    def __init__(self, verifier=None, authorization_endpoint=None):
        self.verifier = verifier
        self.authorization_endpoint = authorization_endpoint
