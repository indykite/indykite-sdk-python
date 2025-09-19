"""Commandline interface for making an API request with the SDK."""

import argparse
from datetime import datetime

from indykite_sdk import api_helper
from indykite_sdk.indykite.knowledge.v1beta2.model_pb2 import Return as ReturnKnowledge
from indykite_sdk.knowledge import KnowledgeClient
from indykite_sdk.model.identity_knowledge import Metadata
from indykite_sdk.model.identity_knowledge import Node as NodeModel
from indykite_sdk.utils.message_to_value import param_to_value


class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):  # pragma: no cover
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split("=")
            getattr(namespace, self.dest)[key] = value


def main():
    # Create parent parser
    parser = argparse.ArgumentParser(description="Knowledge client API.")
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    # Create child parsers
    # knowledge
    read_identity_knowledge_parser = subparsers.add_parser("read_identity_knowledge")

    get_identity_by_id_parser = subparsers.add_parser("get_identity_by_id")
    get_identity_by_id_parser.add_argument("id", help="Identity node gid (node with is_identity equal True)")

    get_identity_by_identifier_parser = subparsers.add_parser("get_identity_by_identifier")
    get_identity_by_identifier_parser.add_argument("external_id", help="Identity node external id")
    get_identity_by_identifier_parser.add_argument("type", help="DT type")

    get_node_by_id_parser = subparsers.add_parser("get_node_by_id")
    get_node_by_id_parser.add_argument("id", help="Resource gid id")

    get_node_by_identifier_parser = subparsers.add_parser("get_node_by_identifier")
    get_node_by_identifier_parser.add_argument("external_id", help="Resource external id")
    get_node_by_identifier_parser.add_argument("type", help="Resource type")

    list_identities_parser = subparsers.add_parser("list_identities")
    list_nodes_parser = subparsers.add_parser("list_nodes")
    list_identities_by_property_parser = subparsers.add_parser("list_identities_by_property")
    list_nodes_by_property_parser = subparsers.add_parser("list_nodes_by_property")
    get_property_parser = subparsers.add_parser("get_property")
    get_metadata_parser = subparsers.add_parser("get_metadata")
    delete_all_nodes_parser = subparsers.add_parser("delete_all_nodes")
    delete_all_nodes_parser.add_argument("node_type", help="DigitalTwin, Resource")

    args = parser.parse_args()
    command = args.command

    if command == "read_identity_knowledge":
        """shell
            python3 knowledge.py read_identity_knowledge
        """
        # send a request to the knowledge API with query, input_params and returns parameters
        # and get a response
        # replace with your own values
        client_knowledge = KnowledgeClient()
        # parameters used in the cypher query
        input_params = {"external_id": "lFtAeWXGjfDEhEz", "type": "Person"}
        # cypher query
        # query = "MATCH (n:Resource) WHERE n.external_id = $external_id and n.type=$type"
        query = "MATCH (c:Car)<-[r:OWNS]-(n:Resource) WHERE n.external_id = $external_id and n.type=$type"
        # elements you want returned:
        # variable: cypher table
        # properties: empty = all info elements or array = all properties you want returned
        returns = [ReturnKnowledge(variable="r"), ReturnKnowledge(variable="n")]
        # [{variable: 'o', properties: []}, {variable: 'r', properties: []}]
        responses = client_knowledge.identity_knowledge_read(query, input_params, returns)
        api_helper.print_response(responses)
        client_knowledge.channel.close()

    elif command == "get_identity_by_id":
        """shell
            python3 knowledge.py get_identity_by_id
        """
        # send a request to the knowledge API with identity node gid
        # and get the node info
        client_knowledge = KnowledgeClient()
        id = args.id
        response = client_knowledge.get_identity_by_id(id)
        if response:
            api_helper.print_response(response)
        else:
            print("No result")
        client_knowledge.channel.close()

    elif command == "get_identity_by_identifier":
        """shell
            python3 knowledge.py get_identity_by_identifier
        """
        # send a request to the knowledge API with identity node identifier (external_id + type)
        # and get the node info
        client_knowledge = KnowledgeClient()
        external_id = args.external_id
        type = args.type
        responses = client_knowledge.get_identity_by_identifier(external_id, type)
        if responses:
            for response in responses:
                api_helper.print_response(response)
        else:
            print("No result")
        client_knowledge.channel.close()

    elif command == "get_node_by_id":
        """shell
            python3 knowledge.py get_node_by_id
        """
        # send a request to the knowledge API with node gid
        # and get the node info
        client_knowledge = KnowledgeClient()
        id = args.id
        response = client_knowledge.get_node_by_id(id)
        if response:
            api_helper.print_response(response)
        else:
            print("No result")
        client_knowledge.channel.close()

    elif command == "get_node_by_identifier":
        """shell
            python3 knowledge.py get_node_by_identifier
        """
        # send a request to the knowledge API with node identifier (external_id + type)
        # and get the node info
        client_knowledge = KnowledgeClient()
        external_id = args.external_id
        type = args.type
        responses = client_knowledge.get_node_by_identifier(external_id, type)
        if responses:
            for response in responses:
                api_helper.print_response(response)
        else:
            print("No result")
        client_knowledge.channel.close()

    elif command == "list_nodes":
        """shell
            python3 knowledge.py list_nodes
        """
        # send a request to the knowledge API
        # and get all nodes info
        client_knowledge = KnowledgeClient()
        responses = client_knowledge.list_nodes()
        if responses:
            for response in responses:
                api_helper.print_response(response)
        else:
            print("No result")
        client_knowledge.channel.close()

    elif command == "list_identities":
        """shell
            python3 knowledge.py list_identities
        """
        # send a request to the knowledge API
        # and get all identity nodes info
        client_knowledge = KnowledgeClient()
        responses = client_knowledge.list_identities()
        if responses:
            for response in responses:
                print(vars(response))
        else:
            print("No result")
        client_knowledge.channel.close()

    elif command == "list_nodes_by_property":
        """shell
            python3 knowledge.py list_nodes_by_property
        """
        # send a request to the knowledge API with a property
        # and get all nodes having the property
        # replace with your own values
        client_knowledge = KnowledgeClient()
        # replace by own values
        property = {"last_name": "mushu"}
        responses = client_knowledge.list_nodes_by_property(property)
        if responses:
            for response in responses:
                print(vars(response))
        else:
            print("No result")
        client_knowledge.channel.close()

    elif command == "list_identities_by_property":
        """shell
            python3 knowledge.py list_identities_by_property
        """
        # send a request to the knowledge API with a property
        # and get all identity nodes having the property
        # replace with your own values
        client_knowledge = KnowledgeClient()
        # replace by own values
        property = {"last_name": "mushu"}
        responses = client_knowledge.list_identities_by_property(property)
        if responses:
            for response in responses:
                print(vars(response))
        else:
            print("No result")
        client_knowledge.channel.close()

    elif command == "get_property":
        # get property from a specific node
        # replace with your own values
        node1 = NodeModel(
            id="gid:AAAAFVCygmDZtk8KtTtw9CBopC8",
            external_id="PEpkjOvUJQvqTFw",
            type="individual",
            tags=[],
            properties=[{"key": "last_name", "value": {"stringValue": "mushu"}}],
        )
        property1 = node1.get_property(node1, "last_name")
        print(property1)

    elif command == "get_metadata":
        # get metadata from a specific property
        # replace with your own values
        metadata1 = Metadata(
            assurance_level=1,
            verification_time=datetime.now().timestamp(),
            source="Myself",
            custom_metadata={"customData": param_to_value("customValue")},
        )
        node1 = NodeModel(
            id="gid:AAAAFVCygmDZtk8KtTtw9CBopC8",
            external_id="PEpkjOvUJQvqTFw",
            type="individual",
            tags=[],
            properties=[{"key": "last_name", "value": {"stringValue": "mushu"}, "metadata": metadata1}],
        )
        metadata1 = node1.get_metadata(node1, "last_name")
        print(print(metadata1.__dir__()))

    elif command == "delete_all_nodes":
        """shell
            python3 knowledge.py ingest_record_resource
        """
        # send a request to the knowledge API to delete all nodes of given type
        client_knowledge = KnowledgeClient()
        responses = client_knowledge.delete_all_with_node_type(args.node_type)
        if responses:
            for response in responses:
                api_helper.print_response(response)
        else:
            print("No result")
        client_knowledge.channel.close()


if __name__ == "__main__":  # pragma: no cover
    main()
