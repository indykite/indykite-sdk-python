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
        ingest_property1 = client_ingest.ingest_property("first_name", "deer")
        ingest_property2 = client_ingest.ingest_property("last_name", "grumpy")
        ingest_property3 = client_ingest.ingest_property("birthdate", "20 Sep, 1977")
        ingest_property4 = client_ingest.ingest_property("role", "Employee")
        ingest_property5 = client_ingest.ingest_property("email", "grumpy@yahoo.uk")
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


if __name__ == '__main__':  # pragma: no cover
    main()
