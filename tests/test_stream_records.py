from indykite_sdk.ingest import IngestClient
from indykite_sdk.indykite.ingest.v1beta1 import model_pb2, ingest_api_pb2 as pb2
from indykite_sdk.indykite.objects.v1beta1 import struct_pb2
from helpers import data


def test_stream_record_nonexisting_config_id(capsys):
    config_id = "gid:AAAAFBtaAlxjDE8GuIWAPEFoSPs"
    record_data = {
        "playerId": struct_pb2.Value(string_value="125"),
        "firstname": struct_pb2.Value(string_value="Marius"),
        "gender": struct_pb2.Value(string_value="m"),
    }
    record = model_pb2.Record(id="2", external_id="test", data=record_data)

    client = IngestClient()
    assert client is not None

    client.stream_records(config_id, [record])
    captured = capsys.readouterr()

    assert "no Knowledge Graph exists for this AppSpace" in captured.out


def test_stream_record_error():
    config_id = data.get_config_id()
    record_data = {
        "playerId": struct_pb2.Value(string_value="125"),
        "firstname": struct_pb2.Value(string_value="Marius"),
        "gender": struct_pb2.Value(string_value="m"),
    }
    record = model_pb2.Record(id="2", external_id="playerId", data=record_data)

    client = IngestClient()
    assert client is not None

    def mocked_stream_records(request_iter: pb2.StreamRecordsRequest):
        for request in request_iter:
            error = model_pb2.PropertyError()
            error.messages.append("problem")

            yield pb2.StreamRecordsResponse(
                record_id=request.record.id,
                record_error=model_pb2.RecordError(property_errors={"reason": error}),
            )

    client.stub.StreamRecords = mocked_stream_records
    responses = client.stream_records(config_id, [record])
    head, *tail = responses

    assert head.record_id is "2"
    assert len(head.record_error.property_errors) is 1
    assert head.record_error.property_errors["reason"].messages == ["problem"]
    assert tail == []


def test_stream_record_success():
    config_id = data.get_config_id()
    record_data = {
        "playerId": struct_pb2.Value(string_value="125"),
        "firstname": struct_pb2.Value(string_value="Marius"),
        "gender": struct_pb2.Value(string_value="m"),
    }
    record = model_pb2.Record(id="2", external_id="playerId", data=record_data)

    client = IngestClient()
    assert client is not None

    def mocked_stream_records(request_iter: pb2.StreamRecordsRequest):
        for request in request_iter:
            yield pb2.StreamRecordsResponse(record_id=request.record.id, record_error=model_pb2.RecordError())

    client.stub.StreamRecords = mocked_stream_records
    responses = client.stream_records(config_id, [record])
    head, tail = responses[0], responses[1:]

    assert head.record_id is "2"
    assert len(head.record_error.property_errors) is 0
    assert tail == []


def test_stream_multiple_records_success():
    config_id = data.get_config_id()
    record1_data = {
        "playerId": struct_pb2.Value(string_value="125"),
        "firstname": struct_pb2.Value(string_value="Marius"),
        "gender": struct_pb2.Value(string_value="m"),
    }
    record1 = model_pb2.Record(id="1", external_id="playerId", data=record1_data)
    record2_data = {
        "playerId": struct_pb2.Value(string_value="126"),
        "firstname": struct_pb2.Value(string_value="Elizabeth"),
        "gender": struct_pb2.Value(string_value="f"),
    }
    record2 = model_pb2.Record(id="2", external_id="playerId", data=record2_data)

    client = IngestClient()
    assert client is not None

    def mocked_stream_records(request_iter: pb2.StreamRecordsRequest):
        for request in request_iter:
            yield pb2.StreamRecordsResponse(record_id=request.record.id, record_error=model_pb2.RecordError())

    client.stub.StreamRecords = mocked_stream_records
    responses = client.stream_records(config_id, [record1, record2])
    first, second, tail = responses[0], responses[1], responses[2:]

    assert first.record_id is "1"
    assert len(first.record_error.property_errors) is 0
    assert second.record_id is "2"
    assert len(second.record_error.property_errors) is 0
    assert tail == []
