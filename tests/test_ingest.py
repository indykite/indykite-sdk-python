from indykite_sdk.ingestv2 import IngestClient
from indykite_sdk.indykite.ingest.v1beta2 import model_pb2, ingest_api_pb2 as pb2
from indykite_sdk.model.ingest_record import IngestRecordResponse
from helpers import data


def test_ingest_record_digital_twin_success():
    client = IngestClient()
    assert client is not None
    record_id = "745898"
    external_id = "external-dt-id3"
    tenant_id = data.get_tenant()
    type = "CarOwner"
    identity_property = client.identity_property("customIdProp", "456")
    assert isinstance(identity_property, model_pb2.IdentityProperty)
    identity_properties = [identity_property]
    ingest_property = client.ingest_property("customProp", "741")
    assert isinstance(ingest_property, model_pb2.Property)
    properties = [ingest_property]
    upsert = client.upsert_data_node_digital_twin(
        external_id,
        type,
        [],
        tenant_id,
        identity_properties,
        properties)
    assert isinstance(upsert, model_pb2.UpsertData)

    response = client.ingest_record_upsert(record_id, upsert)
    assert isinstance(response, IngestRecordResponse)


def test_ingest_record_resource_success():
    client = IngestClient()
    assert client is not None
    record_id = "745899"
    external_id = "lot-1"
    type = "ParkingLot"
    ingest_property = client.ingest_property("customProp", "9654")
    assert isinstance(ingest_property, model_pb2.Property)
    properties = [ingest_property]
    upsert = client.upsert_data_node_resource(
                                external_id,
                                type,
                                [],
                                properties)
    assert isinstance(upsert, model_pb2.UpsertData)
    response = client.ingest_record_upsert(record_id, upsert)
    assert isinstance(response, IngestRecordResponse)


def test_ingest_record_relation_success():
    client = IngestClient()
    assert client is not None
    record_id = "745890"
    type = "CAN_USE"
    source_match = client.node_match("vehicle-1", "Vehicle")
    assert isinstance(source_match, model_pb2.NodeMatch)
    target_match = client.node_match("lot-1", "ParkingLot")
    assert isinstance(target_match, model_pb2.NodeMatch)
    match = client.relation_match(source_match, target_match, type)
    assert isinstance(match, model_pb2.RelationMatch)
    ingest_property = client.ingest_property("customProp", "8742")
    assert isinstance(ingest_property, model_pb2.Property)
    properties = [ingest_property]
    upsert = client.upsert_data_relation(
        match,
        properties)
    assert isinstance(upsert, model_pb2.UpsertData)
    response = client.ingest_record_upsert(record_id, upsert)
    assert isinstance(response, IngestRecordResponse)

    node = client.node_match("vehicle-1", "Vehicle")
    delete = client.delete_data_node(node)
    assert isinstance(delete, model_pb2.DeleteData)
    response = client.ingest_record_delete(id=record_id, delete=delete)
    assert isinstance(response, IngestRecordResponse)


def test_ingest_record_relation_delete():
    client = IngestClient()
    assert client is not None
    record_id = "745891"
    type = "CAN_USE"
    source_match = client.node_match("vehicle-4", "Vehicle")
    assert isinstance(source_match, model_pb2.NodeMatch)
    target_match = client.node_match("lot-4", "ParkingLot")
    assert isinstance(target_match, model_pb2.NodeMatch)
    match = client.relation_match(source_match, target_match, type)
    assert isinstance(match, model_pb2.RelationMatch)
    properties = []
    upsert = client.upsert_data_relation(
        match,
        properties)
    assert isinstance(upsert, model_pb2.UpsertData)
    response = client.ingest_record_upsert(record_id, upsert)
    assert isinstance(response, IngestRecordResponse)

    delete = client.delete_data_relation(match)
    assert isinstance(delete, model_pb2.DeleteData)
    response = client.ingest_record_delete(id=record_id, delete=delete)
    assert isinstance(response, IngestRecordResponse)


def test_delete_record_node_property():
    client = IngestClient()
    assert client is not None
    record_id = "745892"
    type = "CAN_USE"
    source_match = client.node_match("vehicle-5", "Vehicle")
    assert isinstance(source_match, model_pb2.NodeMatch)
    target_match = client.node_match("lot-5", "ParkingLot")
    assert isinstance(target_match, model_pb2.NodeMatch)
    match = client.relation_match(source_match, target_match, type)
    assert isinstance(match, model_pb2.RelationMatch)
    properties = []
    upsert = client.upsert_data_relation(
        match,
        properties)
    assert isinstance(upsert, model_pb2.UpsertData)
    response = client.ingest_record_upsert(record_id, upsert)
    assert isinstance(response, IngestRecordResponse)

    key = "nodePropertyName"
    node_property = client.node_property_match(source_match, key)
    delete = client.delete_data_node_property(node_property)
    assert isinstance(delete, model_pb2.DeleteData)
    response = client.ingest_record_delete(id=record_id, delete=delete)
    assert isinstance(response, IngestRecordResponse)


def test_delete_record_relation_property():
    client = IngestClient()
    assert client is not None
    record_id = "745893"
    type = "CAN_USE"
    source_match = client.node_match("vehicle-6", "Vehicle")
    assert isinstance(source_match, model_pb2.NodeMatch)
    target_match = client.node_match("lot-6", "ParkingLot")
    assert isinstance(target_match, model_pb2.NodeMatch)
    match = client.relation_match(source_match, target_match, type)
    assert isinstance(match, model_pb2.RelationMatch)
    properties = []
    upsert = client.upsert_data_relation(
        match,
        properties)
    assert isinstance(upsert, model_pb2.UpsertData)
    response = client.ingest_record_upsert(record_id, upsert)
    assert isinstance(response, IngestRecordResponse)

    key = "relationPropertyName"
    relation_property = client.relation_property_match(match, key)
    delete = client.delete_data_relation_property(relation_property)
    assert isinstance(delete, model_pb2.DeleteData)
    response = client.ingest_record_delete(id=record_id, delete=delete)
    assert isinstance(response, IngestRecordResponse)


def test_identity_property(capsys):
    client = IngestClient()
    assert client is not None
    identity_property = client.identity_property([],[])
    captured = capsys.readouterr()
    assert "ERROR" in captured.err


def test_ingest_property(capsys):
    client = IngestClient()
    assert client is not None
    identity_property = client.ingest_property([],[])
    captured = capsys.readouterr()
    assert "ERROR" in captured.err


def test_upsert_digital_twin_error(capsys):
    client = IngestClient()
    assert client is not None
    source_match = client.node_match("vehicle-5", "Vehicle")
    upsert = client.upsert_data_node_digital_twin(source_match, source_match, source_match)
    captured = capsys.readouterr()
    assert not isinstance(upsert, model_pb2.UpsertData)
    assert "ERROR" in captured.err


def test_upsert_resource_error(capsys):
    client = IngestClient()
    assert client is not None
    source_match = client.node_match("vehicle-5", "Vehicle")
    upsert = client.upsert_data_node_resource(source_match, source_match, source_match)
    captured = capsys.readouterr()
    assert not isinstance(upsert, model_pb2.UpsertData)
    assert "ERROR" in captured.err


def test_upsert_relation_error(capsys):
    client = IngestClient()
    assert client is not None
    match = client.relation_match({}, {}, "")
    upsert = client.upsert_data_relation(match, match)
    captured = capsys.readouterr()
    assert not isinstance(upsert, model_pb2.UpsertData)
    assert "ERROR" in captured.err


def test_upsert_relation_match_error(capsys):
    client = IngestClient()
    assert client is not None
    match = client.relation_match("", "", "")
    captured = capsys.readouterr()
    assert not isinstance(match, model_pb2.RelationMatch)
    assert "ERROR" in captured.err


def test_node_property_match_error(capsys):
    client = IngestClient()
    assert client is not None
    key = "nodePropertyName"
    node_property = client.node_property_match("", key)
    captured = capsys.readouterr()
    assert not isinstance(node_property, model_pb2.DeleteData.NodePropertyMatch)
    assert "ERROR" in captured.err


def test_relation_property_match_error(capsys):
    client = IngestClient()
    assert client is not None
    key = "relationPropertyName"
    node_property = client.relation_property_match("", key)
    captured = capsys.readouterr()
    assert not isinstance(node_property, model_pb2.DeleteData.RelationPropertyMatch)
    assert "ERROR" in captured.err


def test_delete_data_node_error(capsys):
    client = IngestClient()
    assert client is not None
    delete = client.delete_data_node("")
    captured = capsys.readouterr()
    assert not isinstance(delete, model_pb2.DeleteData)
    assert "ERROR" in captured.err


def test_delete_data_relation_error(capsys):
    client = IngestClient()
    assert client is not None
    delete = client.delete_data_relation("")
    captured = capsys.readouterr()
    assert not isinstance(delete, model_pb2.DeleteData)
    assert "ERROR" in captured.err


def test_delete_data_node_property_error(capsys):
    client = IngestClient()
    assert client is not None
    delete = client.delete_data_node_property("")
    captured = capsys.readouterr()
    assert not isinstance(delete, model_pb2.DeleteData)
    assert "ERROR" in captured.err


def test_delete_data_relation_property_error(capsys):
    client = IngestClient()
    assert client is not None
    delete = client.delete_data_relation_property("")
    captured = capsys.readouterr()
    assert not isinstance(delete, model_pb2.DeleteData)
    assert "ERROR" in captured.err


def test_record_upsert_error(capsys):
    client = IngestClient()
    assert client is not None
    record = client.record_upsert("4521", "")
    captured = capsys.readouterr()
    assert not isinstance(record, model_pb2.Record)
    assert "ERROR" in captured.err


def test_ingest_record_delete_error(capsys):
    client = IngestClient()
    assert client is not None
    record_id = "745890"
    node = client.node_match("vehicle-11111111111", "Vehicle111111111")
    delete = client.delete_data_node(node)
    delete_record_node = client.ingest_record_delete(id=record_id, delete=delete)
    captured = capsys.readouterr()
    assert "ERROR" in captured.err
