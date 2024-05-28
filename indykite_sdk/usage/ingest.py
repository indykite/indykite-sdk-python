"""
Commandline interface for making an API request with the SDK.
"""
import argparse
from datetime import datetime
import random
import string
import uuid
from indykite_sdk.ingest import IngestClient
from indykite_sdk import api_helper
from indykite_sdk.indykite.ingest.v1beta3 import model_pb2


class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):  # pragma: no cover
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value


def main():
    # Create parent parser
    parser = argparse.ArgumentParser(description="Identity client API.")
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    # Create child parsers
    # ingest
    ingest_record_identity_parser = subparsers.add_parser("ingest_record_identity")
    ingest_record_resource_parser = subparsers.add_parser("ingest_record_resource")
    ingest_record_relation_parser = subparsers.add_parser("ingest_record_relation")
    delete_record_relation_property_parser = subparsers.add_parser("delete_record_relation_property")
    delete_record_node_property_parser = subparsers.add_parser("delete_record_node_property")
    delete_record_relation_parser = subparsers.add_parser("delete_record_relation")
    delete_record_node_parser = subparsers.add_parser("delete_record_node")
    stream_records_parser = subparsers.add_parser("stream_records")
    ingest_batch_identity_parser = subparsers.add_parser("ingest_batch_identity")
    ingest_batch_resource_parser = subparsers.add_parser("ingest_batch_resource")
    delete_batch_identity_parser = subparsers.add_parser("delete_batch_identity")
    delete_batch_resource_parser = subparsers.add_parser("delete_batch_resource")
    delete_batch_node_properties_parser = subparsers.add_parser("delete_batch_node_properties")
    ingest_batch_relationship_parser = subparsers.add_parser("ingest_batch_relationship")
    delete_batch_relationship_parser = subparsers.add_parser("delete_batch_relationship")
    delete_batch_relationship_properties_parser = subparsers.add_parser("delete_batch_relationship_properties")

    args = parser.parse_args()
    command = args.command

    if command == "ingest_record_identity":
        """shell
            python3 ingest.py ingest_record_identity
        """
        # ingest an identity node record in the IKG service
        # replace with your own values
        client_ingest = IngestClient()
        # unique value which can be random
        record_id = str(uuid.uuid4())
        # unique id in external source
        external_id = ''.join(random.choices(string.ascii_letters, k=15))
        print(external_id)
        # type of node
        type = "Person"
        # properties
        ingest_property1 = client_ingest.ingest_property("first_name", "blicken")
        ingest_property2 = client_ingest.ingest_property("last_name", "grumpy")
        ingest_property3 = client_ingest.ingest_property("birthdate", "20 Sep, 1977")
        ingest_property4 = client_ingest.ingest_property("role", "Employee")
        ingest_property5 = client_ingest.ingest_property("email", "blicken@yahoo.uk")
        properties = [ingest_property1, ingest_property2, ingest_property3, ingest_property4, ingest_property5]
        # create upsert object with all elements
        upsert = client_ingest.upsert_data_node(
            external_id,
            type,
            ["Person"],
            properties,
            "",
            True)
        # create record with record_id and upsert
        record = client_ingest.record_upsert(record_id, upsert)
        print(record)
        # send the ingestion request and get the response
        ingest_record_identity_node = client_ingest.ingest_record(record)
        if ingest_record_identity_node:
            api_helper.print_response(ingest_record_identity_node)
        else:
            print("Invalid upsert")
        client_ingest.channel.close()
        return ingest_record_identity_node

    elif command == "ingest_record_resource":
        """shell
            python3 ingest.py ingest_record_resource
        """
        # ingest a resource node record in the IKG service
        # replace with your own values
        client_ingest = IngestClient()
        # unique value which can be random
        record_id = str(uuid.uuid4())
        # unique id in external source
        external_id = ''.join(random.choices(string.ascii_letters, k=15))
        print(external_id)
        # type of node
        type = "Asset"
        # properties
        t = datetime.now()
        ingest_metadata = client_ingest.ingest_metadata(1, t, "BRUCE", {"customVin": "customVinValue"})
        ingest_property = client_ingest.ingest_property("maker", "FORD")
        ingest_property2 = client_ingest.ingest_property("vin", "PjOkiLpNjm", ingest_metadata)
        ingest_property3 = client_ingest.ingest_property("colour", "blue")
        ingest_property4 = client_ingest.ingest_property("asset", "T")
        ingest_property5 = client_ingest.ingest_property("status", "Active")
        properties = [ingest_property, ingest_property2, ingest_property3, ingest_property4, ingest_property5]
        # create upsert object with all elements
        upsert = client_ingest.upsert_data_node(
            external_id,
            type,
            ["Asset"],
            properties)
        # create record with record_id and upsert
        record = client_ingest.record_upsert(record_id, upsert)
        # send the ingestion request and get the response
        ingest_record_resource = client_ingest.ingest_record(record)
        if ingest_record_resource:
            api_helper.print_response(ingest_record_resource)
        else:
            print("Invalid upsert")
        client_ingest.channel.close()
        return ingest_record_resource

    elif command == "ingest_record_relation":
        """shell
            python3 ingest.py ingest_record_relation
        """
        # ingest a relationship record in the IKG service
        # replace with your own values
        client_ingest = IngestClient()
        # unique value which can be random
        record_id = str(uuid.uuid4())
        # type of relationship
        type = "BELONGS_TO"
        # id in external source / type of node : pair must be unique
        source_match = client_ingest.node_match("HLEgiljrtoNEiyX", "Individual")
        target_match = client_ingest.node_match("tSMiFkHozbhtfQZ", "Organization")
        # create upsert object with all elements
        upsert = client_ingest.upsert_data_relationship(
            source_match, target_match, type,
            [])
        # create record with record_id and upsert
        record = client_ingest.record_upsert(record_id, upsert)
        # send the ingestion request and get the response
        ingest_record_relation = client_ingest.ingest_record(record)
        if ingest_record_relation:
            api_helper.print_response(ingest_record_relation)
        else:
            print("Invalid upsert")
        client_ingest.channel.close()
        return ingest_record_relation

    elif command == "delete_record_node":
        """shell
            python3 ingest.py delete_record_node
        """
        # delete a node record from the IKG service
        # replace with your own values
        client_ingest = IngestClient()
        # unique value which can be random
        record_id = "745890"
        # id in external source / type of node : pair must be unique
        # create node object with the elements
        node = client_ingest.node_match("QNcLrJCLGjIbpYO", "Individual")
        delete = client_ingest.delete_data_node(node)
        # create record with record_id and delete object
        record = client_ingest.record_delete(record_id, delete)
        # send the deletion request and get the response
        delete_record_node = client_ingest.ingest_record(record)
        if delete_record_node:
            api_helper.print_response(delete_record_node)
        else:
            print("Invalid delete")
        client_ingest.channel.close()
        return delete_record_node

    elif command == "delete_record_relation":
        """shell
            python3 ingest.py delete_record_relation
        """
        # delete a relationship record from the IKG service
        # replace with your own values
        client_ingest = IngestClient()
        # unique value which can be random
        record_id = "745890"
        # type of relationship
        type = "CAN_USE"
        # id in external source / type of node : pair must be unique
        source_match = client_ingest.node_match("vehicle-1", "Vehicle")
        target_match = client_ingest.node_match("lot-1", "ParkingLot")
        # create relationship object with the elements
        relation = model_pb2.Relationship(source=source_match, target=target_match, type=type, properties=[])
        delete = client_ingest.delete_data_relationship(relation)
        # create record with record_id and delete object
        record = client_ingest.record_delete(record_id, delete)
        # send the deletion request and get the response
        delete_record_relation = client_ingest.ingest_record(record)
        if delete_record_relation:
            api_helper.print_response(delete_record_relation)
        else:
            print("Invalid delete")
        client_ingest.channel.close()
        return delete_record_relation

    elif command == "delete_record_node_property":
        """shell
            python3 ingest.py delete_record_node_property
        """
        # delete a node by property from the IKG service
        # replace with your own values
        client_ingest = IngestClient()
        # unique value which can be random
        record_id = "745890"
        # id in external source / type of node : pair must be unique
        match = client_ingest.node_match("vehicle-1", "Vehicle")
        property_type = "nodePropertyName"
        node_property = client_ingest.node_property_match(match, property_type)
        delete = client_ingest.delete_data_node_property(node_property)
        # create record with record_id and delete object
        record = client_ingest.record_delete(record_id, delete)
        # send the deletion request and get the response
        delete_record_node_property = client_ingest.ingest_record(record)
        if delete_record_node_property:
            api_helper.print_response(delete_record_node_property)
        else:
            print("Invalid delete")
        client_ingest.channel.close()
        return delete_record_node_property

    elif command == "delete_record_relation_property":
        """shell
            python3 ingest.py delete_record_relation_property
        """
        # delete a relationship by property from the IKG service
        # replace with your own values
        client_ingest = IngestClient()
        # unique value which can be random
        record_id = "745890"
        # type of relationship
        type = "CAN_USE"
        # id in external source / type of node : pair must be unique
        source_match = client_ingest.node_match("vehicle-1", "Vehicle")
        target_match = client_ingest.node_match("lot-1", "ParkingLot")
        property_type = "relationPropertyName"
        # create relationship property object with all elements
        relation_property = client_ingest.relationship_property_match(source_match, target_match, type, property_type)
        delete = client_ingest.delete_data_relationship_property(relation_property)
        # create record with record_id and delete object
        record = client_ingest.record_delete(record_id, delete)
        # send the deletion request and get the response
        delete_record_relation_property = client_ingest.ingest_record(record)
        if delete_record_relation_property:
            api_helper.print_response(delete_record_relation_property)
        else:
            print("Invalid delete")
        client_ingest.channel.close()
        return delete_record_relation_property

    elif command == "stream_records":
        """shell
            python3 ingest.py stream_records
        """
        # ingest a stream of nodes records in the IKG service
        # replace with your own values
        client_ingest = IngestClient()
        # unique value which can be random
        record_id = str(uuid.uuid4())
        # unique id in external source
        external_id = ''.join(random.choices(string.ascii_letters, k=15))
        print(external_id)
        # type of node
        type = "Asset"
        # properties
        ingest_property = client_ingest.ingest_property("maker", "FORD")
        ingest_property2 = client_ingest.ingest_property("vin", "9WEBDCF112547KIOLP")
        ingest_property3 = client_ingest.ingest_property("colour", "green")
        ingest_property4 = client_ingest.ingest_property("asset", "T")
        ingest_property5 = client_ingest.ingest_property("status", "Active")
        properties = [ingest_property, ingest_property2, ingest_property3, ingest_property4, ingest_property5]
        # create upsert object with all elements
        upsert = client_ingest.upsert_data_node(
            external_id,
            type,
            ["Asset"],
            properties)
        # create record with record_id and upsert
        record = client_ingest.record_upsert(record_id, upsert)

        record_id2 = str(uuid.uuid4())
        # unique id in external source
        external_id = ''.join(random.choices(string.ascii_letters, k=15))
        print(external_id)
        # type of node
        type = "Asset"
        # properties
        ingest_property = client_ingest.ingest_property("maker", "FORD")
        ingest_property2 = client_ingest.ingest_property("vin", "9WEBDCF188745KIOLP")
        ingest_property3 = client_ingest.ingest_property("colour", "red")
        ingest_property4 = client_ingest.ingest_property("asset", "T")
        ingest_property5 = client_ingest.ingest_property("status", "Active")
        properties = [ingest_property, ingest_property2, ingest_property3, ingest_property4, ingest_property5]
        # create upsert object with all elements
        upsert2 = client_ingest.upsert_data_node(
            external_id,
            type,
            ["Asset"],
            properties)
        # create record with record_id and upsert
        record2 = client_ingest.record_upsert(record_id2, upsert2)

        record_id3 = str(uuid.uuid4())
        # unique id in external source
        external_id = ''.join(random.choices(string.ascii_letters, k=15))
        print(external_id)
        # type of node
        type = "Asset"
        # properties
        ingest_property = client_ingest.ingest_property("maker", "FORD")
        ingest_property2 = client_ingest.ingest_property("vin", "9WEBDCF188745KIOLP")
        ingest_property3 = client_ingest.ingest_property("colour", "red")
        ingest_property4 = client_ingest.ingest_property("asset", "T")
        ingest_property5 = client_ingest.ingest_property("status", "Active")
        properties = [ingest_property, ingest_property2, ingest_property3, ingest_property4, ingest_property5]
        # create upsert object with all elements
        upsert3 = client_ingest.upsert_data_node(
            external_id,
            type,
            ["Asset"],
            properties)
        # create record with record_id and upsert
        record3 = client_ingest.record_upsert(record_id3, upsert3)
        # send the ingestion requests in stream and get the responses
        responses = client_ingest.stream_records(
            [record, record2, record3])
        if responses:
            for response in responses:
                api_helper.print_response(response)
        else:
            print("Invalid ingestion")
        client_ingest.channel.close()
        return response

    elif command == "ingest_batch_identity":
        """shell
            python3 ingest.py ingest_batch_identity
        """
        # ingest identity nodes in the IKG service
        # replace with your own values
        client_ingest = IngestClient()
        # unique id in external source
        external_id = ''.join(random.choices(string.ascii_letters, k=15))
        print(external_id)
        external_id2 = ''.join(random.choices(string.ascii_letters, k=15))
        print(external_id2)
        # type of node
        type = "Person"
        # properties
        ingest_property1 = client_ingest.ingest_property("firstname", "kelso")
        ingest_property2 = client_ingest.ingest_property("lastname", "grumpy")
        ingest_property3 = client_ingest.ingest_property("birthdate", "20 Sep, 1977")
        ingest_property4 = client_ingest.ingest_property("role", "Employee")
        ingest_property5 = client_ingest.ingest_property("email", "kelso@yahoo.uk")
        properties = [ingest_property1, ingest_property2, ingest_property3, ingest_property4, ingest_property5]
        ingest_property21 = client_ingest.ingest_property("firstname", "elias")
        ingest_property25 = client_ingest.ingest_property("email", "eliaslso@yahoo.uk")
        properties2 = [ingest_property21, ingest_property2, ingest_property3, ingest_property4, ingest_property25]
        # create upsert object with all elements
        node1 = client_ingest.data_node(
            external_id,
            type,
            ["Person"],
            properties,
            "",
            True)
        node2 = client_ingest.data_node(
            external_id2,
            type,
            ["Person"],
            properties2,
            "",
            True)
        # send the ingestion request and get the response
        ingest = client_ingest.batch_upsert_nodes([node1, node2])
        if ingest:
            api_helper.print_response(ingest)
        else:
            print("Invalid upsert")
        client_ingest.channel.close()
        return ingest

    elif command == "ingest_batch_resource":
        """shell
            python3 ingest.py ingest_batch_resource
        """
        # ingest identity nodes in the IKG service
        # replace with your own values
        client_ingest = IngestClient()
        # unique id in external source
        external_id = ''.join(random.choices(string.ascii_letters, k=15))
        print(external_id)
        external_id2 = ''.join(random.choices(string.ascii_letters, k=15))
        print(external_id2)
        # type of node
        type = "Car"
        # properties
        t = datetime.now()
        ingest_metadata = client_ingest.ingest_metadata(1, t, "BRUCE", {"customVin": "customVinValue"})
        ingest_property = client_ingest.ingest_property("maker", "FORD")
        ingest_property2 = client_ingest.ingest_property("vin", "PjOkiLpNjm", ingest_metadata)
        ingest_property3 = client_ingest.ingest_property("colour", "blue")
        ingest_property4 = client_ingest.ingest_property("asset", "T")
        ingest_property5 = client_ingest.ingest_property("status", "Active")
        properties = [ingest_property, ingest_property2, ingest_property3, ingest_property4, ingest_property5]
        ingest_property22 = client_ingest.ingest_property("vin", "ioiroeiorieo")
        ingest_property32 = client_ingest.ingest_property("colour", "pink")
        properties2 = [ingest_property, ingest_property22, ingest_property32, ingest_property4, ingest_property5]
        # create upsert object with all elements
        node1 = client_ingest.data_node(
            external_id,
            type,
            ["Car"],
            properties,
            "",
            False)
        node2 = client_ingest.data_node(
            external_id2,
            type,
            ["Cr"],
            properties2,
            "",
            False)
        # send the ingestion request and get the response
        ingest = client_ingest.batch_upsert_nodes([node1, node2])
        if ingest:
            api_helper.print_response(ingest)
        else:
            print("Invalid upsert")
        client_ingest.channel.close()
        return ingest

    elif command == "delete_batch_identity":
        """shell
            python3 ingest.py delete_batch_identity
        """
        # delete nodes from the IKG service
        # replace with your own values
        client_ingest = IngestClient()
        # id in external source / type of node : pair must be unique
        # create node object with the elements
        node1 = client_ingest.node_match("GwzaIdAKwRoHsed", "Person")
        node2 = client_ingest.node_match("OAnsyxYKXfffDyd", "Person")
        # send the deletion request and get the response
        delete_batch_node = client_ingest.batch_delete_nodes([node1, node2])
        if delete_batch_node:
            api_helper.print_response(delete_batch_node)
        else:
            print("Invalid delete")
        client_ingest.channel.close()
        return delete_batch_node

    elif command == "delete_batch_node_properties":
        """shell
            python3 ingest.py delete_batch_node_properties
        """
        # delete node properties from the IKG service
        # replace with your own values
        client_ingest = IngestClient()
        # id in external source / type of node : pair must be unique
        match = client_ingest.node_match("CuvOSTKOnQZaaXh", "Person")
        property_type = "nodePropertyName"
        node_property = client_ingest.node_property_match(match, property_type)
        match2 = client_ingest.node_match("YrZKEfErhJkqMCb", "Person")
        property_type2 = "nodePropertyName2"
        node_property2 = client_ingest.node_property_match(match2, property_type2)
        # send the deletion request and get the response
        delete_batch_node_properties = client_ingest.batch_delete_node_properties([node_property, node_property2])
        if delete_batch_node_properties:
            api_helper.print_response(delete_batch_node_properties)
        else:
            print("Invalid delete")
        client_ingest.channel.close()
        return delete_batch_node_properties

    elif command == "ingest_batch_relationship":
        """shell
            python3 ingest.py ingest_batch_relationship
        """
        # ingest identity nodes in the IKG service
        # replace with your own values
        client_ingest = IngestClient()
        # unique value which can be random
        record_id = str(uuid.uuid4())
        # unique id in external source
        external_id = ''.join(random.choices(string.ascii_letters, k=15))
        print(external_id)
        external_id2 = ''.join(random.choices(string.ascii_letters, k=15))
        print(external_id2)
        # type of relationship
        type = "BELONGS_TO"
        # id in external source / type of node : pair must be unique
        source_match = client_ingest.node_match("sXNBVfuDBlCufim", "Car")
        target_match = client_ingest.node_match("GwzaIdAKwRoHsed", "Person")
        source_match2 = client_ingest.node_match("AAhcJsczfCYloyg", "Car")
        target_match2 = client_ingest.node_match("OAnsyxYKXfffDyd", "Person")
        # create upsert object with all elements
        relationship1 = client_ingest.data_relationship(source_match, target_match, type,[])
        relationship2 = client_ingest.data_relationship(source_match2, target_match2, type, [])

        # send the ingestion request and get the response
        ingest = client_ingest.batch_upsert_relationships([relationship1, relationship2])
        if ingest:
            api_helper.print_response(ingest)
        else:
            print("Invalid upsert")
        client_ingest.channel.close()
        return ingest

    elif command == "delete_batch_relationship":
        """shell
            python3 ingest.py delete_batch_relationship
        """
        # delete nodes from the IKG service
        # replace with your own values
        client_ingest = IngestClient()
        # id in external source / type of node : pair must be unique
        # type of relationship
        type = "BELONGS_TO"
        # id in external source / type of node : pair must be unique
        source_match = client_ingest.node_match("sXNBVfuDBlCufim", "Car")
        target_match = client_ingest.node_match("GwzaIdAKwRoHsed", "Person")
        source_match2 = client_ingest.node_match("AAhcJsczfCYloyg", "Car")
        target_match2 = client_ingest.node_match("OAnsyxYKXfffDyd", "Person")
        # create upsert object with all elements
        relationship1 = client_ingest.data_relationship(source_match, target_match, type, [])
        relationship2 = client_ingest.data_relationship(source_match2, target_match2, type, [])
        # send the deletion request and get the response
        delete_batch_relationship = client_ingest.batch_delete_relationships([relationship1, relationship2])
        if delete_batch_relationship:
            api_helper.print_response(delete_batch_relationship)
        else:
            print("Invalid delete")
        client_ingest.channel.close()
        return delete_batch_relationship

    elif command == "delete_batch_relationship_properties":
        """shell
            python3 ingest.py delete_batch_relationship_properties
        """
        # delete node properties from the IKG service
        # replace with your own values
        client_ingest = IngestClient()
        type = "BELONGS_TO"
        # id in external source / type of node : pair must be unique
        source_match = client_ingest.node_match("HLEgiljrtoNEiyX", "Car")
        target_match = client_ingest.node_match("tSMiFkHozbhtfQZ", "Person")
        source_match2 = client_ingest.node_match("HLEgiljrtoNEiyX", "Car")
        target_match2 = client_ingest.node_match("tSMiFkHozbhtfQZ", "Person")
        property_type = "relationPropertyName"
        # create relationship property object with all elements
        relation_property = client_ingest.relationship_property_match(source_match, target_match, type, property_type)
        relation_property2 = client_ingest.relationship_property_match(source_match2, target_match2, type, property_type)
        # send the deletion request and get the response
        delete_batch_relationship_properties = client_ingest.batch_delete_relationship_properties(
            [relation_property, relation_property2])
        if delete_batch_relationship_properties:
            api_helper.print_response(delete_batch_relationship_properties)
        else:
            print("Invalid delete")
        client_ingest.channel.close()
        return delete_batch_relationship_properties


if __name__ == '__main__':  # pragma: no cover
    main()
