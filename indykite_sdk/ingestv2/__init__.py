import certifi
import grpc
import os
import sys
import indykite_sdk.utils.logger as logger
from indykite_sdk.identity import helper
from indykite_sdk.indykite.ingest.v1beta2 import ingest_api_pb2 as pb2
from indykite_sdk.indykite.ingest.v1beta2 import ingest_api_pb2_grpc as pb2_grpc


class IngestClient(object):

    def __init__(self, local=False):
        try:
            cred = os.getenv("INDYKITE_APPLICATION_CREDENTIALS")
            # Load the config from File (secondary)
            if not cred:
                cred = os.getenv("INDYKITE_APPLICATION_CREDENTIALS_FILE")
                if not cred:
                    raise Exception(
                        "Missing INDYKITE_APPLICATION_CREDENTIALS or "
                        "INDYKITE_APPLICATION_CREDENTIALS_FILE environment variable"
                    )

                credentials = os.path.join(os.path.dirname(cred), os.path.basename(cred))
                credentials = helper.load_credentials(credentials)

            # Load the credential json (primary)
            else:
                credentials = helper.load_json(cred)

            agent_token = helper.create_agent_jwt(credentials)

            call_credentials = grpc.access_token_call_credentials(agent_token.decode("utf-8"))

            if local:
                certificate_path = os.getenv("CAPEM")
                endpoint = credentials.get("local_endpoint")
            else:
                certificate_path = certifi.where()
                endpoint = credentials.get("endpoint")

            with open(certificate_path, "rb") as cert_file:
                channel_credentials = grpc.ssl_channel_credentials(cert_file.read())

            composite_credentials = grpc.composite_channel_credentials(channel_credentials, call_credentials)
            self.channel = grpc.secure_channel(endpoint, composite_credentials)
            self.stub = pb2_grpc.IngestAPIStub(channel=self.channel)
        except Exception as exception:
            tb = sys.exception().__traceback__
            raise exception(...).with_traceback(tb)

    # Imported methods
    from .ingest_record import ingest_record_upsert, upsert_data_node_digital_twin, identity_property, ingest_property, \
        upsert_data_node_resource, upsert_data_relation, relation_match, node_match, node_property_match, \
        relation_property_match, ingest_record_delete, delete_data_node, delete_data_relation, delete_data_node_property, \
        delete_data_relation_property, generate_records_request, stream_records, record_upsert
