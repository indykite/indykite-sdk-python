"""
Commandline interface for making an API request with the SDK.
"""
import argparse
import json
import os
from google.protobuf.duration_pb2 import Duration
from indykite_sdk.config import ConfigClient
from indykite_sdk.indykite.config.v1beta1.model_pb2 import (SendGridProviderConfig, MailJetProviderConfig,
                                                            AmazonSESProviderConfig, MailgunProviderConfig)
from indykite_sdk.indykite.config.v1beta1.model_pb2 import (EmailServiceConfig, AuthFlowConfig, OAuth2ClientConfig,
                                                            WebAuthnProviderConfig, AuthorizationPolicyConfig)
from indykite_sdk.indykite.config.v1beta1.model_pb2 import OAuth2ProviderConfig, OAuth2ApplicationConfig, \
    UniquePropertyConstraint, UsernamePolicy
from indykite_sdk.indykite.config.v1beta1.model_pb2 import EmailAttachment, Email, EmailMessage, EmailTemplate, \
    EmailDefinition
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from indykite_sdk import api_helper


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
    # create_email_service_config_node
    create_email_service_config_node_parser = subparsers.add_parser("create_email_service_config_node")
    create_email_service_config_node_parser.add_argument("customer_id", help="Customer id (gid)")
    create_email_service_config_node_parser.add_argument("name", help="Name (not display name)")
    create_email_service_config_node_parser.add_argument("display_name", help="Display name")
    create_email_service_config_node_parser.add_argument("description", help="Description")

    # read_config_node
    read_config_node_parser = subparsers.add_parser("read_config_node")
    read_config_node_parser.add_argument("config_node_id", help="Config node id (gid)")

    # update_email_service_config_node
    update_email_service_config_node_parser = subparsers.add_parser("update_email_service_config_node")
    update_email_service_config_node_parser.add_argument("config_node_id", help="Config node id (gid)")
    update_email_service_config_node_parser.add_argument("etag", help="Etag")
    update_email_service_config_node_parser.add_argument("display_name", help="Display name")
    update_email_service_config_node_parser.add_argument("description", help="Description")

    # delete_email_service_config_node
    delete_config_node_parser = subparsers.add_parser("delete_config_node")
    delete_config_node_parser.add_argument("config_node_id", help="Config node id (gid)")
    delete_config_node_parser.add_argument("etag", help="Etag")

    # list_config_node_versions
    list_config_node_versions_parser = subparsers.add_parser("list_config_node_versions")
    list_config_node_versions_parser.add_argument("config_node_id", help="Config node id (gid)")

    # create_auth_flow_config_node
    create_auth_flow_config_node_parser = subparsers.add_parser("create_auth_flow_config_node")
    create_auth_flow_config_node_parser.add_argument("app_space_id", help="AppSpace (gid)")
    create_auth_flow_config_node_parser.add_argument("name", help="Name (not display name)")
    create_auth_flow_config_node_parser.add_argument("display_name", help="Display name")
    create_auth_flow_config_node_parser.add_argument("description", help="Description")

    # update_auth_flow_config_node
    update_auth_flow_config_node_parser = subparsers.add_parser("update_auth_flow_config_node")
    update_auth_flow_config_node_parser.add_argument("config_node_id", help="Config node id (gid)")
    update_auth_flow_config_node_parser.add_argument("etag", help="Etag")
    update_auth_flow_config_node_parser.add_argument("display_name", help="Display name")
    update_auth_flow_config_node_parser.add_argument("description", help="Description")

    # create_oauth2_client_config_node
    create_oauth2_client_config_node_parser = subparsers.add_parser("create_oauth2_client_config_node")
    create_oauth2_client_config_node_parser.add_argument("app_space_id", help="AppSpace (gid)")
    create_oauth2_client_config_node_parser.add_argument("name", help="Name (not display name)")
    create_oauth2_client_config_node_parser.add_argument("display_name", help="Display name")
    create_oauth2_client_config_node_parser.add_argument("description", help="Description")

    # update_oauth2_client_config_node
    update_oauth2_client_config_node_parser = subparsers.add_parser("update_oauth2_client_config_node")
    update_oauth2_client_config_node_parser.add_argument("config_node_id", help="Config node id (gid)")
    update_oauth2_client_config_node_parser.add_argument("etag", help="Etag")
    update_oauth2_client_config_node_parser.add_argument("display_name", help="Display name")
    update_oauth2_client_config_node_parser.add_argument("description", help="Description")

    # create_webauthn_provider_config_node
    create_webauthn_provider_config_node_parser = subparsers.add_parser("create_webauthn_provider_config_node")
    create_webauthn_provider_config_node_parser.add_argument("app_space_id", help="AppSpace (gid)")
    create_webauthn_provider_config_node_parser.add_argument("name", help="Name (not display name)")
    create_webauthn_provider_config_node_parser.add_argument("display_name", help="Display name")
    create_webauthn_provider_config_node_parser.add_argument("description", help="Description")

    # update_webauthn_provider_config_node
    update_webauthn_provider_config_node_parser = subparsers.add_parser("update_webauthn_provider_config_node")
    update_webauthn_provider_config_node_parser.add_argument("config_node_id", help="Config node id (gid)")
    update_webauthn_provider_config_node_parser.add_argument("etag", help="Etag")
    update_webauthn_provider_config_node_parser.add_argument("display_name", help="Display name")
    update_webauthn_provider_config_node_parser.add_argument("description", help="Description")

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

    # read_oauth2_provider
    read_oauth2_provider_parser = subparsers.add_parser("read_oauth2_provider")
    read_oauth2_provider_parser.add_argument("oauth2_provider_id", help="Oauth2 provider id (gid)")

    # create_oauth2_provider
    create_oauth2_provider_parser = subparsers.add_parser("create_oauth2_provider")
    create_oauth2_provider_parser.add_argument("app_space_id", help="AppSpace (gid)")
    create_oauth2_provider_parser.add_argument("name", help="Name (not display name)")
    create_oauth2_provider_parser.add_argument("display_name", help="Display name")
    create_oauth2_provider_parser.add_argument("description", help="Description")

    # update_oauth2_provider
    update_oauth2_provider_parser = subparsers.add_parser("update_oauth2_provider")
    update_oauth2_provider_parser.add_argument("oauth2_provider_id", help="OAuth2 provider id (gid)")
    update_oauth2_provider_parser.add_argument("etag", help="Etag")
    update_oauth2_provider_parser.add_argument("display_name", help="Display name")
    update_oauth2_provider_parser.add_argument("description", help="Description")

    # delete_oauth2_provider
    delete_oauth2_provider_parser = subparsers.add_parser("delete_oauth2_provider")
    delete_oauth2_provider_parser.add_argument("oauth2_provider_id", help="OAuth2 provider id (gid)")
    delete_oauth2_provider_parser.add_argument("etag", help="Etag")

    # read_oauth2_application
    read_oauth2_application_parser = subparsers.add_parser("read_oauth2_application")
    read_oauth2_application_parser.add_argument("oauth2_application_id", help="Oauth2 application id (gid)")

    # create_oauth2_application
    create_oauth2_application_parser = subparsers.add_parser("create_oauth2_application")
    create_oauth2_application_parser.add_argument("oauth2_provider_id", help="OAuth2 provider (gid)")
    create_oauth2_application_parser.add_argument("name", help="Name (not display name)")
    create_oauth2_application_parser.add_argument("display_name", help="Display name")
    create_oauth2_application_parser.add_argument("description", help="Description")

    # update_oauth2_application
    update_oauth2_application_parser = subparsers.add_parser("update_oauth2_application")
    update_oauth2_application_parser.add_argument("oauth2_application_id", help="OAuth2 application id (gid)")
    update_oauth2_application_parser.add_argument("etag", help="Etag")
    update_oauth2_application_parser.add_argument("display_name", help="Display name")
    update_oauth2_application_parser.add_argument("description", help="Description")

    # delete_oauth2_application
    delete_oauth2_application_parser = subparsers.add_parser("delete_oauth2_application")
    delete_oauth2_application_parser.add_argument("oauth2_application_id", help="OAuth2 application id (gid)")
    delete_oauth2_application_parser.add_argument("etag", help="Etag")

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

    args = parser.parse_args()
    command = args.command

    if command == "create_email_service_config_node":
        # to create a sendgrid email service to send invitations to people to join the platform
        # replace the env variables by your own
        """shell
           python3 configuration_config_nodes.py create_email_service_config_node
           CUSTOMER_ID SERVICE_NAME SERVICE_DISPLAY_NAME SERVICE_DESCRIPTION
        """
        client_config = ConfigClient()
        location = args.customer_id
        name = args.name
        display_name = args.display_name
        description = args.description

        default_from_address_address = os.getenv('INDYKITE_DEFAULT_FROM')
        default_from_address_name = "Test Config"

        sendgrid = SendGridProviderConfig(
            api_key=os.getenv('SENDGRID_KEY'),
            sandbox_mode=True,
            ip_pool_name=wrappers.StringValue(value=os.getenv('SENDGRID_IP')),
            host=wrappers.StringValue(value="https://api.sendgrid.com")
        )

        message_from = Email(address=os.getenv('INDYKITE_DEFAULT_FROM'), name='Test From')
        message_to = [Email(address=os.getenv('INDYKITE_DEFAULT_TO'), name='Test To')]
        message_subject = "subject"
        message_text_content = "content text"
        message_html_content = "<html><body>content html</body></html>"

        email_service_config = EmailServiceConfig(
            default_from_address=Email(address=default_from_address_address, name=default_from_address_name),
            sendgrid=sendgrid,
            invitation_message=EmailDefinition(
                message=EmailMessage(
                    to=message_to,
                    cc=[],
                    bcc=[],
                    subject=message_subject,
                    text_content=message_text_content,
                    html_content=message_html_content
                )
            )
        )
        bookmark = []  # or value returned by last write operation
        create_email_service_config_node_response = client_config.create_email_service_config_node(
            location,
            name,
            display_name,
            description,
            email_service_config,
            bookmark
        )
        if create_email_service_config_node_response:
            api_helper.print_response(create_email_service_config_node_response)
        else:
            print("Invalid create email service config node response")
        client_config.channel.close()
        return create_email_service_config_node_response

    elif command == "read_config_node":
        # to get info for any given config node (AuthFlowConfig ,EmailServiceConfig, AuditSinkConfig,
        # OAuth2ClientConfig, WebAuthnProviderConfig, AuthorizationPolicyConfig)
        client_config = ConfigClient()
        config_node_id = args.config_node_id
        bookmark = []  # or value returned by last write operation
        version = 0
        config_node = client_config.read_config_node(config_node_id, bookmark, version)
        if config_node:
            api_helper.print_response(config_node)
        else:
            print("Invalid config node id")
        client_config.channel.close()

    elif command == "update_email_service_config_node":
        # to update sendgrid email service info
        client_config = ConfigClient()
        config_node_id = args.config_node_id
        etag = args.etag
        display_name = args.display_name
        description = args.description

        default_from_address_address = "test+config@indykite.com"
        default_from_address_name = "Test Config"

        sendgrid = SendGridProviderConfig(
            api_key=os.getenv('SENDGRID_KEY'),
            sandbox_mode=True,
            ip_pool_name=wrappers.StringValue(value=os.getenv('SENDGRID_IP')),
            host=wrappers.StringValue(value="https://api.sendgrid.com")
        )

        message_to = [Email(address='test+to@indykite.com', name='Test To')]
        message_subject = "subject2"
        message_text_content = "content text"
        message_html_content = "<html><body>content html</body></html>"
        bookmark = []  # or value returned by last write operation
        email_service_config = EmailServiceConfig(
            default_from_address=Email(
                address=default_from_address_address,
                name=default_from_address_name
            ),
            sendgrid=sendgrid,
            authentication_message=EmailDefinition(
                message=EmailMessage(
                    to=message_to,
                    cc=[],
                    bcc=[],
                    subject=message_subject,
                    text_content=message_text_content,
                    html_content=message_html_content
                )
            )
        )

        update_email_service_config_node_response = client_config.update_email_service_config_node(
            config_node_id,
            etag,
            display_name,
            description,
            email_service_config,
            bookmark
        )
        if update_email_service_config_node_response:
            api_helper.print_response(update_email_service_config_node_response)
        else:
            print("Invalid update email service config node response")
        client_config.channel.close()
        return update_email_service_config_node_response

    elif command == "delete_config_node":
        # to delete any given config node (AuthFlowConfig ,EmailServiceConfig, AuditSinkConfig,
        # OAuth2ClientConfig, WebAuthnProviderConfig, AuthorizationPolicyConfig)
        client_config = ConfigClient()
        config_node_id = args.config_node_id
        etag = args.etag
        config_node = client_config.delete_config_node(config_node_id, etag, [])
        if config_node:
            api_helper.print_response(config_node)
        else:
            print("Invalid delete config node response")

    elif command == "list_config_node_versions":
        #  list all versions of a given config node (AuthFlowConfig ,EmailServiceConfig, AuditSinkConfig,
        # OAuth2ClientConfig, WebAuthnProviderConfig, AuthorizationPolicyConfig)
        client_config = ConfigClient()
        config_node_id = args.config_node_id
        list_config_nodes = client_config.list_config_node_versions(config_node_id)
        if list_config_nodes:
            api_helper.print_response(list_config_nodes)
        else:
            print("Invalid list_config_nodes response")
        client_config.channel.close()
        return list_config_nodes

    elif command == "create_auth_flow_config_node":
        # to create an authentication flow config node  to authenticate
        client_config = ConfigClient()
        location = args.app_space_id
        name = args.name
        display_name = args.display_name
        description = args.description
        bookmark = []  # or value returned by last write operation
        with open("../utils/sdk_simple_flow.json") as f:
            file_data = f.read()
        user_dict = json.loads(file_data)
        user_dict = json.dumps(user_dict, indent=4, separators=(',', ': ')).encode('utf-8')

        # only bare JSON or YAML source_format is supported as input
        auth_flow_config = client_config.auth_flow_config(
            source_format="FORMAT_BARE_JSON",
            source=user_dict
        )

        create_auth_flow_config_node_response = client_config.create_auth_flow_config_node(
            location,
            name,
            display_name,
            description,
            auth_flow_config,
            bookmark
        )
        if create_auth_flow_config_node_response:
            api_helper.print_response(create_auth_flow_config_node_response)
        else:
            print("Invalid create auth flow config node response")
        client_config.channel.close()
        return create_auth_flow_config_node_response

    elif command == "update_auth_flow_config_node":
        # to update an authentication flow config node
        client_config = ConfigClient()
        config_node_id = args.config_node_id
        etag = args.etag
        display_name = args.display_name
        description = args.description
        bookmark = []  # or value returned by last write operation
        with open("utils/sdk_simple_flow.json") as f:
            file_data = f.read()
        user_dict = json.loads(file_data)
        user_dict = json.dumps(user_dict, indent=4, separators=(',', ': ')).encode('utf-8')

        # only bare JSON or YAML source_format is support as input
        auth_flow_config = client_config.auth_flow_config(
            source_format="FORMAT_BARE_JSON",
            source=user_dict
        )

        update_auth_flow_config_node_response = client_config.update_auth_flow_config_node(
            config_node_id,
            etag,
            display_name,
            description,
            auth_flow_config,
            bookmark
        )
        if update_auth_flow_config_node_response:
            api_helper.print_response(update_auth_flow_config_node_response)
        else:
            print("Invalid update auth flow config node response")
        client_config.channel.close()
        return update_auth_flow_config_node_response

    elif command == "create_oauth2_client_config_node":
        # to create an oauth2 client config node to authenticate
        # replace the env variables by your own
        """shell
           python3 configuration_config_nodes.py create_oauth2_client_config_node
           APP_SPACE_ID OAUTH_CLIENT_NAME OAUTH_CLIENT_DISPLAY_NAME OAUTH_CLIENT_DESCRIPTION
        """
        client_config = ConfigClient()
        location = args.app_space_id
        name = args.name
        display_name = args.display_name
        description = args.description
        bookmark = []  # or value returned by last write operation
        oauth2_client_config = OAuth2ClientConfig(
            provider_type="PROVIDER_TYPE_GOOGLE_COM",
            client_id=os.getenv('CLIENT_ID'),
            client_secret=os.getenv('CLIENT_SECRET'),
            default_scopes=["openid", "profile", "email"],
            allowed_scopes=["openid", "profile", "email"]
        )

        create_oauth2_client_config_node_response = client_config.create_oauth2_client_config_node(
            location,
            name,
            display_name,
            description,
            oauth2_client_config,
            bookmark
        )
        if create_oauth2_client_config_node_response:
            api_helper.print_response(create_oauth2_client_config_node_response)
        else:
            print("Invalid create oauth2 client config node response")
        client_config.channel.close()
        return create_oauth2_client_config_node_response

    elif command == "update_oauth2_client_config_node":
        # to update an oauth2 client config node
        client_config = ConfigClient()
        config_node_id = args.config_node_id
        etag = args.etag
        display_name = args.display_name
        description = args.description
        bookmark = []  # or value returned by last write operation
        oauth2_client_config = OAuth2ClientConfig(
            provider_type="PROVIDER_TYPE_GOOGLE_COM",
            client_id=os.getenv('CLIENT_ID'),
            client_secret=os.getenv('CLIENT_SECRET'),
            default_scopes=["openid", "profile", "email"],
            allowed_scopes=["openid", "profile", "email"]
        )

        update_oauth2_client_config_node_response = client_config.update_oauth2_client_config_node(
            config_node_id,
            etag,
            display_name,
            description,
            oauth2_client_config,
            bookmark
        )
        if update_oauth2_client_config_node_response:
            api_helper.print_response(update_oauth2_client_config_node_response)
        else:
            print("Invalid update oauth2 client config node response")
        client_config.channel.close()
        return update_oauth2_client_config_node_response

    elif command == "create_webauthn_provider_config_node":
        # to create a WebAuthN provider config node to authenticate
        client_config = ConfigClient()
        location = args.app_space_id
        name = args.name
        display_name = args.display_name
        description = args.description

        webauthn_provider_config = client_config.webauthn_provider_config(
            relying_parties={"http://localhost": "localhost"},  # e.g {"http://localhost": "localhost"}
            attestation_preference="CONVEYANCE_PREFERENCE_NONE",
            authenticator_attachment="AUTHENTICATOR_ATTACHMENT_DEFAULT",
            require_resident_key=False,
            user_verification="USER_VERIFICATION_REQUIREMENT_PREFERRED",
            registration_timeout=Duration(seconds=30),
            authentication_timeout=Duration(seconds=60)
        )

        create_webauthn_provider_config_node_response = client_config.create_webauthn_provider_config_node(
            location, name, display_name, description, webauthn_provider_config, [])
        if create_webauthn_provider_config_node_response:
            api_helper.print_response(create_webauthn_provider_config_node_response)
        else:
            print("Invalid create webauthn provider config node response")
        client_config.channel.close()
        return create_webauthn_provider_config_node_response

    elif command == "update_webauthn_provider_config_node":
        # to update a WebAuthN provider config node
        client_config = ConfigClient()
        config_node_id = args.config_node_id
        etag = args.etag
        display_name = args.display_name
        description = args.description
        bookmark = []  # or value returned by last write operation
        webauthn_provider_config = client_config.webauthn_provider_config(
            relying_parties=os.getenv('RELYING_PARTIES'),  # e.g {"http://localhost": "localhost"}
            attestation_preference="CONVEYANCE_PREFERENCE_INDIRECT",
            authenticator_attachment="AUTHENTICATOR_ATTACHMENT_DEFAULT",
            require_resident_key=False,
            user_verification="USER_VERIFICATION_REQUIREMENT_REQUIRED",
            registration_timeout=Duration(seconds=30),
            authentication_timeout=Duration(seconds=60)
        )

        update_webauthn_provider_config_node_response = client_config.update_webauthn_provider_config_node(
            config_node_id,
            etag,
            display_name,
            description,
            webauthn_provider_config,
            bookmark)

        if update_webauthn_provider_config_node_response:
            api_helper.print_response(update_webauthn_provider_config_node_response)
        else:
            print("Invalid update webauthn provider config node response")
        client_config.channel.close()
        return update_webauthn_provider_config_node_response

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
        bookmark = []  # or value returned by last write operation
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
            policy_config,
            bookmark
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
        bookmark = []  # or value returned by last write operation
        with open("utils/sdk_policy_config.json") as f:
            file_data = f.read()
        policy_dict = json.loads(file_data)
        policy_dict = json.dumps(policy_dict)
        policy_config = client_config.authorization_policy_config(
            policy=str(policy_dict),
            status="STATUS_ACTIVE",
            tags=[]
        )

        update_authorization_policy_config_node_response = client_config.update_authorization_policy_config_node(
            config_node_id,
            etag,
            display_name,
            description,
            policy_config,
            bookmark
        )
        if update_authorization_policy_config_node_response:
            api_helper.print_response(update_authorization_policy_config_node_response)
        else:
            print("Invalid update authorization policy config node response")
        client_config.channel.close()
        return update_authorization_policy_config_node_response

    elif command == "read_oauth2_provider":
        # to get info on an existing oauth2 provider
        client_config = ConfigClient()
        oauth2_provider_id = args.oauth2_provider_id
        bookmark = []  # or value returned by last write operation
        config = client_config.read_oauth2_provider(oauth2_provider_id, bookmark)
        if config:
            api_helper.print_response(config)
        else:
            print("Invalid oauth2 provider id")
        client_config.channel.close()

    elif command == "create_oauth2_provider":
        # create an oauth2 provider config node for authentication
        client_config = ConfigClient()
        app_space_id = args.app_space_id
        name = args.name
        display_name = args.display_name
        description = args.description
        bookmark = []  # or value returned by last write operation
        # local env example
        config = OAuth2ProviderConfig(
            grant_types=["GRANT_TYPE_AUTHORIZATION_CODE"],
            response_types=["RESPONSE_TYPE_CODE", "RESPONSE_TYPE_TOKEN"],
            scopes=["openid", "profile", "email"],
            token_endpoint_auth_method=["TOKEN_ENDPOINT_AUTH_METHOD_CLIENT_SECRET_BASIC",
                                        "TOKEN_ENDPOINT_AUTH_METHOD_CLIENT_SECRET_POST"],
            token_endpoint_auth_signing_alg=["ES256", "ES384", "ES512"],
            front_channel_login_uri={"default": "http://localhost:3000/login/oauth2"},
            front_channel_consent_uri={"default": "http://localhost:3000/consent"}
        )

        create_oauth2_provider_response = client_config.create_oauth2_provider(
            app_space_id,
            name,
            display_name,
            description,
            config,
            bookmark
        )
        if create_oauth2_provider_response:
            api_helper.print_response(create_oauth2_provider_response)
        else:
            print("Invalid create oauth2 provider response")
        client_config.channel.close()
        return create_oauth2_provider_response

    elif command == "update_oauth2_provider":
        # update an oauth2 provider config node for authentication
        client_config = ConfigClient()
        oauth2_provider_id = args.oauth2_provider_id
        etag = args.etag
        display_name = args.display_name
        description = args.description
        bookmark = []  # or value returned by last write operation
        # local env example
        config = OAuth2ProviderConfig(
            grant_types=["GRANT_TYPE_AUTHORIZATION_CODE"],
            response_types=["RESPONSE_TYPE_CODE", "RESPONSE_TYPE_TOKEN"],
            scopes=["openid", "profile", "email"],
            token_endpoint_auth_method=["TOKEN_ENDPOINT_AUTH_METHOD_CLIENT_SECRET_BASIC",
                                        "TOKEN_ENDPOINT_AUTH_METHOD_CLIENT_SECRET_POST"],
            token_endpoint_auth_signing_alg=["ES256", "ES384", "ES512"],
            front_channel_login_uri={"default": "http://localhost:3000/login/oauth2"},
            front_channel_consent_uri={"default": "http://localhost:3000/consent"}
        )

        update_oauth2_provider_response = client_config.update_oauth2_provider(
            oauth2_provider_id,
            etag,
            display_name,
            description,
            config,
            bookmark
        )
        if update_oauth2_provider_response:
            api_helper.print_response(update_oauth2_provider_response)
        else:
            print("Invalid update oauth2 provider response")
        client_config.channel.close()
        return update_oauth2_provider_response

    elif command == "delete_oauth2_provider":
        # delete an oauth2 provider config node for authentication
        client_config = ConfigClient()
        oauth2_provider_id = args.oauth2_provider_id
        etag = args.etag
        bookmark = []  # or value returned by last write operation
        config = client_config.delete_oauth2_provider(oauth2_provider_id, etag, bookmark)
        if config:
            api_helper.print_response(config)
        else:
            print("Invalid delete oauth2 provider response")
        client_config.channel.close()

    elif command == "read_oauth2_application":
        # read info on existing oauth2 application config node for authentication
        client_config = ConfigClient()
        oauth2_application_id = args.oauth2_application_id
        bookmark = []  # or value returned by last write operation
        config = client_config.read_oauth2_application(oauth2_application_id, bookmark)
        if config:
            api_helper.print_response(config)
        else:
            print("Invalid oauth2 application id")
        client_config.channel.close()

    elif command == "create_oauth2_application":
        # create an oauth2 application config node for authentication
        client_config = ConfigClient()
        oauth2_provider_id = args.oauth2_provider_id
        name = args.name
        display_name = args.display_name
        description = args.description
        bookmark = []  # or value returned by last write operation
        # local env example
        config = OAuth2ApplicationConfig(
            display_name="Oauth2 Application Config",
            redirect_uris=["http://localhost:3000/redirect"],
            owner="Owner",
            policy_uri="http://localhost:3000/policy",
            terms_of_service_uri="http://localhost:3000/policy",
            client_uri="http://localhost:3000/client",
            logo_uri="http://localhost:3000/logo",
            user_support_email_address="test@example.com",
            subject_type="CLIENT_SUBJECT_TYPE_PUBLIC",
            scopes=["openid", "profile", "email"],
            token_endpoint_auth_method="TOKEN_ENDPOINT_AUTH_METHOD_CLIENT_SECRET_BASIC",
            token_endpoint_auth_signing_alg="ES256",
            grant_types=["GRANT_TYPE_AUTHORIZATION_CODE"],
            response_types=["RESPONSE_TYPE_CODE", "RESPONSE_TYPE_TOKEN"]
        )

        create_oauth2_application_response = client_config.create_oauth2_application(
            oauth2_provider_id,
            name,
            display_name,
            description,
            config,
            bookmark
        )
        if create_oauth2_application_response:
            api_helper.print_response(create_oauth2_application_response)
        else:
            print("Invalid create oauth2 application response")
        client_config.channel.close()
        return create_oauth2_application_response

    elif command == "update_oauth2_application":
        # update an oauth2 application config node for authentication
        client_config = ConfigClient()
        oauth2_application_id = args.oauth2_application_id
        etag = args.etag
        display_name = args.display_name
        description = args.description
        bookmark = []  # or value returned by last write operation
        # local env example
        config = OAuth2ApplicationConfig(
            display_name="Oauth2 Application Config",
            redirect_uris=["http://localhost:3000/redirect"],
            owner="Owner",
            policy_uri="http://localhost:3000/policy",
            terms_of_service_uri="http://localhost:3000/policy",
            client_uri="http://localhost:3000/client",
            logo_uri="http://localhost:3000/logo",
            user_support_email_address="test@example.com",
            subject_type="CLIENT_SUBJECT_TYPE_PUBLIC",
            scopes=["openid", "profile", "email"],
            token_endpoint_auth_method="TOKEN_ENDPOINT_AUTH_METHOD_CLIENT_SECRET_BASIC",
            token_endpoint_auth_signing_alg="ES256",
            grant_types=["GRANT_TYPE_AUTHORIZATION_CODE"],
            response_types=["RESPONSE_TYPE_CODE", "RESPONSE_TYPE_TOKEN"]
        )

        update_oauth2_application_response = client_config.update_oauth2_application(
            oauth2_application_id,
            etag,
            display_name,
            description,
            config,
            bookmark
        )
        if update_oauth2_application_response:
            api_helper.print_response(update_oauth2_application_response)
        else:
            print("Invalid update oauth2 application response")
        client_config.channel.close()
        return update_oauth2_application_response

    elif command == "delete_oauth2_application":
        # delete an oauth2 application config node for authentication
        client_config = ConfigClient()
        oauth2_application_id = args.oauth2_application_id
        etag = args.etag
        bookmark = []  # or value returned by last write operation
        config = client_config.delete_oauth2_application(oauth2_application_id, etag, bookmark)
        if config:
            api_helper.print_response(config)
        else:
            print("Invalid delete oauth2 application response")
        client_config.channel.close()

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
        bookmark = []  # or value returned by last write operation
        # replace the json file by your own
        consent_config = ConfigClient().consent_config(
            purpose="Taking control",
            data_points={"last_name", "first_name", "email"},
            application_id=application_id,
            validity_period=86400,
            revoke_after_use=False
        )
        create_consent_config_node_response = client_config.create_consent_config_node(
            location,
            name,
            display_name,
            description,
            consent_config,
            bookmark
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
        bookmark = []  # or value returned by last write operation
        consent_config = ConfigClient().consent_config(
            purpose="Taking control",
            data_points={"lastname", "firstname", "email"},
            application_id=application_id,
            validity_period=86400,
            revoke_after_use=False
        )

        update_consent_config_node_response = client_config.update_consent_config_node(
            config_node_id,
            etag,
            display_name,
            description,
            consent_config,
            bookmark
        )
        if update_consent_config_node_response:
            api_helper.print_response(update_consent_config_node_response)
        else:
            print("Invalid update consent config node response")
        client_config.channel.close()
        return update_consent_config_node_response


if __name__ == '__main__':  # pragma: no cover
    main()
