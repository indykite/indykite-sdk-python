import certifi
import grpc
import os
import sys
from indykite_sdk.identity import helper
from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2_grpc as pb2_grpc


class IdentityClient(object):

    def __init__(self, local=False):
        try:
            cred = os.getenv('INDYKITE_APPLICATION_CREDENTIALS')
            # Load the config from File (secondary)
            if not cred:
                cred = os.getenv('INDYKITE_APPLICATION_CREDENTIALS_FILE')
                if not cred:
                    raise Exception("Missing INDYKITE_APPLICATION_CREDENTIALS or "
                                    "INDYKITE_APPLICATION_CREDENTIALS_FILE environment variable")

                credentials = os.path.join(os.path.dirname(cred), os.path.basename(cred))
                credentials = helper.load_credentials(credentials)

            # Load the credential json (primary)
            else:
                credentials = helper.load_json(cred)

            agent_token = helper.create_agent_jwt(credentials)

            call_credentials = grpc.access_token_call_credentials(agent_token.decode("utf-8"))

            if local:
                certificate_path = os.getenv('CAPEM')
                endpoint = credentials.get("local_endpoint")
            else:
                certificate_path = certifi.where()
                endpoint = credentials.get("endpoint")

            with open(certificate_path, "rb") as cert_file:
                channel_credentials = grpc.ssl_channel_credentials(cert_file.read())

            composite_credentials = grpc.composite_channel_credentials(channel_credentials,
                                                                       call_credentials)

            self.channel = grpc.secure_channel(endpoint, composite_credentials)
            self.stub = pb2_grpc.IdentityManagementAPIStub(channel=self.channel)

        except Exception as exception:
            tb = sys.exception().__traceback__
            raise exception(...).with_traceback(tb)

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
