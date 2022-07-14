from jarvis_sdk.ingest import IngestClient
from jarvis_sdk.indykite.ingest.v1beta1 import model_pb2
from jarvis_sdk.indykite.objects.v1beta1 import struct_pb2
from tests.helpers import data


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

    client.ingest_records(config_id, [record])
    captured = capsys.readouterr()

    assert "Ingest mapping config gid:AAAAFBtaAlxjDE8GuIWAPEFoSPs not found" in captured.out


def test_stream_record_wrong_external_id(capsys):
    config_id = data.get_config_id()
    record_data = {
        "playerId": struct_pb2.Value(string_value="125"),
        "firstname": struct_pb2.Value(string_value="Marius"),
        "gender": struct_pb2.Value(string_value="m"),
    }
    record = model_pb2.Record(id="2", external_id="wrongId", data=record_data)

    client = IngestClient()
    assert client is not None

    client.ingest_records(config_id, [record])
    captured = capsys.readouterr()

    assert "found no matching ingest mapping entity for the record external_id: wrongId" in captured.out


def test_stream_record_success(capsys):
    config_id = data.get_config_id()
    record_data = {
        "playerId": struct_pb2.Value(string_value="125"),
        "firstname": struct_pb2.Value(string_value="Marius"),
        "gender": struct_pb2.Value(string_value="m"),
    }
    record = model_pb2.Record(id="2", external_id="playerId", data=record_data)

    client = IngestClient()
    assert client is not None

    client.ingest_records(config_id, [record])
    captured = capsys.readouterr()

    assert 'record_id: "2"\nrecord_error {\n}\n\n' == captured.out


def test_stream_multiple_records_success(capsys):
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

    client.ingest_records(config_id, [record1, record2])
    captured = capsys.readouterr()

    assert (
        'record_id: "1"\nrecord_error {\n}\n\nrecord_id: "2"\nrecord_index: 1\nrecord_error {\n}\n\n'
        == captured.out
    )
