
import random
import string

from indykite_sdk.ingest import IngestClient
from indykite_sdk.indykite.ingest.v1beta3 import model_pb2
from indykite_sdk.model.ingest_record import (BatchUpsertNodesResponse,
                                              BatchDeleteNodesResponse,
                                              BatchDeleteNodePropertiesResponse,
                                              BatchUpsertRelationshipsResponse,
                                              BatchDeleteRelationshipsResponse,
                                              BatchDeleteRelationshipPropertiesResponse)
from indykite_sdk.indykite.knowledge.objects.v1beta1 import ikg_pb2


def test_ingest_batch_identity_success():
    client = IngestClient()
    assert client is not None
    external_id = ''.join(random.choices(string.ascii_letters, k=15))
    external_id2 = ''.join(random.choices(string.ascii_letters, k=15))
    ingest_property = client.ingest_property("customProp1", "742")
    assert isinstance(ingest_property, ikg_pb2.Property)
    properties = [ingest_property]
    ingest_property2 = client.ingest_property("customProp2", "742")
    assert isinstance(ingest_property2, ikg_pb2.Property)
    properties2 = [ingest_property2]
    type = "Person"
    # create upsert object with all elements
    node1 = client.data_node(
        external_id,
        type,
        ["Person"],
        properties,
        "",
        True)
    node2 = client.data_node(
        external_id2,
        type,
        ["Person"],
        properties2,
        "",
        True)
    # send the ingestion request and get the response
    response = client.batch_upsert_nodes([node1, node2])
    assert isinstance(response, BatchUpsertNodesResponse)
    node_match1 = client.node_match(external_id, "Person")
    node_match2 = client.node_match(external_id2, "Person")
    delete_batch_node = client.batch_delete_nodes([node_match1, node_match2])
    assert isinstance(delete_batch_node, BatchDeleteNodesResponse)


def test_ingest_batch_relationship_success():
    client = IngestClient()
    assert client is not None
    type = "CAN_USE"
    source_match = client.node_match("vehicle-1", "Vehicle")
    assert isinstance(source_match, model_pb2.NodeMatch)
    target_match = client.node_match("lot-1", "ParkingLot")
    assert isinstance(target_match, model_pb2.NodeMatch)
    ingest_property = client.ingest_property("customProp", "8742")
    assert isinstance(ingest_property, ikg_pb2.Property)
    properties = [ingest_property]
    relationship1 = client.data_relationship(source_match, target_match, type, properties)
    assert isinstance(relationship1, model_pb2.Relationship)
    source_match = client.node_match("vehicle-2", "Vehicle")
    assert isinstance(source_match, model_pb2.NodeMatch)
    target_match = client.node_match("lot-2", "ParkingLot")
    assert isinstance(target_match, model_pb2.NodeMatch)
    relationship2 = client.data_relationship(source_match, target_match, type, properties)
    assert isinstance(relationship2, model_pb2.Relationship)
    response = client.batch_upsert_relationships([relationship1, relationship2])
    assert isinstance(response, BatchUpsertRelationshipsResponse)
    delete_batch_relationship = client.batch_delete_relationships([relationship1, relationship2])
    assert isinstance(delete_batch_relationship, BatchDeleteRelationshipsResponse)


def test_delete_batch_node_properties():
    client = IngestClient()
    assert client is not None
    external_id = ''.join(random.choices(string.ascii_letters, k=15))
    external_id2 = ''.join(random.choices(string.ascii_letters, k=15))
    ingest_property = client.ingest_property("custom1", "478")
    assert isinstance(ingest_property, ikg_pb2.Property)
    properties = [ingest_property]
    ingest_property2 = client.ingest_property("custom2", "214")
    assert isinstance(ingest_property2, ikg_pb2.Property)
    properties2 = [ingest_property2]
    type = "Person"
    # create upsert object with all elements
    node1 = client.data_node(
        external_id,
        type,
        ["Person"],
        properties,
        "",
        True)
    node2 = client.data_node(
        external_id2,
        type,
        ["Person"],
        properties2,
        "",
        True)
    # send the ingestion request and get the response
    response = client.batch_upsert_nodes([node1, node2])
    assert isinstance(response, BatchUpsertNodesResponse)
    node_match1 = client.node_match(external_id, "Person")
    node_match2 = client.node_match(external_id2, "Person")
    node_property = client.node_property_match(node_match1)
    node_property2 = client.node_property_match(node_match2)
    response = client.batch_delete_node_properties([node_property, node_property2])
    assert isinstance(response, BatchDeleteNodePropertiesResponse)


def test_delete_record_relationship_property():
    client = IngestClient()
    assert client is not None
    type = "CAN_USE"
    source_match = client.node_match("vehicle-1", "Vehicle")
    assert isinstance(source_match, model_pb2.NodeMatch)
    target_match = client.node_match("lot-1", "ParkingLot")
    assert isinstance(target_match, model_pb2.NodeMatch)
    ingest_property = client.ingest_property("customProp", "8742")
    assert isinstance(ingest_property, ikg_pb2.Property)
    properties = [ingest_property]
    relationship1 = client.data_relationship(source_match, target_match, type, properties)
    assert isinstance(relationship1, model_pb2.Relationship)
    property_type = "relationPropertyName"
    relationship_property = client.relationship_property_match(source_match, target_match, type, property_type)
    source_match = client.node_match("vehicle-2", "Vehicle")
    assert isinstance(source_match, model_pb2.NodeMatch)
    target_match = client.node_match("lot-2", "ParkingLot")
    assert isinstance(target_match, model_pb2.NodeMatch)
    relationship2 = client.data_relationship(source_match, target_match, type, properties)
    assert isinstance(relationship2, model_pb2.Relationship)
    relationship_property2 = client.relationship_property_match(source_match, target_match, type, property_type)
    response = client.batch_upsert_relationships([relationship1, relationship2])
    assert isinstance(response, BatchUpsertRelationshipsResponse)

    response = client.batch_delete_relationship_properties([relationship_property, relationship_property2])
    assert isinstance(response, BatchDeleteRelationshipPropertiesResponse)


def test_data_node_error(capsys):
    client = IngestClient()
    assert client is not None
    source_match = client.node_match("vehicle-5", "Vehicle")
    data = client.data_node(source_match, source_match, source_match, source_match, source_match, source_match)
    captured = capsys.readouterr()
    assert not isinstance(data, ikg_pb2.Node)
    assert "ERROR" in captured.err


def test_data_relationship_error(capsys):
    client = IngestClient()
    assert client is not None
    ingest_property = client.ingest_property("customProp", "665874")
    properties = [ingest_property]
    data = client.data_relationship({}, "", "", properties)
    captured = capsys.readouterr()
    assert not isinstance(data, model_pb2.UpsertData)
    assert "ERROR" in captured.err
