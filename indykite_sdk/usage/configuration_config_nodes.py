"""
Commandline interface for making an API request with the SDK.
"""
import argparse
from datetime import datetime
import json
import numpy as np

from indykite_sdk.config import ConfigClient
from indykite_sdk import api_helper
from indykite_sdk.indykite.config.v1beta1 import model_pb2


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
    # read_config_node
    read_config_node_parser = subparsers.add_parser("read_config_node")
    read_config_node_parser.add_argument("config_node_id", help="Config node id (gid)")

    # delete_config_node
    delete_config_node_parser = subparsers.add_parser("delete_config_node")
    delete_config_node_parser.add_argument("config_node_id", help="Config node id (gid)")
    delete_config_node_parser.add_argument("etag", help="Etag")

    # list_config_node_versions
    list_config_node_versions_parser = subparsers.add_parser("list_config_node_versions")
    list_config_node_versions_parser.add_argument("config_node_id", help="Config node id (gid)")

    # create_authorization_policy_config_node
    create_authorization_policy_config_node_parser = subparsers.add_parser("create_authorization_policy_config_node")
    create_authorization_policy_config_node_parser.add_argument("app_space_id", help="AppSpace (gid)")
    create_authorization_policy_config_node_parser.add_argument("name", help="Name (not display name)")
    create_authorization_policy_config_node_parser.add_argument("display_name", help="Display name")
    create_authorization_policy_config_node_parser.add_argument("description", help="Description")

    # update_authorization_policy_config_node
    update_authorization_policy_config_node_parser = subparsers.add_parser("update_authorization_policy_config_node")
    update_authorization_policy_config_node_parser.add_argument("config_node_id", help="Config node id (gid)")
    update_authorization_policy_config_node_parser.add_argument("etag", help="Etag")
    update_authorization_policy_config_node_parser.add_argument("display_name", help="Display name")
    update_authorization_policy_config_node_parser.add_argument("description", help="Description")

    # create_consent_config_node
    create_consent_config_node_parser = subparsers.add_parser("create_consent_config_node")
    create_consent_config_node_parser.add_argument("app_space_id", help="AppSpace (gid)")
    create_consent_config_node_parser.add_argument("name", help="Name (not display name)")
    create_consent_config_node_parser.add_argument("display_name", help="Display name")
    create_consent_config_node_parser.add_argument("description", help="Description")
    create_consent_config_node_parser.add_argument("application_id", help="Application (gid)")

    # update_consent_config_node
    update_consent_config_node_parser = subparsers.add_parser("update_consent_config_node")
    update_consent_config_node_parser.add_argument("config_node_id", help="Config node id (gid)")
    update_consent_config_node_parser.add_argument("etag", help="Etag")
    update_consent_config_node_parser.add_argument("display_name", help="Display name")
    update_consent_config_node_parser.add_argument("description", help="Description")
    update_consent_config_node_parser.add_argument("application_id", help="Application (gid)")

    # create_token_introspect_config_node
    create_token_introspect_config_node_parser = subparsers.add_parser("create_token_introspect_config_node")
    create_token_introspect_config_node_parser.add_argument("app_space_id", help="AppSpace (gid)")
    create_token_introspect_config_node_parser.add_argument("name", help="Name (not display name)")
    create_token_introspect_config_node_parser.add_argument("display_name", help="Display name")
    create_token_introspect_config_node_parser.add_argument("description", help="Description")

    # update_token_introspect_config_node
    update_token_introspect_config_node_parser = subparsers.add_parser("update_token_introspect_config_node")
    update_token_introspect_config_node_parser.add_argument("config_node_id", help="Config node id (gid)")
    update_token_introspect_config_node_parser.add_argument("etag", help="Etag")
    update_token_introspect_config_node_parser.add_argument("display_name", help="Display name")
    update_token_introspect_config_node_parser.add_argument("description", help="Description")

    # create_external_data_resolver_config_node
    create_external_data_resolver_config_node_parser = subparsers.add_parser("create_external_data_resolver_config_node")
    create_external_data_resolver_config_node_parser.add_argument("app_space_id", help="AppSpace (gid)")
    create_external_data_resolver_config_node_parser.add_argument("name", help="Name (not display name)")
    create_external_data_resolver_config_node_parser.add_argument("display_name", help="Display name")
    create_external_data_resolver_config_node_parser.add_argument("description", help="Description")

    # update_external_data_resolver_config_node
    update_external_data_resolver_config_node_parser = subparsers.add_parser("update_external_data_resolver_config_node")
    update_external_data_resolver_config_node_parser.add_argument("config_node_id", help="Config node id (gid)")
    update_external_data_resolver_config_node_parser.add_argument("etag", help="Etag")
    update_external_data_resolver_config_node_parser.add_argument("display_name", help="Display name")
    update_external_data_resolver_config_node_parser.add_argument("description", help="Description")

    # create_entity_matching_pipeline_config_node
    create_entity_matching_pipeline_config_node_parser = subparsers.add_parser("create_entity_matching_pipeline_config_node")
    create_entity_matching_pipeline_config_node_parser.add_argument("app_space_id", help="AppSpace (gid)")
    create_entity_matching_pipeline_config_node_parser.add_argument("name", help="Name (not display name)")
    create_entity_matching_pipeline_config_node_parser.add_argument("display_name", help="Display name")
    create_entity_matching_pipeline_config_node_parser.add_argument("description", help="Description")

    # update_entity_matching_pipeline_config_node
    update_entity_matching_pipeline_config_node_parser = subparsers.add_parser("update_entity_matching_pipeline_config_node")
    update_entity_matching_pipeline_config_node_parser.add_argument("config_node_id", help="Config node id (gid)")
    update_entity_matching_pipeline_config_node_parser.add_argument("etag", help="Etag")
    update_entity_matching_pipeline_config_node_parser.add_argument("display_name", help="Display name")
    update_entity_matching_pipeline_config_node_parser.add_argument("description", help="Description")

    args = parser.parse_args()
    command = args.command

    if command == "read_config_node":
        # to get info for any given config node (AuthorizationPolicyConfig, ConsentConfiguration)
        client_config = ConfigClient()
        config_node_id = args.config_node_id
        version = 0
        config_node = client_config.read_config_node(config_node_id, version)
        if config_node:
            # print(config_node.token_introspect_config.jwt)
            # print(config_node.token_introspect_config.offline)
            api_helper.print_response(config_node)
        else:
            print("Invalid config node id")
        client_config.channel.close()

    elif command == "delete_config_node":
        # to delete any given config node (AuthorizationPolicyConfig, ConsentConfiguration)
        client_config = ConfigClient()
        config_node_id = args.config_node_id
        etag = args.etag
        config_node = client_config.delete_config_node(config_node_id, etag, [])
        if config_node:
            api_helper.print_response(config_node)
        else:
            print("Invalid delete config node response")

    elif command == "list_config_node_versions":
        #  list all versions of a given config node (AuthorizationPolicyConfig, ConsentConfiguration)
        client_config = ConfigClient()
        config_node_id = args.config_node_id
        list_config_nodes = client_config.list_config_node_versions(config_node_id)
        if list_config_nodes:
            api_helper.print_response(list_config_nodes)
        else:
            print("Invalid list_config_nodes response")
        client_config.channel.close()
        return list_config_nodes

    elif command == "create_authorization_policy_config_node":
        # to create an authorization policy config node to query against in authorization requests
        """shell
           python3 configuration_config_nodes.py create_authorization_policy_config_node
           APP_SPACE_ID POLICY_NAME POLICY_DISPLAY_NAME POLICY_DESCRIPTION
        """
        client_config = ConfigClient()
        location = args.app_space_id
        name = args.name
        display_name = args.display_name
        description = args.description
        # replace the json file by your own
        with open("../utils/sdk_policy_config.json") as f:
            file_data = f.read()
        policy_dict = json.loads(file_data)
        policy_dict = json.dumps(policy_dict)
        policy_config = client_config.authorization_policy_config(
            policy=str(policy_dict),
            status="STATUS_ACTIVE",
            tags=[]
        )
        create_authorization_policy_config_node_response = client_config.create_authorization_policy_config_node(
            location,
            name,
            display_name,
            description,
            policy_config
        )

        if create_authorization_policy_config_node_response:
            api_helper.print_response(create_authorization_policy_config_node_response)
        else:
            print("Invalid create authorization policy config node response")
        client_config.channel.close()
        return create_authorization_policy_config_node_response

    elif command == "update_authorization_policy_config_node":
        # to update an authorization policy config node to query against in authorization requests
        client_config = ConfigClient()
        config_node_id = args.config_node_id
        etag = args.etag
        display_name = args.display_name
        description = args.description
        with open("../utils/sdk_policy_config.json") as f:
            file_data = f.read()
        policy_dict = json.loads(file_data)
        policy_dict = json.dumps(policy_dict)
        policy_config = client_config.authorization_policy_config(
            policy=str(policy_dict),
            status="STATUS_ACTIVE",
            tags=["TagOne"]
        )

        update_authorization_policy_config_node_response = client_config.update_authorization_policy_config_node(
            config_node_id,
            etag,
            display_name,
            description,
            policy_config
        )
        if update_authorization_policy_config_node_response:
            api_helper.print_response(update_authorization_policy_config_node_response)
        else:
            print("Invalid update authorization policy config node response")
        client_config.channel.close()
        return update_authorization_policy_config_node_response

    elif command == "create_consent_config_node":
        # to create a consent config node to query against in trusted data access
        """shell
           python3 configuration_config_nodes.py create_consent_config_node
           APP_SPACE_ID CONSENT_NAME CONSENT_DISPLAY_NAME CONSENT_DESCRIPTION APPLICATION_ID
        """
        client_config = ConfigClient()
        location = args.app_space_id
        name = args.name
        display_name = args.display_name
        description = args.description
        application_id = args.application_id
        # replace the json file by your own
        consent_config = ConfigClient().consent_config(
            purpose="Taking control2",
            data_points=["{\"query\": \"-[:OWNS]->(car:Car)\", "
                         "\"returns\": [{\"variable\": \"car\", \"properties\": [\"vin\"]}]}"],
            application_id=application_id,
            validity_period=86400,
            revoke_after_use=False,
            token_status=3
        )
        create_consent_config_node_response = client_config.create_consent_config_node(
            location,
            name,
            display_name,
            description,
            consent_config
        )

        if create_consent_config_node_response:
            api_helper.print_response(create_consent_config_node_response)
        else:
            print("Invalid create consent config node response")
        client_config.channel.close()
        return create_consent_config_node_response

    elif command == "update_consent_config_node":
        # to update a consent config node to query against in trusted data access
        client_config = ConfigClient()
        config_node_id = args.config_node_id
        etag = args.etag
        display_name = args.display_name
        description = args.description
        application_id = args.application_id
        consent_config = ConfigClient().consent_config(
            purpose="Taking control",
            data_points=["{ \"query\": \"-[:OWNS]-(car:Car)\", \"returns\": [ { \"variable\": \"car\"," +
                         "\"properties\": [\"plateNumber\"] } ] }"],
            application_id=application_id,
            validity_period=86400,
            revoke_after_use=False,
            token_status=2
        )

        update_consent_config_node_response = client_config.update_consent_config_node(
            config_node_id,
            etag,
            display_name,
            description,
            consent_config
        )
        if update_consent_config_node_response:
            api_helper.print_response(update_consent_config_node_response)
        else:
            print("Invalid update consent config node response")
        client_config.channel.close()
        return update_consent_config_node_response

    elif command == "create_token_introspect_config_node":
        # to create a token introspect config node
        """shell
           python3 configuration_config_nodes.py create_token_introspect_config_node
           APP_SPACE_ID TOKEN_NAME TOKEN_DISPLAY_NAME TOKEN_DESCRIPTION
        """
        client_config = ConfigClient()
        location = args.app_space_id
        name = args.name
        display_name = args.display_name
        description = args.description
        # replace the json file by your own
        # token_matcher = oneof TokenIntrospectConfig.JWT, TokenIntrospectConfig.Opaque
        jwt = model_pb2.TokenIntrospectConfig.JWT(
            issuer="https://myself.com",
            audience="id-of-the-audience"
        )
        # opaque = model_pb2.TokenIntrospectConfig.Opaque()
        # validation = oneof TokenIntrospectConfig.Offline, TokenIntrospectConfig.Online
        # offline only with jwt
        offline = model_pb2.TokenIntrospectConfig.Offline(
            public_jwks=[
                json.dumps({"kid": "abc", "use": "sig", "alg": "RS256", "n": "--nothing-real-just-random-xyqwerasf--",
                            "kty": "RSA"}).encode('utf-8'),
                json.dumps({"kid": "jkl", "use": "sig", "alg": "RS256", "n": "--nothing-real-just-random-435asdf43--",
                            "kty": "RSA"}).encode('utf-8')
            ]
        )
        # online = model_pb2.TokenIntrospectConfig.Online(user_info_endpoint="https://data.example.com/userinfo",
        # cache_ttl=3600)
        token_introspect_config = ConfigClient().token_introspect_config(
            token_matcher={'jwt': jwt},
            validation={'offline': offline},
            claims_mapping={"email": "mail", "name":"full_name"},
            ikg_node_type="Person",
            perform_upsert=True
        )
        create_token_introspect_config_node_response = client_config.create_token_introspect_config_node(
            location,
            name,
            display_name,
            description,
            token_introspect_config
        )

        if create_token_introspect_config_node_response:
            api_helper.print_response(create_token_introspect_config_node_response)
        else:
            print("Invalid create token introspect config node response")
        client_config.channel.close()
        return create_token_introspect_config_node_response

    elif command == "update_token_introspect_config_node":
        # to update a token introspect config node
        client_config = ConfigClient()
        config_node_id = args.config_node_id
        etag = args.etag
        display_name = args.display_name
        description = args.description
        # token_matcher = oneof TokenIntrospectConfig.JWT, TokenIntrospectConfig.Opaque
        jwt = model_pb2.TokenIntrospectConfig.JWT(
            issuer="https://example.com",
            audience="audience-id"
        )
        # opaque = model_pb2.TokenIntrospectConfig.Opaque()
        # validation = oneof TokenIntrospectConfig.Offline, TokenIntrospectConfig.Online
        # offline only with jwt
        offline = model_pb2.TokenIntrospectConfig.Offline(
            public_jwks=[
                json.dumps({"kid": "abc", "use": "sig", "alg": "RS256", "n": "--nothing-real-just-random-xyqwerasf--",
                            "kty": "RSA"}).encode('utf-8'),
                json.dumps({"kid": "jkl", "use": "sig", "alg": "RS256", "n": "--nothing-real-just-random-435asdf43--",
                            "kty": "RSA"}).encode('utf-8')
            ]
        )
        # online = model_pb2.TokenIntrospectConfig.Online(user_info_endpoint="https://data.example.com/userinfo",
        # cache_ttl=3600)
        token_introspect_config = ConfigClient().token_introspect_config(
            token_matcher={'jwt': jwt},
            validation={'offline': offline},
            claims_mapping={"email": "mail", "name": "full_name"},
            ikg_node_type="Person",
            perform_upsert=True
        )

        update_token_introspect_config_node_response = client_config.update_token_introspect_config_node(
            config_node_id,
            etag,
            display_name,
            description,
            token_introspect_config
        )
        if update_token_introspect_config_node_response:
            api_helper.print_response(update_token_introspect_config_node_response)
        else:
            print("Invalid update token introspect config node response")
        client_config.channel.close()
        return update_token_introspect_config_node_response

    elif command == "create_external_data_resolver_config_node":
        # to create an external data resolver config node
        """shell
           python3 configuration_config_nodes.py create_external_data_resolver_config_node
           APP_SPACE_ID RESOLVER_NAME RESOLVER_DISPLAY_NAME RESOLVER_DESCRIPTION
        """
        client_config = ConfigClient()
        location = args.app_space_id
        name = args.name
        display_name = args.display_name
        description = args.description
        # Create headers (which is a map<string, ExternalDataResolverConfig.Header>)
        header1 = model_pb2.ExternalDataResolverConfig.Header()
        header1.values.extend(["Authorization", "Bearer token_value"])

        header2 = model_pb2.ExternalDataResolverConfig.Header()
        header2.values.extend(["Content-Type", "application/json"])

        # Populate the headers map
        headers = {"AuthHeader": header1, "ContentHeader": header2}
        external_data_resolver_config = ConfigClient().external_data_resolver_config(
            url="https://example.com/source2",
            method="GET",
            headers=headers,
            request_type=1,
            request_payload=b'{"url": "source2", "method": "GET"}',
            response_type=1,
            response_selector="."
        )

        create_external_data_resolver_config_node_response = client_config.create_external_data_resolver_config_node(
            location,
            name,
            display_name,
            description,
            external_data_resolver_config
        )

        if create_external_data_resolver_config_node_response:
            api_helper.print_response(create_external_data_resolver_config_node_response)
        else:
            print("Invalid create external data resolver config node response")
        client_config.channel.close()
        return create_external_data_resolver_config_node_response

    elif command == "update_external_data_resolver_config_node":
        # to update an external data resolver config node
        client_config = ConfigClient()
        config_node_id = args.config_node_id
        etag = args.etag
        display_name = args.display_name
        description = args.description
        external_data_resolver_config = ConfigClient().external_data_resolver_config(
            url="https://example.com/source2",
            method="GET",
            request_type=1,
            request_payload=b'{"url": "source2", "method": "GET"}',
            response_type=1,
            response_selector="."
        )

        # Create headers (which is a map<string, ExternalDataResolverConfig.Header>)
        header1 =  model_pb2.ExternalDataResolverConfig.Header()
        header1.values.extend(["Authorization", "Bearer token_value"])

        header2 = model_pb2.ExternalDataResolverConfig.Header()
        header2.values.extend(["Content-Type", "application/json"])

        # Populate the headers map
        external_data_resolver_config.headers["AuthHeader"] = header1
        external_data_resolver_config.headers["ContentHeader"] = header2

        update_external_data_resolver_config_node_response = client_config.update_external_data_resolver_config_node(
            config_node_id,
            etag,
            display_name,
            description,
            external_data_resolver_config
        )
        if update_external_data_resolver_config_node_response:
            api_helper.print_response(update_external_data_resolver_config_node_response)
        else:
            print("Invalid update external data resolver config node response")
        client_config.channel.close()
        return update_external_data_resolver_config_node_response

    elif command == "create_entity_matching_pipeline_config_node":
        # to create an entity matching pipeline config node
        """shell
           python3 configuration_config_nodes.py create_entity_matching_pipeline_config_node
           APP_SPACE_ID EM_NAME EM_DISPLAY_NAME EM_DESCRIPTION
        """
        client_config = ConfigClient()
        location = args.app_space_id
        name = args.name
        display_name = args.display_name
        description = args.description
        t = datetime.now()
        node_filter = model_pb2.EntityMatchingPipelineConfig.NodeFilter()
        node_filter.source_node_types.extend(["Person"])
        node_filter.target_node_types.extend(["Person"])
        entity_matching_pipeline_config = ConfigClient().entity_matching_pipeline_config(
            node_filter=node_filter,
            similarity_score_cutoff=np.float32(0.9),
            property_mapping_status=1,
            entity_matching_status=1,
            property_mappings=[],
            rerun_interval="1 day",
            last_run_time=t,
            report_url="gs://some-path",
            report_type="csv"
        )

        create_entity_matching_pipeline_config_node_response = client_config.create_entity_matching_pipeline_config_node(
            location,
            name,
            display_name,
            description,
            entity_matching_pipeline_config
        )

        if create_entity_matching_pipeline_config_node_response:
            api_helper.print_response(create_entity_matching_pipeline_config_node_response)
        else:
            print("Invalid create entity matching pipeline config node response")
        client_config.channel.close()
        return create_entity_matching_pipeline_config_node_response

    elif command == "update_entity_matching_pipeline_config_node":
        # to update an entity matching pipeline config node
        client_config = ConfigClient()
        config_node_id = args.config_node_id
        etag = args.etag
        display_name = args.display_name
        description = args.description
        node_filter = model_pb2.EntityMatchingPipelineConfig.NodeFilter()
        node_filter.source_node_types.extend(["employee", "technician"])
        node_filter.target_node_types.extend(["user", "customer"])
        entity_matching_pipeline_config = ConfigClient().entity_matching_pipeline_config(
            node_filter=node_filter
        )
        update_entity_matching_pipeline_config_node_response = client_config.update_entity_matching_pipeline_config_node(
            config_node_id,
            etag,
            display_name,
            description,
            entity_matching_pipeline_config
        )
        if update_entity_matching_pipeline_config_node_response:
            api_helper.print_response(update_entity_matching_pipeline_config_node_response)
        else:
            print("Invalid update entity matching pipeline config node response")
        client_config.channel.close()
        return update_entity_matching_pipeline_config_node_response


if __name__ == '__main__':  # pragma: no cover
    main()
