from indykite_sdk.indykite.ingest.v1beta3 import ingest_api_pb2 as pb2
from indykite_sdk.model.ingest_record import StreamRecordsResponse
import sys
import indykite_sdk.utils.logger as logger


def generate_records_request(self, records):
    """
    Create iterator for record requests
    :param self:
    :param records: list of records
    :return: yield record_request
    """
    """Create iterator for record requests."""
    for record in records:
        record_request = pb2.StreamRecordsRequest(record=record)
        yield record_request


def stream_records(self, records):
    """
    send records in stream
    :param self:
    :param records: list of records
    :return: list of deserialized StreamRecordsResponses
    """
    sys.excepthook = logger.handle_excepthook
    try:
        record_iterator = self.generate_records_request(records)
        response_iterator = self.stub.StreamRecords(record_iterator)
        responses = list(response_iterator)
        res = [StreamRecordsResponse.deserialize(response) for response in responses]
        return res

    except Exception as exception:
        return logger.logger_error(exception)
