from indykite_sdk.ingest import IngestClient
from indykite_sdk.indykite.ingest.v1beta3 import model_pb2
from indykite_sdk.model.ingest_record import IngestRecordResponse
from indykite_sdk.indykite.knowledge.objects.v1beta1 import ikg_pb2


def test_ingest_record_digital_twin_success():
    client = IngestClient()
    assert client is not None
    record_id = "745898"
    external_id = "external-dt-id345"
    type = "Owner"
    ingest_property = client.ingest_property("customProp2", "742")
    assert isinstance(ingest_property, ikg_pb2.Property)
    properties = [ingest_property]
    upsert = client.upsert_data_node(
        external_id,
        type,
        [],
        properties,
        "",
        True)
    assert isinstance(upsert, model_pb2.UpsertData)
    record = client.record_upsert(record_id, upsert)
    assert isinstance(record, model_pb2.Record)
    response = client.ingest_record(record)
    assert isinstance(response, IngestRecordResponse)


def test_ingest_record_resource_success():
    client = IngestClient()
    assert client is not None
    record_id = "745899"
    external_id = "lot-1"
    type = "ParkingLot"
    ingest_property = client.ingest_property("customProp", "9654")
    assert isinstance(ingest_property, ikg_pb2.Property)
    properties = [ingest_property]
    upsert = client.upsert_data_node(
                                external_id,
                                type,
                                [],
                                properties,
                                "",
                                False)
    assert isinstance(upsert, model_pb2.UpsertData)
    record = client.record_upsert(record_id, upsert)
    assert isinstance(record, model_pb2.Record)
    response = client.ingest_record(record)
    assert isinstance(response, IngestRecordResponse)


def test_ingest_record_relationship_success():
    client = IngestClient()
    assert client is not None
    record_id = "745890"
    type = "CAN_USE"
    source_match = client.node_match("vehicle-1", "Vehicle")
    assert isinstance(source_match, model_pb2.NodeMatch)
    target_match = client.node_match("lot-1", "ParkingLot")
    assert isinstance(target_match, model_pb2.NodeMatch)
    ingest_property = client.ingest_property("customProp", "8742")
    assert isinstance(ingest_property, ikg_pb2.Property)
    properties = [ingest_property]
    upsert = client.upsert_data_relationship(source_match, target_match, type, properties)
    assert isinstance(upsert, model_pb2.UpsertData)
    record = client.record_upsert(record_id, upsert)
    assert isinstance(record, model_pb2.Record)
    response = client.ingest_record(record)
    assert isinstance(response, IngestRecordResponse)

    node = client.node_match("vehicle-1", "Vehicle")
    delete = client.delete_data_node(node)
    assert isinstance(delete, model_pb2.DeleteData)
    record = client.record_delete(record_id, delete)
    assert isinstance(record, model_pb2.Record)
    response = client.ingest_record(record)
    assert isinstance(response, IngestRecordResponse)


def test_ingest_record_relationship_delete():
    client = IngestClient()
    assert client is not None
    record_id = "856921"
    type = "CAN_DRIVE"
    source_match = client.node_match("vehicle-465", "Vehicle")
    assert isinstance(source_match, model_pb2.NodeMatch)
    target_match = client.node_match("lot-4645", "ParkingLot")
    assert isinstance(target_match, model_pb2.NodeMatch)
    ingest_property = client.ingest_property("customProp", "4412512")
    properties = [ingest_property]
    upsert = client.upsert_data_relationship(source_match, target_match, type, properties)
    assert isinstance(upsert, model_pb2.UpsertData)
    record = client.record_upsert(record_id, upsert)
    assert isinstance(record, model_pb2.Record)
    response = client.ingest_record(record)
    assert isinstance(response, IngestRecordResponse)
    relationship = model_pb2.Relationship(
        source=source_match,
        target=target_match,
        type=type,
        properties=properties)
    assert isinstance(relationship, model_pb2.Relationship)
    delete = client.delete_data_relationship(relationship)
    assert isinstance(delete, model_pb2.DeleteData)
    record = client.record_delete(record_id, delete)
    assert isinstance(record, model_pb2.Record)
    response = client.ingest_record(record)
    assert isinstance(response, IngestRecordResponse)


def test_delete_record_node_property():
    client = IngestClient()
    assert client is not None
    record_id = "589623"
    type = "CAN_DRIVE"
    source_match = client.node_match("vehicle-555", "Vehicle")
    assert isinstance(source_match, model_pb2.NodeMatch)
    target_match = client.node_match("lot-555", "ParkingLot")
    assert isinstance(target_match, model_pb2.NodeMatch)
    ingest_property = client.ingest_property("customProp", "777447")
    properties = [ingest_property]
    upsert = client.upsert_data_relationship(source_match, target_match, type, properties)
    assert isinstance(upsert, model_pb2.UpsertData)
    record = client.record_upsert(record_id, upsert)
    assert isinstance(record, model_pb2.Record)
    response = client.ingest_record(record)
    assert isinstance(response, IngestRecordResponse)

    property_type = "nodePropertyName"
    node_property = client.node_property_match(source_match, property_type)
    delete = client.delete_data_node_property(node_property)
    assert isinstance(delete, model_pb2.DeleteData)
    record = client.record_delete(record_id, delete)
    assert isinstance(record, model_pb2.Record)
    response = client.ingest_record(record)
    assert isinstance(response, IngestRecordResponse)


def test_delete_record_relationship_property():
    client = IngestClient()
    assert client is not None
    record_id = "6523145"
    type = "CAN_DRIVE"
    source_match = client.node_match("vehicle-656", "Vehicle")
    assert isinstance(source_match, model_pb2.NodeMatch)
    target_match = client.node_match("lot-656", "ParkingLot")
    assert isinstance(target_match, model_pb2.NodeMatch)
    ingest_property = client.ingest_property("customProp", "665874")
    properties = [ingest_property]
    upsert = client.upsert_data_relationship(source_match, target_match, type, properties)
    assert isinstance(upsert, model_pb2.UpsertData)
    record = client.record_upsert(record_id, upsert)
    response = client.ingest_record(record)
    assert isinstance(response, IngestRecordResponse)

    property_type = "relationPropertyName"
    relationship_property = client.relationship_property_match(source_match, target_match, type, property_type)
    delete = client.delete_data_relationship_property(relationship_property)
    assert isinstance(delete, model_pb2.DeleteData)
    record = client.record_delete(record_id, delete)
    assert isinstance(record, model_pb2.Record)
    response = client.ingest_record(record)
    assert isinstance(response, IngestRecordResponse)


def test_ingest_property_no_type(capsys):
    client = IngestClient()
    assert client is not None
    ing_property = client.ingest_property("","")
    captured = capsys.readouterr()
    assert "type is missing" in captured.err


def test_ingest_property_no_value(capsys):
    client = IngestClient()
    assert client is not None
    ing_property = client.ingest_property("role","")
    captured = capsys.readouterr()
    assert "value is missing" in captured.err


def test_upsert_node_error(capsys):
    client = IngestClient()
    assert client is not None
    source_match = client.node_match("vehicle-5", "Vehicle")
    upsert = client.upsert_data_node(source_match, source_match, source_match, source_match, source_match, source_match)
    captured = capsys.readouterr()
    assert not isinstance(upsert, model_pb2.UpsertData)
    assert "ERROR" in captured.err


def test_upsert_relationship_error(capsys):
    client = IngestClient()
    assert client is not None
    ingest_property = client.ingest_property("customProp", "665874")
    properties = [ingest_property]
    upsert = client.upsert_data_relationship({}, "", "", properties)
    captured = capsys.readouterr()
    assert not isinstance(upsert, model_pb2.UpsertData)
    assert "ERROR" in captured.err


def test_node_property_match_error(capsys):
    client = IngestClient()
    assert client is not None
    type_property = "nodePropertyName"
    node_property = client.node_property_match("", type_property)
    captured = capsys.readouterr()
    assert not isinstance(node_property, model_pb2.DeleteData.NodePropertyMatch)
    assert "ERROR" in captured.err


def test_relationship_property_match_error(capsys):
    client = IngestClient()
    assert client is not None
    type_property = "relationshipPropertyName"
    node_property = client.relationship_property_match("", "", type_property)
    captured = capsys.readouterr()
    assert not isinstance(node_property, model_pb2.DeleteData.RelationshipPropertyMatch)
    assert "ERROR" in captured.err


def test_delete_data_node_error(capsys):
    client = IngestClient()
    assert client is not None
    delete = client.delete_data_node("")
    captured = capsys.readouterr()
    assert not isinstance(delete, model_pb2.DeleteData)
    assert "ERROR" in captured.err


def test_delete_data_relationship_error(capsys):
    client = IngestClient()
    assert client is not None
    delete = client.delete_data_relationship("")
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


def test_delete_data_relationship_property_error(capsys):
    client = IngestClient()
    assert client is not None
    delete = client.delete_data_relationship_property("")
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
    record = client.record_delete(record_id, delete)
    delete_record_node = client.ingest_record(record)
    captured = capsys.readouterr()
    assert "ERROR" in captured.err
