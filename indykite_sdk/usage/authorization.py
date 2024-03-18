"""
Commandline interface for making an API request with the SDK.
"""
import argparse
from indykite_sdk.authorization import AuthorizationClient
from indykite_sdk.model.is_authorized import IsAuthorizedResource
from indykite_sdk.model.what_authorized import WhatAuthorizedResourceTypes
from indykite_sdk.model.who_authorized import WhoAuthorizedResource
from indykite_sdk import api_helper


class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):  # pragma: no cover
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value


def main():
    # Create parent parser
    parser = argparse.ArgumentParser(description="Authorization client API.")
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    # Create child parsers
    # is_authorized_identity_node
    is_authorized_identity_node_parser = subparsers.add_parser("is_authorized_identity_node")
    is_authorized_identity_node_parser.add_argument("identity_node",
                                                    help="Identity node gid (node with is_identity equal True)")

    # is_authorized_token
    is_authorized_token_parser = subparsers.add_parser("is_authorized_token")
    is_authorized_token_parser.add_argument("access_token")

    # is_authorized_property
    is_authorized_property_parser = subparsers.add_parser("is_authorized_property")
    is_authorized_property_parser.add_argument("property_type", help="Identity node Property")
    is_authorized_property_parser.add_argument("property_value", help="Identity node Property value")

    # is_authorized_external_id
    is_authorized_external_id_parser = subparsers.add_parser("is_authorized_external_id")
    is_authorized_external_id_parser.add_argument("type", help="Identity node type")
    is_authorized_external_id_parser.add_argument("external_id", help="Identity node external id")

    # what_authorized_dt
    what_authorized_dt_parser = subparsers.add_parser("what_authorized_dt")
    what_authorized_dt_parser.add_argument("identity_node",
                                           help="Identity node gid (node with is_identity equal True)")

    # what_authorized_token
    what_authorized_token_parser = subparsers.add_parser("what_authorized_token")
    what_authorized_token_parser.add_argument("access_token")

    # what_authorized_property
    what_authorized_property_parser = subparsers.add_parser("what_authorized_property")
    what_authorized_property_parser.add_argument("property_type", help="Identity node Identity Property")
    what_authorized_property_parser.add_argument("property_value", help="Identity node Identity Property value")

    # what_authorized_external_id
    what_authorized_external_id_parser = subparsers.add_parser("what_authorized_external_id")
    what_authorized_external_id_parser.add_argument("node_type", help="Identity node node type")
    what_authorized_external_id_parser.add_argument("external_id", help="Identity node external_id")

    # who_authorized
    who_authorized_parser = subparsers.add_parser("who_authorized")

    args = parser.parse_args()
    command = args.command
    if command == "is_authorized_dt":
        """shell
                python3 authorization.py is_authorized_dt IDENTITY_NODE_GID
        """
        # is a given subject, identified by its gid, authorized to have a specific action on specific resources
        # replace actions and resources according to your data
        client_authorization = AuthorizationClient()
        identity_node_id = args.identity_node_id
        actions = ["ACTION1", "ACTION2"]
        resources = [IsAuthorizedResource("resourceID", "TypeName", actions),
                     IsAuthorizedResource("resource2ID", "TypeName", actions)]
        input_params = {"age": "21"}
        policy_tags = ["Car", "Rental", "Sharing"]
        is_authorized = client_authorization.is_authorized_digital_twin(
            identity_node_id,
            resources,
            input_params,
            policy_tags)

        if is_authorized:
            api_helper.print_response(is_authorized)
        else:
            print("Invalid is_authorized")
        client_authorization.channel.close()
        return is_authorized

    elif command == "is_authorized_token":
        """shell
                python3 authorization.py is_authorized_token IDENTITY_NODE_USER_TOKEN
        """
        # is a given subject, identified by its user token, authorized to have a specific action on specific resources
        # replace actions and resources according to your data
        client_authorization = AuthorizationClient()
        access_token = args.access_token
        actions = ["ACTION1", "ACTION2"]
        resources = [IsAuthorizedResource("resourceID", "TypeName", actions),
                     IsAuthorizedResource("resource2ID", "TypeName", actions)]
        input_params = {}
        policy_tags = []
        is_authorized = client_authorization.is_authorized_token(access_token, resources, input_params, policy_tags)
        if is_authorized:
            api_helper.print_response(is_authorized)
        else:
            print("Invalid is_authorized")
        client_authorization.channel.close()
        return is_authorized

    elif command == "is_authorized_property":
        """shell
            python3 authorization.py is_authorized_property PROPERTY_TYPE PROPERTY_VALUE
        """
        # is a given subject, identified by its property, authorized to have a specific action on specific resources
        # replace actions and resources according to your data
        client_authorization = AuthorizationClient()
        property_type = args.property_type  # e.g "email"
        property_value = args.property_value  # e.g test@example.com
        actions = ["ACTION1", "ACTION2"]
        resources = [IsAuthorizedResource("resourceID", "TypeName", actions),
                     IsAuthorizedResource("resource2ID", "TypeName", actions)]
        input_params = {"age": "21"}
        policy_tags = []
        is_authorized = client_authorization.is_authorized_property_filter(
            property_type,
            property_value,
            resources,
            input_params,
            policy_tags)
        if is_authorized:
            api_helper.print_response(is_authorized)
        else:
            print("Invalid is_authorized")
        client_authorization.channel.close()
        return is_authorized

    elif command == "is_authorized_external_id":
        """shell
                python3 authorization.py is_authorized_external_id IDENTITY_NODE_EXTERNAL_ID
        """
        # is a given subject, identified by its external_id, authorized to have a specific action on specific resources
        # replace actions and resources according to your data
        client_authorization = AuthorizationClient()
        node_type = args.type
        external_id = args.external_id
        actions = ["SUBSCRIBES_TO"]
        resources = [IsAuthorizedResource("CCbJwkQtLOmCdLq", "Asset", actions),
                     IsAuthorizedResource("aXQMRIcTzyIyeKC", "Asset", actions)]
        input_params = {}
        policy_tags = []
        is_authorized = client_authorization.is_authorized_external_id(
            node_type,
            external_id,
            resources,
            input_params,
            policy_tags)

        if is_authorized:
            api_helper.print_response(is_authorized)
        else:
            print("Invalid is_authorized")
        client_authorization.channel.close()
        return is_authorized

    elif command == "what_authorized_dt":
        """shell
            python3 authorization.py what_authorized_dt IDENTITY_NODE_GID
        """
        # what a given subject, identified by its gid, is authorized to have specific actions on
        # replace actions and resources types according to your data
        client_authorization = AuthorizationClient()
        identity_node_id = args.identity_node
        actions = ["ACTION1", "ACTION2"]
        resource_types = [WhatAuthorizedResourceTypes("TypeName", actions),
                          WhatAuthorizedResourceTypes("TypeNameSecond", actions)]
        input_params = {"age": "21"}
        policy_tags = ["Car", "Rental", "Sharing"]
        what_authorized = client_authorization.what_authorized_digital_twin(
            identity_node_id,
            resource_types,
            input_params,
            policy_tags)

        if what_authorized:
            api_helper.print_response(what_authorized)
        else:
            print("Invalid what_authorized")
        client_authorization.channel.close()
        return what_authorized

    elif command == "what_authorized_token":
        """shell
            python3 authorization.py what_authorized_token IDENTITY_NODE_USER_TOKEN
        """
        # what a given subject, identified by its user token, is authorized to have specific actions on
        # replace actions and resources types according to your data
        client_authorization = AuthorizationClient()
        access_token = args.access_token
        actions = ["ACTION1", "ACTION2"]
        resource_types = [WhatAuthorizedResourceTypes("TypeName", actions),
                          WhatAuthorizedResourceTypes("TypeNameSecond", actions)]
        input_params = {}
        policy_tags = []
        what_authorized = client_authorization.what_authorized_token(access_token, resource_types, input_params,
                                                                     policy_tags)
        if what_authorized:
            api_helper.print_response(what_authorized)
        else:
            print("Invalid what_authorized")
        client_authorization.channel.close()
        return what_authorized

    elif command == "what_authorized_property":
        """shell
            python3 authorization.py what_authorized_property PROPERTY_TYPE PROPERTY_VALUE
        """
        # what a given subject, identified by its property, is authorized to have specific actions on
        # replace actions and resources types according to your data
        client_authorization = AuthorizationClient()
        property_type = args.property_type  # e.g "email"
        property_value = args.property_value  # e.g test@example.com
        actions = ["ACTION1", "ACTION2"]
        resource_types = [WhatAuthorizedResourceTypes("TypeName", actions),
                          WhatAuthorizedResourceTypes("TypeNameSecond", actions)]
        input_params = {"age": "21"}
        policy_tags = []
        what_authorized = client_authorization.what_authorized_property_filter(
            property_type,
            property_value,
            resource_types,
            input_params,
            policy_tags)
        if what_authorized:
            api_helper.print_response(what_authorized)
        else:
            print("Invalid what_authorized")
        client_authorization.channel.close()
        return what_authorized

    elif command == "what_authorized_external_id":
        """shell
            python3 authorization.py what_authorized_external_id IDENTITY_NODE_EXTERNAL_ID
        """
        # what a given subject, identified by its external_id, is authorized to have specific actions on
        # replace actions and resources types according to your data
        client_authorization = AuthorizationClient()
        node_type = args.node_type  # e.g "Individual"
        external_id = args.external_id
        actions = ["SUBSCRIBES_TO"]
        resource_types = [WhatAuthorizedResourceTypes("Asset", actions),
                          WhatAuthorizedResourceTypes("TypeNameSecond", actions)]
        input_params = {}
        policy_tags = []
        what_authorized = client_authorization.what_authorized_external_id(
            node_type,
            external_id,
            resource_types,
            input_params,
            policy_tags)
        if what_authorized:
            api_helper.print_response(what_authorized)
        else:
            print("Invalid what_authorized")
        client_authorization.channel.close()
        return what_authorized

    elif command == "who_authorized":
        """shell
            python3 authorization.py who_authorized
        """
        # who is authorized to have specific actions on specific resources
        # replace actions and resources according to your data
        client_authorization = AuthorizationClient()
        actions = ["HAS_FREE_PARKING"]
        resources = [WhoAuthorizedResource("parking-lot-id1", "ParkingLot", actions)]
        input_params = {}
        policy_tags = []
        who_authorized = client_authorization.who_authorized(
            resources,
            input_params,
            policy_tags)

        if who_authorized:
            api_helper.print_response(who_authorized)
        else:
            print("Invalid who_authorized")
        client_authorization.channel.close()
        return who_authorized


if __name__ == '__main__':  # pragma: no cover
    main()
