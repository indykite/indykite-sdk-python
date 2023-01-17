import certifi
import grpc
import os

from indykite_sdk.authorization import helper
from indykite_sdk.indykite.authorization.v1beta1 import authorization_service_pb2_grpc as pb2


class AuthorizationClient(object):

    def __init__(self, local=False):
        cred = os.getenv('INDYKITE_APPLICATION_CREDENTIALS')

        # Load the config from File (secondary)
        if (cred is False) or (cred is None):
            cred = os.getenv('INDYKITE_APPLICATION_CREDENTIALS_FILE')
            try:
                if (cred is False) or (cred is None):
                    raise Exception("Missing INDYKITE_APPLICATION_CREDENTIALS or "
                                    "INDYKITE_APPLICATION_CREDENTIALS_FILE environment variable")
            except Exception as exception:
                print(exception)
                return None
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
        self.stub = pb2.AuthorizationAPIStub(channel=self.channel)

    # Imported methods
    from .is_authorized import is_authorized_token, is_authorized_digital_twin, is_authorized_property_filter
