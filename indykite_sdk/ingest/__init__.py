import certifi
import grpc
import os

from indykite_sdk.identity import helper
from indykite_sdk.indykite.ingest.v1beta1 import ingest_api_pb2 as pb2
from indykite_sdk.indykite.ingest.v1beta1 import ingest_api_pb2_grpc as pb2_grpc
from typing import Iterator


class IngestClient(object):
    def __init__(self, local=False):
        cred = os.getenv("INDYKITE_APPLICATION_CREDENTIALS")

        # Load the config from File (secondary)
        if (cred is False) or (cred is None):
            cred = os.getenv("INDYKITE_APPLICATION_CREDENTIALS_FILE")
            try:
                if (cred is False) or (cred is None):
                    raise Exception(
                        "Missing INDYKITE_APPLICATION_CREDENTIALS or INDYKITE_APPLICATION_CREDENTIALS_FILE environment variable"
                    )
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

    def generate_records_request(self, config_id, records):
        """Create iterator for record requests."""
        for record in records:
            record_request = pb2.StreamRecordsRequest(mapping_config_id=config_id, record=record)
            yield record_request

    def stream_records(self, config_id, records):
        record_iterator = self.generate_records_request(config_id, records)
        response_iterator = self.stub.StreamRecords(record_iterator)
        responses = []

        try:
            for response in response_iterator:
                if not response.record_error.property_errors:
                    print(f"Record {response.record_id} ingested successfully")
                else:
                    print(f"Record {response.record_id} has errors: \n{response.record_error}")

                responses.append(response)
        except Exception as exception:
            print(exception)
            return None

        return responses
