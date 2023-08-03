import sys
from indykite_sdk.utils import jwt_credentials
from indykite_sdk.utils.logger import handle_excepthook, logger_error


class IdentityClient(object):

    def __init__(self, local=False, token_source=None):
        sys.excepthook = handle_excepthook
        try:
            self.channel, self.stub, self.credentials, self.token_source = jwt_credentials.get_credentials(
                client="identity",
                local=local,
                token_source=token_source
            )
        except Exception as exception:
            return logger_error(exception)

    # Imported methods
    from .change_password import change_password_of_user, change_password
    from .get_digital_twin import get_digital_twin_by_token, get_digital_twin, get_digital_twin_by_property, \
        property_filter
    from .token_introspect import token_introspect, session_introspect
    from .patch_properties import patch_properties_by_token, patch_properties
    from .verification import start_digital_twin_email_verification, verify_digital_twin_email
    from .delete import del_digital_twin, del_digital_twin_by_token, del_digital_twin_by_property
    from .enrich_token import enrich_token
    from .import_digital_twins import import_digital_twins
    from .consent import create_consent, list_consents, revoke_consent, check_oauth2_consent_challenge, \
        create_oauth2_consent_verifier_approval, create_oauth2_consent_verifier_denial
    from .forgotten_password import start_forgotten_password_flow
    from .invitation import create_email_invitation, create_mobile_invitation, check_invitation_state, resend_invitation, cancel_invitation
    from .register_digital_twins_no_cred import register_digital_twin_without_credential
    from .create_custom_login_token import create_custom_login_token
