"""
Commandline interface for making an API request with the SDK.
"""
import argparse
import numpy as np
from indykite_sdk.entitymatching import EntityMatchingClient
from indykite_sdk.indykite.entitymatching.v1beta1 import model_pb2
from indykite_sdk import api_helper



class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):  # pragma: no cover
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value


def main():
    # Create parent parser
    parser = argparse.ArgumentParser(description="EntityMatching client API.")
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    # Create child parsers
    # entitymatching
    read_suggested_property_mapping_parser = subparsers.add_parser("read_suggested_property_mapping")
    read_suggested_property_mapping_parser.add_argument("id", help="EntityMatching pipeline id (gid)")
    run_entity_matching_pipeline_parser = subparsers.add_parser("run_entity_matching_pipeline")
    run_entity_matching_pipeline_parser.add_argument("id", help="EntityMatching pipeline id (gid)")
    args = parser.parse_args()
    command = args.command

    if command == "read_suggested_property_mapping":
        """shell
            python3 entitymatching.py read_suggested_property_mapping config_node_id
        """
        # read an entitymatching config node
        # replace with your own values
        client_entitymatching = EntityMatchingClient()
        id = args.id
        # send the read entity matching report request and get the response
        read_suggested_property_mapping = client_entitymatching.read_suggested_property_mapping(id)
        if read_suggested_property_mapping:
            api_helper.print_response(read_suggested_property_mapping)
        else:
            print("Invalid read_suggested_property_mapping")
        client_entitymatching.channel.close()
        return read_suggested_property_mapping

    elif command == "run_entity_matching_pipeline":
        """shell
            python3 entitymatching.py run_entity_matching_pipeline config_node_id
        """
        # ingest identity nodes in the IKG service
        # replace with your own values
        client_entitymatching = EntityMatchingClient()
        id = args.id
        similarity_score_cutoff=np.float32(0.95)
        custom_property_mappings = model_pb2.CustomPropertyMappings(
            source_node_property="email",
            target_node_property="email"
        )
        # run the pipeline and get the response
        run_entity_matching_pipeline = client_entitymatching.run_entity_matching_pipeline(
            id=id,
            similarity_score_cutoff=similarity_score_cutoff,
            custom_property_mappings=custom_property_mappings
        )
        if run_entity_matching_pipeline:
            api_helper.print_response(run_entity_matching_pipeline)
        else:
            print("Invalid run_entity_matching_pipeline")
        client_entitymatching.channel.close()
        return run_entity_matching_pipeline


if __name__ == '__main__':  # pragma: no cover
    main()
