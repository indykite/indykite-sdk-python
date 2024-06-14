"""
Commandline interface for making an API request with the SDK.
"""
import argparse
import json
import time
from datetime import datetime
import logging
from indykite_sdk.config import ConfigClient
from indykite_sdk import api_helper


class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):  # pragma: no cover
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value


def main():
    """
    to call one command in the usage directory, check the command and the corresponding arguments in the list then execute:
    python3 configuration_spaces.py COMMAND arg1 arg2 ...
    """

    """ list of commands and arguments definitions """

    # Create parent parser
    parser = argparse.ArgumentParser(description="Identity client API.")
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    # customer_id
    customer_id_parser = subparsers.add_parser("customer_id")
    # customer_parser.add_argument("access_token", help="JWT bearer token")

    # customer_name
    customer_name_parser = subparsers.add_parser("customer_name")
    customer_name_parser.add_argument("customer_name", help="Customer name (not display name)")

    # customer_name_token
    customer_name_token_parser = subparsers.add_parser("customer_name_token")
    customer_name_token_parser.add_argument("customer_name", help="Customer name (not display name)")

    # service_account
    service_account_parser = subparsers.add_parser("service_account")

    # app_space_id
    app_space_id_parser = subparsers.add_parser("app_space_id")
    app_space_id_parser.add_argument("app_space_id", help="App Space id (gid)")

    # app_space_name
    app_space_name_parser = subparsers.add_parser("app_space_name")
    app_space_name_parser.add_argument("app_space_name", help="App Space name (not display name)")
    app_space_name_parser.add_argument("customer_id", help="Customer Id (gid)")

    # create_app_space
    create_app_space_parser = subparsers.add_parser("create_app_space")
    create_app_space_parser.add_argument("customer_id", help="Customer Id (gid)")
    create_app_space_parser.add_argument("app_space_name", help="App Space name (not display name)")
    create_app_space_parser.add_argument("display_name", help="Display Name")

    # update_app_space
    update_app_space_parser = subparsers.add_parser("update_app_space")
    update_app_space_parser.add_argument("app_space_id", help="AppSpace Id (gid)")
    update_app_space_parser.add_argument("etag", help="Etag")
    update_app_space_parser.add_argument("display_name", help="Display Name")

    # list_app_spaces
    list_app_spaces_parser = subparsers.add_parser("list_app_spaces")
    list_app_spaces_parser.add_argument("customer_id", help="Customer Id (gid)")
    list_app_spaces_parser.add_argument("match_list", help="Matching names separated by ,",
                                        type=lambda s: [str(item) for item in s.split(',')])
    list_app_spaces_parser.add_argument("bookmark", nargs='*', help="Optional list of bookmarks separated by space")

    # delete_app_space
    delete_app_space_parser = subparsers.add_parser("delete_app_space")
    delete_app_space_parser.add_argument("app_space_id", help="AppSpace Id (gid)")
    delete_app_space_parser.add_argument("etag", nargs='?', help="Optional Etag")

    # application_id
    application_id_parser = subparsers.add_parser("application_id")
    application_id_parser.add_argument("application_id", help="Application id (gid)")

    # application_name
    application_name_parser = subparsers.add_parser("application_name")
    application_name_parser.add_argument("application_name", help="Application name (not display name)")
    application_name_parser.add_argument("app_space_id", help="AppSpace Id (gid)")

    # create_application
    create_application_parser = subparsers.add_parser("create_application")
    create_application_parser.add_argument("app_space_id", help="AppSpace Id (gid)")
    create_application_parser.add_argument("application_name", help="Application name (not display name)")
    create_application_parser.add_argument("display_name", help="Display Name")

    # update_application
    update_application_parser = subparsers.add_parser("update_application")
    update_application_parser.add_argument("application_id", help="Application Id")
    update_application_parser.add_argument("etag", help="Etag")
    update_application_parser.add_argument("display_name", help="Display Name")

    # list_applications
    list_applications_parser = subparsers.add_parser("list_applications")
    list_applications_parser.add_argument("app_space_id", help="AppSpace Id (gid)")
    list_applications_parser.add_argument("match_list", help="Matching names separated by ,",
                                          type=lambda s: [str(item) for item in s.split(',')])
    list_applications_parser.add_argument("bookmark", nargs='*', help="Optional list of bookmarks separated by space")

    # delete_application
    delete_application_parser = subparsers.add_parser("delete_application")
    delete_application_parser.add_argument("application_id", help="Application Id")
    delete_application_parser.add_argument("etag", nargs='?', help="Optional Etag")

    # application_agent_id
    application_agent_id_parser = subparsers.add_parser("application_agent_id")
    application_agent_id_parser.add_argument("application_agent_id", help="Application agent id (gid)")

    # application_agent_name
    application_agent_name_parser = subparsers.add_parser("application_agent_name")
    application_agent_name_parser.add_argument("application_agent_name",
                                               help="Application agent name (not display name)")
    application_agent_name_parser.add_argument("app_space_id", help="AppSpace Id (gid)")

    # create_application_agent
    create_application_agent_parser = subparsers.add_parser("create_application_agent")
    create_application_agent_parser.add_argument("application_id", help="Application Id (gid)")
    create_application_agent_parser.add_argument("application_agent_name",
                                                 help="Application agent name (not display name)")
    create_application_agent_parser.add_argument("display_name", help="Display Name")

    # update_application_agent
    update_application_agent_parser = subparsers.add_parser("update_application_agent")
    update_application_agent_parser.add_argument("application_agent_id", help="Application Agent Id")
    update_application_agent_parser.add_argument("etag", help="Etag")
    update_application_agent_parser.add_argument("display_name", help="Display Name")

    # list_application_agents
    list_application_agents_parser = subparsers.add_parser("list_application_agents")
    list_application_agents_parser.add_argument("app_space_id", help="AppSpace Id (gid)")
    list_application_agents_parser.add_argument("match_list", help="Matching names separated by ,",
                                                type=lambda s: [str(item) for item in s.split(',')])
    list_application_agents_parser.add_argument("bookmark", nargs='*',
                                                help="Optional list of bookmarks separated by space")

    # delete_application_agent
    delete_application_agent_parser = subparsers.add_parser("delete_application_agent")
    delete_application_agent_parser.add_argument("application_agent_id", help="Application Agent Id")
    delete_application_agent_parser.add_argument("etag", nargs='?', help="Optional Etag")

    # application_agent_credential
    application_agent_credential_parser = subparsers.add_parser("application_agent_credential")
    application_agent_credential_parser.add_argument("application_agent_credential_id",
                                                     help="Application agent credential id")

    # register_application_agent_credential_jwk
    register_application_agent_credential_jwk_parser = subparsers.add_parser(
        "register_application_agent_credential_jwk")
    register_application_agent_credential_jwk_parser.add_argument("application_agent_id",
                                                                  help="Application agent credential id")
    register_application_agent_credential_jwk_parser.add_argument("display_name", help="Display name")

    # register_application_agent_credential_pem
    register_application_agent_credential_pem_parser = subparsers.add_parser(
        "register_application_agent_credential_pem")
    register_application_agent_credential_pem_parser.add_argument("application_agent_id",
                                                                  help="Application agent credential id")
    register_application_agent_credential_pem_parser.add_argument("display_name", help="Display name")

    # delete_application_agent_credential
    delete_application_agent_credential_parser = subparsers.add_parser("delete_application_agent_credential")
    delete_application_agent_credential_parser.add_argument("application_agent_credential_id",
                                                            help="Application agent credential id")
    delete_application_agent_credential_parser.add_argument("etag", help="Etag")

    # create_application_with_agent_credentials
    create_application_with_agent_credentials_parser = subparsers.add_parser(
        "create_application_with_agent_credentials")
    create_application_with_agent_credentials_parser.add_argument("app_space_id", help="AppSpace Id (gid)")
    create_application_with_agent_credentials_parser.add_argument("application_name", help="Application name")
    create_application_with_agent_credentials_parser.add_argument("application_agent_name",
                                                                  help="Application Agent Name")
    create_application_with_agent_credentials_parser.add_argument("application_agent_credentials_name",
                                                                  help="Application Agent Credentials Name")
    create_application_with_agent_credentials_parser.add_argument("public_key_type", help="Key type: jwk or pem")

    # service_account_id
    service_account_id_parser = subparsers.add_parser("service_account_id")
    service_account_id_parser.add_argument("service_account_id", help="Service account id (gid)")

    # service_account_name
    service_account_name_parser = subparsers.add_parser("service_account_name")
    service_account_name_parser.add_argument("customer_id", help="Customer Id (gid)")
    service_account_name_parser.add_argument("service_account_name", help="Service account name (not display name)")

    # create_service_account
    create_service_account_parser = subparsers.add_parser("create_service_account")
    create_service_account_parser.add_argument("customer_id", help="Customer id (gid)")
    create_service_account_parser.add_argument("service_account_name", help="Service account name (not display name)")
    create_service_account_parser.add_argument("display_name", help="Display Name")
    create_service_account_parser.add_argument("role", choices=["all_editor", "all_viewer", "app_editor", "app_viewer",
                                                                "authn_viewer", "authn_editor"],
                                               help="Roles: all_editor all_viewer app_editor app_viewer authn_viewer authn_editor")

    # update_service_account
    update_service_account_parser = subparsers.add_parser("update_service_account")
    update_service_account_parser.add_argument("service_account_id", help="Service account Id")
    update_service_account_parser.add_argument("etag", help="Etag")
    update_service_account_parser.add_argument("display_name", help="Display Name")

    # delete_service_account
    delete_service_account_parser = subparsers.add_parser("delete_service_account")
    delete_service_account_parser.add_argument("service_account_id", help="Service account Id")
    delete_service_account_parser.add_argument("etag", nargs='?', help="Optional Etag")

    # register_service_account_credential_jwk
    register_service_account_credential_jwk_parser = subparsers.add_parser(
        "register_service_account_credential_jwk")
    register_service_account_credential_jwk_parser.add_argument("service_account_id",
                                                                help="Service account credential id")
    register_service_account_credential_jwk_parser.add_argument("display_name", help="Display name")

    # register_service_account_credential_pem
    register_service_account_credential_pem_parser = subparsers.add_parser(
        "register_service_account_credential_pem")
    register_service_account_credential_pem_parser.add_argument("service_account_id",
                                                                help="Service account credential id")
    register_service_account_credential_pem_parser.add_argument("display_name", help="Display name")

    # read_service_account_credential
    read_service_account_credential_parser = subparsers.add_parser("read_service_account_credential")
    read_service_account_credential_parser.add_argument("service_account_credential_id",
                                                        help="Service account credentials id (gid)")

    # delete_service_account_credential
    delete_service_account_credential_parser = subparsers.add_parser("delete_service_account_credential")
    delete_service_account_credential_parser.add_argument("service_account_credential_id",
                                                          help="Service account credential id")
    delete_service_account_credential_parser.add_argument("etag", nargs='?', help="Optional Etag")

    args = parser.parse_args()
    command = args.command

    if command == "customer_id":
        """shell
           python3 configuration_spaces.py customer_id
        """
        # read_customer_by_id method: to get customer info from customer gid id
        # (extracted here from service account credentials)
        client_config = ConfigClient()
        try:
            service_account = client_config.read_service_account()
        except Exception as exception:
            print(exception)
            return None

        print(service_account.customer_id)
        customer = client_config.read_customer_by_id(service_account.customer_id)
        if customer:
            api_helper.print_response(customer)
        else:
            print("Invalid customer id")
        client_config.channel.close()

    elif command == "customer_name":
        """shell
           python3 configuration_spaces.py customer_name CUSTOMER_NAME
        """
        # read_customer_by_name method: to get customer info from customer name
        client_config = ConfigClient()
        customer_name = args.customer_name
        customer = client_config.read_customer_by_name(customer_name)
        client_config.channel.close()
        if customer:
            api_helper.print_response(customer)
        else:
            print("Invalid customer id")

    elif command == "customer_name_token":
        client_config = ConfigClient()
        # add "tokenLifetime": "2m" into service_account credentials json file to test token expiry
        print(client_config.token_source.token.access_token)
        # read_customer_by_name method: to get customer info from customer name
        customer_name = args.customer_name
        customer = client_config.read_customer_by_name(customer_name)
        if customer:
            api_helper.print_response(customer)
        else:
            print("Invalid customer id")
        time.sleep(180)
        client_config2 = ConfigClient(client_config.token_source)
        print(client_config2.token_source.token.access_token)
        # read_customer_by_name method: to get customer info from customer name
        customer_name = args.customer_name
        customer = client_config2.read_customer_by_name(customer_name)
        if customer:
            api_helper.print_response(customer)
        else:
            print("Invalid customer id")
        client_config.channel.close()

    elif command == "service_account":
        # service_account method: to get service account info from service account gid id
        # (extracted here from service account credentials)
        client_config = ConfigClient()
        service_account = client_config.read_service_account()
        if service_account:
            api_helper.print_response(service_account)
        else:
            print("Invalid service account")
        client_config.channel.close()

    elif command == "app_space_id":
        # app_space_id method: to get AppSpace info from AppSpace gid id
        client_config = ConfigClient()
        app_space_id = args.app_space_id
        app_space = client_config.read_app_space_by_id(app_space_id)
        if app_space:
            api_helper.print_response(app_space)
        else:
            print("Invalid app_space id")
        client_config.channel.close()

    elif command == "app_space_name":
        """shell
           python3 configuration_spaces.py app_space_name  APP_SPACE_NAME CUSTOMER_ID
        """
        # app_space_name method: to get AppSpace info from AppSpace name and customer gid id
        client_config = ConfigClient()
        app_space_name = args.app_space_name
        customer_id = args.customer_id
        app_space = client_config.read_app_space_by_name(customer_id, app_space_name)
        if app_space:
            api_helper.print_response(app_space)
        else:
            print("Invalid app_space name")
        client_config.channel.close()

    elif command == "create_app_space":
        """shell
           python3 configuration_spaces.py create_app_space  CUSTOMER_ID APP_SPACE_NAME APP_SPACE_DISPLAY_NAME
        """
        # create_app_space method: to create AppSpace with AppSpace name and customer gid id
        client_config = ConfigClient()
        app_space_name = args.app_space_name
        customer_id = args.customer_id
        display_name = args.display_name
        bookmark = []  # or value returned by last write operation
        app_space_response = client_config.create_app_space(customer_id, app_space_name, display_name, "description",
                                                            bookmark)
        if app_space_response:
            api_helper.print_response(app_space_response)
        else:
            print("Invalid app_space response")
        client_config.channel.close()
        return app_space_response

    elif command == "update_app_space":
        """shell
            python3 configuration_spaces.py update_app_space APP_SPACE_NAME ETAG APP_SPACE_DISPLAY_NAME
        """
        # update_app_space method: to update AppSpace info from new AppSpace info
        client_config = ConfigClient()
        app_space_id = args.app_space_id
        etag = args.etag
        display_name = args.display_name
        bookmark = []  # or value returned by last write operation
        app_space_response = client_config.update_app_space(app_space_id, etag, display_name, "description update",
                                                            bookmark)
        if app_space_response:
            api_helper.print_response(app_space_response)
        else:
            print("Invalid app_space response")
        client_config.channel.close()
        return app_space_response

    elif command == "list_app_spaces":
        # list_app_spaces method: to get AppSpace info from AppSpace name and customer gid id
        client_config = ConfigClient()
        customer_id = args.customer_id
        match_list = args.match_list
        if args.bookmark:
            bookmark = args.bookmark
        else:
            bookmark = []
        list_app_spaces_response = client_config.list_app_spaces(customer_id, match_list, bookmark)
        if list_app_spaces_response:
            for app_space in list_app_spaces_response:
                api_helper.print_response(app_space)
        else:
            print("Invalid list_app_spaces response")
        client_config.channel.close()
        return list_app_spaces_response

    elif command == "delete_app_space":
        # delete_app_space method: to delete AppSpace info from AppSpace id and etag
        # will delete everything below the AppSpace
        client_config = ConfigClient()
        app_space_id = args.app_space_id
        if args.etag:
            etag = args.etag
        else:
            etag = None
        bookmark = []  # or value returned by last write operation
        delete_app_space_response = client_config.delete_app_space(app_space_id, etag, bookmark)
        if delete_app_space_response:
            print(delete_app_space_response)
        else:
            print("Invalid delete_app_space_response response")
        client_config.channel.close()
        return delete_app_space_response

    elif command == "application_id":
        # application_id method: to get application info from application gid id
        client_config = ConfigClient()
        application_id = args.application_id
        application = client_config.read_application_by_id(application_id)
        if application:
            api_helper.print_response(application)
        else:
            print("Invalid application id")
        client_config.channel.close()

    elif command == "application_name":
        # application_name method: to get application info from application name and appSpace gid id
        client_config = ConfigClient()
        application_name = args.application_name
        app_space_id = args.app_space_id
        application = client_config.read_application_by_name(app_space_id, application_name)
        if application:
            api_helper.print_response(application)
        else:
            print("Invalid application name")
        client_config.channel.close()

    elif command == "create_application":
        # create_application method: to create application from given info
        client_config = ConfigClient()
        app_space_id = args.app_space_id
        application_name = args.application_name
        display_name = args.display_name
        bookmark = []  # or value returned by last write operation
        application_response = client_config.create_application(
            app_space_id,
            application_name,
            display_name,
            "description",
            bookmark)
        if application_response:
            api_helper.print_response(application_response)
        else:
            print("Invalid application response")
        client_config.channel.close()
        return application_response

    elif command == "update_application":
        # update_application method: to update application from given info
        client_config = ConfigClient()
        application_id = args.application_id
        etag = args.etag
        display_name = args.display_name
        bookmark = []  # or value returned by last write operation
        application_response = client_config.update_application(
            application_id,
            etag,
            display_name,
            "description update",
            bookmark)
        if application_response:
            api_helper.print_response(application_response)
        else:
            print("Invalid application response")
        client_config.channel.close()
        return application_response

    elif command == "list_applications":
        # list_applications method: to list all applications
        client_config = ConfigClient()
        app_space_id = args.app_space_id
        match_list = args.match_list
        if args.bookmark:
            bookmark = args.bookmark
        else:
            bookmark = []
        list_applications_response = client_config.list_applications(app_space_id, match_list, bookmark)
        if list_applications_response:
            print(list_applications_response)
        else:
            print("Invalid list_applications response")
        client_config.channel.close()
        return list_applications_response

    elif command == "delete_application":
        # delete_application method: to delete application from gid id and etag
        client_config = ConfigClient()
        application_id = args.application_id
        if args.etag:
            etag = args.etag
        else:
            etag = None
        bookmark = []  # or value returned by last write operation
        delete_application_response = client_config.delete_application(application_id, etag, bookmark)
        if delete_application_response:
            print(delete_application_response)
        else:
            print("Invalid delete_application_response response")
        client_config.channel.close()
        return delete_application_response

    elif command == "application_agent_id":
        # application_agent_id method: to get application agent info from application agent gid id
        client_config = ConfigClient()
        application_agent_id = args.application_agent_id
        application_agent = client_config.read_application_agent_by_id(application_agent_id)
        if application_agent:
            api_helper.print_response(application_agent)
        else:
            print("Invalid application agent id")
        client_config.channel.close()

    elif command == "application_agent_name":
        # application_agent_name method: to get application agent info from
        # application agent name and application gid id
        client_config = ConfigClient()
        application_agent_name = args.application_agent_name
        app_space_id = args.app_space_id
        application_agent = client_config.read_application_agent_by_name(app_space_id, application_agent_name)
        if application_agent:
            api_helper.print_response(application_agent)
        else:
            print("Invalid application agent name")
        client_config.channel.close()

    elif command == "create_application_agent":
        # create_application_agent method: to create application agent from given info
        client_config = ConfigClient()
        application_id = args.application_id
        application_agent_name = args.application_agent_name
        display_name = args.display_name
        api_permissions = ["indykite/*"]
        application_agent_response = client_config.create_application_agent(
            application_id=application_id,
            name=application_agent_name,
            display_name=display_name,
            description="description",
            bookmarks=[],
            api_permissions=api_permissions,
            )
        if application_agent_response:
            api_helper.print_response(application_agent_response)
        else:
            print("Invalid application agent response")
        client_config.channel.close()
        return application_agent_response

    elif command == "update_application_agent":
        # update_application_agent method: to update application agent from given info
        client_config = ConfigClient()
        application_agent_id = args.application_agent_id
        etag = args.etag
        display_name = args.display_name
        bookmark = []  # or value returned by last write operation
        application_agent_response = client_config.update_application_agent(
            application_agent_id,
            etag,
            display_name,
            "description update",
            bookmark)
        if application_agent_response:
            api_helper.print_response(application_agent_response)
        else:
            print("Invalid application agent response")
        client_config.channel.close()
        return application_agent_response

    elif command == "list_application_agents":
        # list_applications_agents method: to list all application agents
        client_config = ConfigClient()
        app_space_id = args.app_space_id
        match_list = args.match_list
        if args.bookmark:
            bookmark = args.bookmark
        else:
            bookmark = []
        list_application_agents_response = client_config.list_application_agents(app_space_id, match_list, bookmark)
        if list_application_agents_response:
            print(list_application_agents_response)
        else:
            print("Invalid list_application_agents response")
        client_config.channel.close()
        return list_application_agents_response

    elif command == "delete_application_agent":
        # delete_application_agent method: to delete application agent from gid id and etag
        client_config = ConfigClient()
        application_agent_id = args.application_agent_id
        if args.etag:
            etag = args.etag
        else:
            etag = None
        bookmark = []  # or value returned by last write operation
        delete_application_agent_response = client_config.delete_application_agent(
            application_agent_id,
            etag,
            bookmark)
        if delete_application_agent_response:
            print(delete_application_agent_response)
        else:
            print("Invalid delete_application_response_agent response")
        client_config.channel.close()
        return delete_application_agent_response

    elif command == "application_agent_credential":
        # application_agent_credential method: to get application agent credentials info from
        # application agent credentials gid id
        client_config = ConfigClient()
        application_agent_credential_id = args.application_agent_credential_id
        application_agent_credential = client_config.read_application_agent_credential(application_agent_credential_id)
        if application_agent_credential:
            api_helper.print_response(application_agent_credential)
        else:
            print("Invalid application agent id")
        client_config.channel.close()

    elif command == "register_application_agent_credential_jwk":
        # register_application_agent_credential_jwk method: to register jwk application agent credentials
        client_config = ConfigClient()
        application_agent_id = args.application_agent_id
        display_name = args.display_name
        jwk = None  # or replace by your JWK public key
        t = datetime.now().timestamp()
        expire_time_in_seconds = int(t) + 31536000  # now + one year example
        bookmark = []  # or value returned by last write operation
        application_agent_credential_response = client_config.register_application_agent_credential_jwk(
            application_agent_id,
            display_name,
            jwk,
            expire_time_in_seconds,
            bookmark
        )
        if application_agent_credential_response:
            api_helper.print_credential(application_agent_credential_response)
        else:
            print("Invalid application agent response")
        client_config.channel.close()
        return application_agent_credential_response

    elif command == "register_application_agent_credential_pem":
        # register_application_agent_credential_pem method: to register pem application agent credentials
        client_config = ConfigClient()
        application_agent_id = args.application_agent_id
        display_name = args.display_name
        pem = None  # or replace by your pem public certificate
        t = datetime.now().timestamp()
        expire_time_in_seconds = int(t) + 2678400  # now + one month example
        bookmark = []  # or value returned by last write operation
        application_agent_credential_response = client_config.register_application_agent_credential_pem(
            application_agent_id,
            display_name,
            pem,
            expire_time_in_seconds,
            bookmark
        )
        if application_agent_credential_response:
            api_helper.print_credential(application_agent_credential_response)
        else:
            print("Invalid application agent response")
        client_config.channel.close()
        return application_agent_credential_response

    elif command == "delete_application_agent_credential":
        # delete_application_agent_credential method: to delete application agent credentials info from gid id and etag
        client_config = ConfigClient()
        application_agent_credential_id = args.application_agent_credential_id
        etag = args.etag
        bookmark = []  # or value returned by last write operation
        delete_application_agent_credential_response = client_config.delete_application_agent_credential(
            application_agent_credential_id,
            bookmark,
            etag
        )
        if delete_application_agent_credential_response:
            print(delete_application_agent_credential_response)
        else:
            print("Invalid delete_application_agent_credential_response response")
        client_config.channel.close()
        return delete_application_agent_credential_response

    elif command == "create_application_with_agent_credentials":
        # create_application_with_agent_credentials method: to create
        # application, application agent and appAgent credentials
        client_config = ConfigClient()
        # example public key (random)
        public_key = {
            "kty": "EC",
            "use": "sig",
            "crv": "P-256",
            "x": "INNm_kk3mHAJE5gs_quJUsE5meEFX7oOsWZQtm0NrYI",
            "y": "yzpgNRuGDAHbnqayGCcA60UxGkuqCYfm2JWglHlGSC4",
            "alg": "ES256"
        }
        public_key_encoded = json.dumps(public_key, indent=2).encode('utf-8')
        create_application_with_agent_credentials_response = client_config.create_application_with_agent_credentials(
            args.app_space_id,
            args.application_name,
            args.application_agent_name,
            args.application_agent_credentials_name,
            args.public_key_type,
            public_key=public_key_encoded,
            expire_time=None)
        if create_application_with_agent_credentials_response:
            api_helper.print_response(create_application_with_agent_credentials_response["response_application"])
            api_helper.print_response(create_application_with_agent_credentials_response["response_application_agent"])
            api_helper.print_credential(
                create_application_with_agent_credentials_response["response_application_agent_credentials"])
        else:
            print("Invalid create_application_with_agent_credentials_response")
        client_config.channel.close()
        return create_application_with_agent_credentials_response

    elif command == "service_account_id":
        # service_account_id method: read service account info from gid id
        client_config = ConfigClient()
        service_account_id = args.service_account_id
        bookmark = []  # or value returned by last write operation
        service_account = client_config.read_service_account(service_account_id, bookmark)
        if service_account:
            api_helper.print_response(service_account)
        else:
            print("Invalid service account")
        client_config.channel.close()

    elif command == "service_account_name":
        # service_account_name method: read service account info from name and customer gid id
        client_config = ConfigClient()
        customer_id = args.customer_id
        service_account_name = args.service_account_name
        bookmark = []  # or value returned by last write operation
        service_account = client_config.read_service_account_by_name(customer_id, service_account_name, bookmark)
        if service_account:
            api_helper.print_response(service_account)
        else:
            print("Invalid service_account name")
        client_config.channel.close()

    elif command == "create_service_account":
        # create_service_account: create a service account from a customer gid id (not allowed in BE)
        client_config = ConfigClient()
        customer_id = args.customer_id
        service_account_name = args.service_account_name
        display_name = args.display_name
        role = args.role
        bookmark = []  # or value returned by last write operation
        service_account_response = client_config.create_service_account(
            customer_id,
            service_account_name,
            display_name,
            "description",
            role,
            bookmark
        )
        if service_account_response:
            api_helper.print_response(service_account_response)
        else:
            print("Invalid service_account response")
        client_config.channel.close()
        return service_account_response

    elif command == "update_service_account":
        # update_service_account method: to update existing service account
        client_config = ConfigClient()
        service_account_id = args.service_account_id
        etag = args.etag
        display_name = args.display_name
        bookmark = []  # or value returned by last write operation
        service_account_response = client_config.update_service_account(
            service_account_id,
            etag,
            display_name,
            "description",
            bookmark
        )
        if service_account_response:
            api_helper.print_response(service_account_response)
        else:
            print("Invalid service_account response")
        client_config.channel.close()
        return service_account_response

    elif command == "delete_service_account":
        # delete_service_account method: will also delete the credentials
        client_config = ConfigClient()
        service_account_id = args.service_account_id
        if args.etag:
            etag = args.etag
        else:
            etag = None
        bookmark = []  # or value returned by last write operation
        delete_service_account_response = client_config.delete_service_account(service_account_id, etag, bookmark)
        if delete_service_account_response:
            print(delete_service_account_response)
        else:
            print("Invalid delete_service_account response")
        client_config.channel.close()
        return delete_service_account_response

    elif command == "read_service_account_credential":
        client_config = ConfigClient()
        service_account_credential_id = args.service_account_credential_id
        service_account_credential = client_config.read_service_account_credential(service_account_credential_id)
        if service_account_credential:
            api_helper.print_response(service_account_credential)
        else:
            print("Invalid service account id")
        client_config.channel.close()

    elif command == "register_service_account_credential_jwk":
        client_config = ConfigClient()
        service_account_id = args.service_account_id
        display_name = args.display_name
        jwk = None  # or replace by your JWK public key
        t = datetime.now().timestamp()
        expire_time_in_seconds = int(t) + 2678400  # now + one month example
        bookmark = []  # or value returned by last write operation
        service_account_credential_response = client_config.register_service_account_credential_jwk(
            service_account_id,
            display_name,
            jwk,
            expire_time_in_seconds,
            bookmark
        )
        if service_account_credential_response:
            api_helper.print_credential(service_account_credential_response)
        else:
            print("Invalid service account response")
        client_config.channel.close()
        return service_account_credential_response

    elif command == "register_service_account_credential_pem":
        client_config = ConfigClient()
        service_account_id = args.service_account_id
        display_name = args.display_name
        pem = None  # or replace by your pem public certificate
        t = datetime.now().timestamp()
        expire_time_in_seconds = int(t) + 2678400  # now + one month example
        bookmark = []  # or value returned by last write operation
        service_account_credential_response = client_config.register_service_account_credential_pem(
            service_account_id,
            display_name,
            pem,
            expire_time_in_seconds,
            bookmark
        )
        if service_account_credential_response:
            api_helper.print_credential(service_account_credential_response)
        else:
            print("Invalid service account response")
        client_config.channel.close()
        return service_account_credential_response

    elif command == "delete_service_account_credential":
        client_config = ConfigClient()
        service_account_credential_id = args.service_account_credential_id
        if args.etag:
            etag = args.etag
        else:
            etag = None
        bookmark = []  # or value returned by last write operation
        delete_service_account_credential_response = client_config.delete_service_account_credential(
            service_account_credential_id,
            etag,
            bookmark
        )
        if delete_service_account_credential_response:
            print(delete_service_account_credential_response)
        else:
            print("Invalid delete_service_account_credential_response response")
        client_config.channel.close()
        return delete_service_account_credential_response


if __name__ == '__main__':  # pragma: no cover
    main()
