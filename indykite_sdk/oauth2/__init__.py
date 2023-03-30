import certifi
import grpc
import os
import sys
from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2_grpc as pb2_grpc
from indykite_sdk.identity import helper
from indykite_sdk.utils.logger import handle_excepthook, logger_error


class HttpClient:
    def __init__(self, token_source=None):
        self.token_source = token_source
        self.channel = None
        self.stub = None

    def get_http(self, token_source=None):
        sys.excepthook = handle_excepthook
        try:
            if token_source is None:
                raise Exception("TokenSource not found")
            access_bytes = token_source.token.access_token
            call_credentials = grpc.access_token_call_credentials(access_bytes.decode('utf-8'))

            certificate_path = certifi.where()
            endpoint = token_source.credentials.get("endpoint")
            with open(certificate_path, "rb") as cert_file:
                channel_credentials = grpc.ssl_channel_credentials(cert_file.read())

            composite_credentials = grpc.composite_channel_credentials(channel_credentials,
                                                                       call_credentials)

            self.channel = grpc.secure_channel(endpoint, composite_credentials)
            self.stub = pb2_grpc.IdentityManagementAPIStub(channel=self.channel)
            self.token_source = token_source

        except Exception as exception:
            return logger_error(exception)

    def get_credentials(self):
        try:
            # Load the credential json (primary)
            if 'INDYKITE_APPLICATION_CREDENTIALS' in os.environ:
                cred = os.getenv('INDYKITE_APPLICATION_CREDENTIALS')
                credentials = helper.load_json(cred)
            # Load the config from File (secondary)
            elif 'INDYKITE_APPLICATION_CREDENTIALS_FILE' in os.environ:
                cred = os.getenv('INDYKITE_APPLICATION_CREDENTIALS_FILE')
                credentials = os.path.join(os.path.dirname(cred), os.path.basename(cred))
                credentials = helper.load_credentials(credentials)
            else:
                raise Exception("Missing INDYKITE_APPLICATION_CREDENTIALS or "
                                "INDYKITE_APPLICATION_CREDENTIALS_FILE environment variable")
            return credentials

        except Exception as exception:
            return logger_error(exception)

    # Imported methods
    from .http import get_refreshable_token_source, get_http_client, get_token



