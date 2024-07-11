from indykite_sdk.ingest import IngestClient
from indykite_sdk.indykite.ingest.v1beta3 import model_pb2, ingest_api_pb2 as pb2


def test_stream_records_exception(capsys):
    client = IngestClient()
    assert client is not None
    record_id = "145899"
    external_id = "lot-1"
    type = "ParkingLot"
    ingest_property = client.ingest_property("customProp", "9654")
    properties = [ingest_property]
    upsert = client.upsert_data_node(
        external_id,
        type,
        [],
        properties)
    record = client.record_upsert(record_id, upsert)

    def mocked_stream_records(request_iter: pb2.StreamRecordsRequest):
        for request in request_iter:
            error = model_pb2.PropertyError()
            error.messages.append("problem")

            yield pb2.StreamRecordsResponse(
                record_id=request.record.id,
                record_error=model_pb2.RecordError(property_errors={"reason": error}),
            )

    client.stub.StreamRecords = mocked_stream_records
    responses = client.stream_records([record])
    captured = capsys.readouterr()
    assert "ERROR" in captured.err


def test_stream_records_success():
    client = IngestClient()
    assert client is not None
    record_id = "145899"
    external_id = "lot-1"
    type = "ParkingLot"
    ingest_property = client.ingest_property("customProp", "9654")
    properties = [ingest_property]
    upsert = client.upsert_data_node(
        external_id,
        type,
        [],
        properties)
    record = client.record_upsert(record_id, upsert)

    def mocked_stream_records(request_iter: pb2.StreamRecordsRequest):
        for request in request_iter:
            yield pb2.StreamRecordsResponse(record_id=request.record.id, record_error=model_pb2.RecordError())

    client.stub.StreamRecords = mocked_stream_records
    responses = client.stream_records([record])
    head, tail = responses[0], responses[1:]

    assert head.record_id == "145899"
    assert len(head.record_error.error) == 0
    assert tail == []


def test_stream_records_fail(capsys):
    client = IngestClient()
    assert client is not None
    record_id = "999658"
    record = client.record_upsert(record_id, "")

    def mocked_stream_records(request_iter: pb2.StreamRecordsRequest):
        for request in request_iter:
            yield pb2.StreamRecordsResponse(record_id=request.record.id, record_error=model_pb2.RecordError())

    client.stub.StreamRecords = mocked_stream_records
    responses = client.stream_records([record])
    captured = capsys.readouterr()
    assert "ERROR" in captured.err
