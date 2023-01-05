"""
Commandline interface for making an API request with the SDK.
"""
import argparse
import base64
import json
from datetime import datetime
from uuid import UUID
from google.protobuf.json_format import MessageToJson

from indykite_sdk.identity import IdentityClient
from indykite_sdk.config import ConfigClient
from indykite_sdk.indykite.config.v1beta1.model_pb2 import (SendGridProviderConfig, MailJetProviderConfig, AmazonSESProviderConfig, MailgunProviderConfig)
from indykite_sdk.indykite.config.v1beta1.model_pb2 import (EmailServiceConfig, AuthFlowConfig, OAuth2ClientConfig, IngestMappingConfig)
from indykite_sdk.indykite.config.v1beta1.model_pb2 import OAuth2ProviderConfig, OAuth2ApplicationConfig
from indykite_sdk.indykite.identity.v1beta2.import_pb2 import ImportDigitalTwinsRequest, ImportDigitalTwin
from indykite_sdk.indykite.identity.v1beta2.import_pb2 import PasswordCredential, PasswordHash, Bcrypt
from indykite_sdk.indykite.config.v1beta1.model_pb2 import EmailAttachment, Email, EmailMessage, EmailTemplate, EmailDefinition
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from indykite_sdk.indykite.identity.v1beta2.import_pb2 import Email as EmailIdentity

class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):  # pragma: no cover
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value


def main():
    # Create parent parser
    parser = argparse.ArgumentParser(description="Identity client API.")
    parser.add_argument("-l", "--local", action="store_true", help="make the request to localhost")
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    # Create child parsers
    # INTROSPECT
    introspect_parser = subparsers.add_parser("introspect")
    introspect_parser.add_argument("user_token", help="JWT bearer token")

    # VERIFY
    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("verification_token", help="Token from email to verify")

    # CHANGE-PASSWORD (self-service)
    password_change = subparsers.add_parser("change-password")
    password_change.add_argument("user_token", help="JWT bearer token")
    password_change.add_argument("new_password", help="New password for the user in '' (single quotation mark)")

    # CHANGE-PASSWORD-OF-USER (admin activity)
    password_change_of_user = subparsers.add_parser("change-password-of-user")
    password_change_of_user.add_argument("digital_twin_id", help="gid ID of the digital twin for password change")
    password_change_of_user.add_argument("tenant_id", help="gid ID of the tenant")
    password_change_of_user.add_argument("new_password", help="New password for the user in '' (single quotation mark)")

    # GET-DT
    get_dt = subparsers.add_parser("get-dt")
    get_dt.add_argument("digital_twin_id", help="gid ID of the digital twin for password change")
    get_dt.add_argument("tenant_id", help="gid ID of the tenant")
    get_dt.add_argument("property_list", nargs="+", help="Array list of the required properties")

    # GET-DT-BY-TOKEN
    get_dt_by_token = subparsers.add_parser("get-dt-by-token")
    get_dt_by_token.add_argument("user_token", help="JWT bearer token")
    get_dt_by_token.add_argument("property_list", nargs="+", help="Array list of the required properties")

    # PATCH-PROPERTIES
    patch_properties = subparsers.add_parser("patch-properties")
    patch_properties.add_argument("digital_twin_id", help="gid ID of the digital twin for password change")
    patch_properties.add_argument("tenant_id", help="gid ID of the tenant")
    patch_properties.add_argument("--add", nargs="+", help="Name and value of the property to add (--add email x@x.x)")
    patch_properties.add_argument("--add_by_ref", nargs="+", help='''
Name and value of the property where the value is a reference
    ''')
    patch_properties.add_argument("--replace", nargs="+", help="Property ID and new value (--replace 111 a@a.a)")
    patch_properties.add_argument("--replace_by_ref", nargs="+", help='''
Property ID and value of the property where the value is a reference
        ''')
    patch_properties.add_argument("--remove", nargs="+", help="Remove the properties with the given ID")

    # PATCH-PROPERTIES-BY-TOKEN
    patch_properties_by_token = subparsers.add_parser("patch-properties-by-token")
    patch_properties_by_token.add_argument("user_token", help="JWT bearer token")
    patch_properties_by_token.add_argument("--add", nargs="+", help='''
Name and value of the property to add (--add email x@x.x)''')
    patch_properties_by_token.add_argument("--add_by_ref", nargs="+", help='''
Name and value of the property where the value is a reference
        ''')
    patch_properties_by_token.add_argument("--replace", nargs="+", help='''
Property ID and new value (--replace 111 a@a.a)''')
    patch_properties_by_token.add_argument("--replace_by_ref", nargs="+", help='''
Property ID and value of the property where the value is a reference
            ''')
    patch_properties_by_token.add_argument("--remove", nargs="+", help="Remove the properties with the given IDs")

    # START-DT-EMAIL-VERIFICATION
    start_dt_email_verification = subparsers.add_parser("start-dt-email-verification")
    start_dt_email_verification.add_argument("digital_twin", help="gid of the digital twin")
    start_dt_email_verification.add_argument("tenant_id", help="gid of the tenant")
    start_dt_email_verification.add_argument("email", help="email address to validate")

    # DELETE-USER (admin activity)
    del_dt = subparsers.add_parser("del-dt")
    del_dt.add_argument("digital_twin_id", help="gid ID of the digital twin for password change")
    del_dt.add_argument("tenant_id", help="gid ID of the tenant")

    # DELETE-USER-BY-TOKEN (self-service)
    del_dt_by_token = subparsers.add_parser("del-dt-by-token")
    del_dt_by_token.add_argument("user_token", help="JWT bearer token")

    # ENRICH-TOKEN
    enrich_token = subparsers.add_parser("enrich-token")
    enrich_token.add_argument("user_token", help="JWT bearer token")
    enrich_token.add_argument("--token_claims", nargs='*',
                              help="Token claims to add (--token_claims key=value)", action=ParseKwargs)
    enrich_token.add_argument("--session_claims", nargs='*',
                              help="Session claims to add (--session_claims key=value)", action=ParseKwargs)

    # customer_id
    customer_id_parser = subparsers.add_parser("customer_id")
    # customer_parser.add_argument("access_token", help="JWT bearer token")

    # customer_name
    customer_name_parser = subparsers.add_parser("customer_name")
    customer_name_parser.add_argument("customer_name", help="Customer name (not display name)")

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

    # tenant_id
    tenant_id_parser = subparsers.add_parser("tenant_id")
    tenant_id_parser.add_argument("tenant_id", help="Tenant id (gid)")

    # tenant_name
    tenant_name_parser = subparsers.add_parser("tenant_name")
    tenant_name_parser.add_argument("tenant_name", help="Tenant name (not display name)")
    tenant_name_parser.add_argument("app_space_id", help="AppSpace Id (gid)")

    # create_tenant
    create_tenant_parser = subparsers.add_parser("create_tenant")
    create_tenant_parser.add_argument("issuer_id", help="Issuer Id (gid)")
    create_tenant_parser.add_argument("tenant_name", help="Tenant name (not display name)")
    create_tenant_parser.add_argument("display_name", help="Display Name")

    # update_tenant
    update_tenant_parser = subparsers.add_parser("update_tenant")
    update_tenant_parser.add_argument("tenant_id", help="Tenant Id")
    update_tenant_parser.add_argument("etag", help="Etag")
    update_tenant_parser.add_argument("display_name", help="Display Name")

    # list_tenants
    list_tenants_parser = subparsers.add_parser("list_tenants")
    list_tenants_parser.add_argument("app_space_id", help="AppSpace Id (gid)")
    list_tenants_parser.add_argument("match_list", help="Matching names separated by ,",
                                        type=lambda s: [str(item) for item in s.split(',')])
    list_tenants_parser.add_argument("bookmark", nargs='*', help="Optional list of bookmarks separated by space")

    # delete_tenant
    delete_tenant_parser = subparsers.add_parser("delete_tenant")
    delete_tenant_parser.add_argument("tenant_id", help="Tenant Id")
    delete_tenant_parser.add_argument("etag", nargs='?', help="Optional Etag")

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
    application_agent_name_parser.add_argument("application_agent_name", help="Application agent name (not display name)")
    application_agent_name_parser.add_argument("app_space_id", help="AppSpace Id (gid)")

    # create_application_agent
    create_application_agent_parser = subparsers.add_parser("create_application_agent")
    create_application_agent_parser.add_argument("application_id", help="Application Id (gid)")
    create_application_agent_parser.add_argument("application_agent_name", help="Application agent name (not display name)")
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
    list_application_agents_parser.add_argument("bookmark", nargs='*', help="Optional list of bookmarks separated by space")

    # delete_application_agent
    delete_application_agent_parser = subparsers.add_parser("delete_application_agent")
    delete_application_agent_parser.add_argument("application_agent_id", help="Application Agent Id")
    delete_application_agent_parser.add_argument("etag", nargs='?', help="Optional Etag")

    # application_agent_credential
    application_agent_credential_parser = subparsers.add_parser("application_agent_credential")
    application_agent_credential_parser.add_argument("application_agent_credential_id", help="Application agent credential id")

    # register_application_agent_credential_jwk
    register_application_agent_credential_jwk_parser = subparsers.add_parser("register_application_agent_credential_jwk")
    register_application_agent_credential_jwk_parser.add_argument("application_agent_id", help="Application agent credential id")
    register_application_agent_credential_jwk_parser.add_argument("display_name", help="Display name")
    register_application_agent_credential_jwk_parser.add_argument("default_tenant_id", help="Default tenant id")

    # register_application_agent_credential_pem
    register_application_agent_credential_pem_parser = subparsers.add_parser("register_application_agent_credential_pem")
    register_application_agent_credential_pem_parser.add_argument("application_agent_id", help="Application agent credential id")
    register_application_agent_credential_pem_parser.add_argument("display_name", help="Display name")
    register_application_agent_credential_pem_parser.add_argument("default_tenant_id", help="Default tenant id")

    # delete_application_agent_credential
    delete_application_agent_credential_parser = subparsers.add_parser("delete_application_agent_credential")
    delete_application_agent_credential_parser.add_argument("application_agent_credential_id", help="Application agent credential id")

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
    create_service_account_parser.add_argument("role", choices=["all_editor", "all_viewer", "app_editor", "app_viewer", "authn_viewer", "authn_editor"],  help="Roles: all_editor all_viewer app_editor app_viewer authn_viewer authn_editor")

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

    # delete_service_account_credential
    delete_service_account_credential_parser = subparsers.add_parser("delete_service_account_credential")
    delete_service_account_credential_parser.add_argument("service_account_credential_id",
                                                          help="Service account credential id")

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

    # create_ingest_mapping_config_node
    create_ingest_mapping_config_node_parser = subparsers.add_parser("create_ingest_mapping_config_node")
    create_ingest_mapping_config_node_parser.add_argument("app_space_id", help="AppSpace (gid)")
    create_ingest_mapping_config_node_parser.add_argument("name", help="Name (not display name)")
    create_ingest_mapping_config_node_parser.add_argument("display_name", help="Display name")
    create_ingest_mapping_config_node_parser.add_argument("description", help="Description")

    # update_ingest_mapping_config_node
    update_ingest_mapping_config_node_parser = subparsers.add_parser("update_ingest_mapping_config_node")
    update_ingest_mapping_config_node_parser.add_argument("config_node_id", help="Config node id (gid)")
    update_ingest_mapping_config_node_parser.add_argument("etag", help="Etag")
    update_ingest_mapping_config_node_parser.add_argument("display_name", help="Display name")
    update_ingest_mapping_config_node_parser.add_argument("description", help="Description")

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

    # import_digital_twins
    import_digital_twins_parser = subparsers.add_parser("import_digital_twins")

    args = parser.parse_args()
    local = args.local
    client = IdentityClient(local)
    client_config = ConfigClient(local)

    command = args.command

    if command == "introspect":
        user_token = args.user_token
        token_info = client.introspect_token(user_token)
        if token_info is not None:
            print_response(token_info)
        else:
            print("Invalid token")

    elif command == "verify":
        verification_token = args.verification_token
        digital_twin_info = client.verify_digital_twin_email(verification_token)
        if digital_twin_info is not None:
            print_response({ "digitalTwin": digital_twin_info })

    elif command == "change-password":
        user_token = args.user_token
        new_password = args.new_password
        password_change = client.change_password(user_token, new_password)
        if password_change is not None:
            print(password_change)

    elif command == "change-password-of-user":
        digital_twin_id = args.digital_twin_id
        tenant_id = args.tenant_id
        new_password = args.new_password
        password_change = client.change_password_of_user(digital_twin_id, tenant_id, new_password)
        if password_change is not None:
            print(password_change)

    elif command == "get-dt":
        digital_twin_id = args.digital_twin_id
        tenant_id = args.tenant_id
        property_list = args.property_list
        dt = client.get_digital_twin(digital_twin_id, tenant_id, property_list[1:])
        if dt is not None:
            print_response(dt)

    elif command == "get-dt-by-token":
        user_token = args.user_token
        property_list = args.property_list
        dt = client.get_digital_twin_by_token(user_token, property_list[1:])
        if dt is not None:
            print_response(dt)

    elif command == "patch-properties":
        digital_twin_id = args.digital_twin_id
        tenant_id = args.tenant_id
        all_args = {
            "add": [],
            "add_by_ref": [],
            "replace": [],
            "replace_by_ref": [],
            "remove": []
        }

        props = args.add
        add_args_to_dict(all_args, "add", props)
        props = args.add_by_ref
        add_args_to_dict(all_args, "add_by_ref", props)
        props = args.replace
        add_args_to_dict(all_args, "replace", props)
        props = args.replace_by_ref
        add_args_to_dict(all_args, "replace_by_ref", props)
        props = args.remove
        add_args_to_dict(all_args, "remove", props)
        properties = client.patch_properties(digital_twin_id, tenant_id, all_args)
        if properties is not None:
            print(properties)

    elif command == "patch-properties-by-token":
        user_token = args.user_token
        all_args = {
            "add": [],
            "add_by_ref": [],
            "replace": [],
            "replace_by_ref": [],
            "remove": []
        }

        props = args.add
        add_args_to_dict(all_args, "add", props)
        props = args.add_by_ref
        add_args_to_dict(all_args, "add_by_ref", props)
        props = args.replace
        add_args_to_dict(all_args, "replace", props)
        props = args.replace_by_ref
        add_args_to_dict(all_args, "replace_by_ref", props)
        props = args.remove
        add_args_to_dict(all_args, "remove", props)
        properties = client.patch_properties_by_token(user_token, all_args)
        if properties is not None:
            print(properties)

    elif command == "start-dt-email-verification":
        digital_twin_id = args.digital_twin
        tenant_id = args.tenant_id
        email = args.email
        resp = client.start_digital_twin_email_verification(digital_twin_id, tenant_id, email)
        if resp is not None:
            print(resp)

    elif command == "del-dt":
        digital_twin_id = args.digital_twin_id
        tenant_id = args.tenant_id
        dt = client.del_digital_twin(digital_twin_id, tenant_id)
        if dt is not None:
            print_response({ "digitalTwin": dt })

    elif command == "del-dt-by-token":
        user_token = args.user_token
        dt = client.del_digital_twin_by_token(user_token)
        if dt is not None:
            print_response({ "digitalTwin": dt })

    elif command == "enrich-token":
        user_token = args.user_token
        token_claims = args.token_claims
        session_claims = args.session_claims
        response = client.enrich_token(user_token, token_claims, session_claims)
        if response is not None:
            print("Successfully enriched token")
        else:
            print("Invalid token")

    elif command == "customer_id":

        try:
            service_account = client_config.get_service_account()
        except Exception as exception:
            print(exception)
            return None

        print(service_account.customer_id)
        customer = client_config.get_customer_by_id(service_account.customer_id)
        if customer:
            print_response(customer)
        else:
            print("Invalid customer id")

    elif command == "customer_name":
        customer_name = args.customer_name
        customer = client_config.get_customer_by_name(customer_name)
        if customer:
            print_response(customer)
        else:
            print("Invalid customer id")

    elif command == "service_account":

        service_account = client_config.get_service_account()
        if service_account:
            print_response(service_account)
        else:
            print("Invalid service account")

    elif command == "app_space_id":
        app_space_id = args.app_space_id
        app_space = client_config.get_app_space_by_id(app_space_id)
        if app_space:
            print_response(app_space)
        else:
            print("Invalid app_space id")

    elif command == "app_space_name":
        app_space_name = args.app_space_name
        customer_id = args.customer_id
        app_space = client_config.get_app_space_by_name(customer_id, app_space_name)
        if app_space:
            print_response(app_space)
        else:
            print("Invalid app_space name")

    elif command == "create_app_space":
        app_space_name = args.app_space_name
        customer_id = args.customer_id
        display_name = args.display_name
        app_space_response = client_config.create_app_space(customer_id, app_space_name, display_name,"description", [])
        if app_space_response:
            print_response(app_space_response)
        else:
            print("Invalid app_space response")
        return app_space_response

    elif command == "update_app_space":
        app_space_id = args.app_space_id
        etag = args.etag
        display_name = args.display_name
        app_space_response = client_config.update_app_space(app_space_id, etag, display_name,"description update", [])
        if app_space_response:
            print_response(app_space_response)
        else:
            print("Invalid app_space response")
        return app_space_response

    elif command == "list_app_spaces":
        customer_id = args.customer_id
        match_list = args.match_list
        if args.bookmark:
            bookmark = args.bookmark
        else:
            bookmark = []
        list_app_spaces_response = client_config.list_app_spaces(customer_id, match_list, bookmark)
        if list_app_spaces_response:
            print(list_app_spaces_response)
        else:
            print("Invalid list_app_spaces response")
        return list_app_spaces_response

    elif command == "delete_app_space":
        app_space_id = args.app_space_id
        if args.etag:
            etag = args.etag
        else:
            etag = None

        delete_app_space_response = client_config.delete_app_space(app_space_id, etag, [])
        if delete_app_space_response:
            print(delete_app_space_response)
        else:
            print("Invalid delete_app_space_response response")
        return delete_app_space_response

    elif command == "tenant_id":
        tenant_id = args.tenant_id
        tenant = client_config.get_tenant_by_id(tenant_id)
        if tenant:
            print_response(tenant)
        else:
            print("Invalid tenant id")

    elif command == "tenant_name":
        tenant_name = args.tenant_name
        app_space_id = args.app_space_id
        tenant = client_config.get_tenant_by_name(app_space_id, tenant_name)
        if tenant:
            print_response(tenant)
        else:
            print("Invalid tenant name")

    elif command == "create_tenant":
        tenant_name = args.tenant_name
        issuer_id = args.issuer_id
        display_name = args.display_name
        tenant_response = client_config.create_tenant(issuer_id, tenant_name, display_name,"description", [])
        if tenant_response:
            print_response(tenant_response)
        else:
            print("Invalid tenant response")
        return tenant_response

    elif command == "update_tenant":
        tenant_id = args.tenant_id
        etag = args.etag
        display_name = args.display_name
        tenant_response = client_config.update_tenant(tenant_id, etag, display_name,"description update", [])
        if tenant_response:
            print_response(tenant_response)
        else:
            print("Invalid tenant response")
        return tenant_response

    elif command == "list_tenants":
        app_space_id = args.app_space_id
        match_list = args.match_list
        if args.bookmark:
            bookmark = args.bookmark
        else:
            bookmark = []
        list_tenants_response = client_config.list_tenants(app_space_id, match_list, bookmark)
        if list_tenants_response:
            print(list_tenants_response)
        else:
            print("Invalid list_tenants response")
        return list_tenants_response

    elif command == "delete_tenant":
        tenant_id = args.tenant_id
        if args.etag:
            etag = args.etag
        else:
            etag = None

        delete_tenant_response = client_config.delete_tenant(tenant_id, etag, [])
        if delete_tenant_response:
            print(delete_tenant_response)
        else:
            print("Invalid delete_tenant_response response")
        return delete_tenant_response

    elif command == "application_id":
        application_id = args.application_id
        application = client_config.get_application_by_id(application_id)
        if application:
            print_response(application)
        else:
            print("Invalid application id")

    elif command == "application_name":
        application_name = args.application_name
        app_space_id = args.app_space_id
        application = client_config.get_application_by_name(app_space_id, application_name)
        if application:
            print_response(application)
        else:
            print("Invalid application name")

    elif command == "create_application":
        app_space_id = args.app_space_id
        application_name = args.application_name
        display_name = args.display_name
        application_response = client_config.create_application(app_space_id, application_name, display_name,
                                                                "description", [])
        if application_response:
            print_response(application_response)
        else:
            print("Invalid application response")
        return application_response

    elif command == "update_application":
        application_id = args.application_id
        etag = args.etag
        display_name = args.display_name
        application_response = client_config.update_application(application_id, etag, display_name,"description update", [])
        if application_response:
            print_response(application_response)
        else:
            print("Invalid application response")
        return application_response

    elif command == "list_applications":
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
        return list_applications_response

    elif command == "delete_application":
        application_id = args.application_id
        if args.etag:
            etag = args.etag
        else:
            etag = None

        delete_application_response = client_config.delete_application(application_id, etag, [])
        if delete_application_response:
            print(delete_application_response)
        else:
            print("Invalid delete_application_response response")
        return delete_application_response

    elif command == "application_agent_id":
        application_agent_id = args.application_agent_id
        application_agent = client_config.get_application_agent_by_id(application_agent_id)
        if application_agent:
            print_response(application_agent)
        else:
            print("Invalid application agent id")

    elif command == "application_agent_name":
        application_agent_name = args.application_agent_name
        app_space_id = args.app_space_id
        application_agent = client_config.get_application_agent_by_name(app_space_id, application_agent_name)
        if application_agent:
            print_response(application_agent)
        else:
            print("Invalid application agent name")

    elif command == "create_application_agent":
        application_id = args.application_id
        application_agent_name = args.application_agent_name
        display_name = args.display_name
        application_agent_response = client_config.create_application_agent(application_id, application_agent_name, display_name,
                                                                "description", [])
        if application_agent_response:
            print_response(application_agent_response)
        else:
            print("Invalid application agent response")
        return application_agent_response

    elif command == "update_application_agent":
        application_agent_id = args.application_agent_id
        etag = args.etag
        display_name = args.display_name
        application_agent_response = client_config.update_application_agent(application_agent_id, etag, display_name,"description update", [])
        if application_agent_response:
            print_response(application_agent_response)
        else:
            print("Invalid application agent response")
        return application_agent_response

    elif command == "list_application_agents":
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
        return list_application_agents_response

    elif command == "delete_application_agent":
        application_agent_id = args.application_agent_id
        if args.etag:
            etag = args.etag
        else:
            etag = None

        delete_application_agent_response = client_config.delete_application_agent(application_agent_id, etag, [])
        if delete_application_agent_response:
            print(delete_application_agent_response)
        else:
            print("Invalid delete_application_response_agent response")
        return delete_application_agent_response

    elif command == "application_agent_credential":
        application_agent_credential_id = args.application_agent_credential_id
        application_agent_credential = client_config.get_application_agent_credential(application_agent_credential_id)
        if application_agent_credential:
            print_response(application_agent_credential)
        else:
            print("Invalid application agent id")

    elif command == "register_application_agent_credential_jwk":
        application_agent_id = args.application_agent_id
        display_name = args.display_name
        default_tenant_id = args.default_tenant_id
        jwk = None
        t = datetime.now().timestamp()
        expire_time_in_seconds = int(t) + 2678400 # now + one month example
        application_agent_credential_response = client_config.register_application_agent_credential_jwk(application_agent_id,
                                                                                             display_name, jwk,
                                                                                             expire_time_in_seconds,
                                                                                             default_tenant_id, [])
        if application_agent_credential_response:
            print_credential(application_agent_credential_response)
        else:
            print("Invalid application agent response")
        return application_agent_credential_response

    elif command == "register_application_agent_credential_pem":
        application_agent_id = args.application_agent_id
        display_name = args.display_name
        default_tenant_id = args.default_tenant_id
        pem = None
        t = datetime.now().timestamp()
        expire_time_in_seconds = int(t) + 2678400 # now + one month example
        application_agent_credential_response = client_config.register_application_agent_credential_pem(application_agent_id,
                                                                                             display_name, pem,
                                                                                             expire_time_in_seconds,
                                                                                             default_tenant_id, [])
        if application_agent_credential_response:
            print_credential(application_agent_credential_response)
        else:
            print("Invalid application agent response")
        return application_agent_credential_response

    elif command == "delete_application_agent_credential":
        application_agent_credential_id = args.application_agent_credential_id

        delete_application_agent_credential_response = client_config.delete_application_agent_credential(application_agent_credential_id, [])
        if delete_application_agent_credential_response:
            print(delete_application_agent_credential_response)
        else:
            print("Invalid delete_application_agent_credential_response response")
        return delete_application_agent_credential_response

    elif command == "service_account_id":
        service_account_id = args.service_account_id
        service_account = client_config.get_service_account(service_account_id)
        if service_account:
            print_response(service_account)
        else:
            print("Invalid service account")

    elif command == "service_account_name":
        customer_id = args.customer_id
        service_account_name = args.service_account_name
        service_account = client_config.get_service_account_by_name(customer_id, service_account_name)
        if service_account:
            print_response(service_account)
        else:
            print("Invalid service_account name")

    elif command == "create_service_account":
        customer_id = args.customer_id
        service_account_name = args.service_account_name
        display_name = args.display_name
        role = args.role
        service_account_response = client_config.create_service_account(customer_id, service_account_name, display_name,"description", role, [])
        if service_account_response:
            print_response(service_account_response)
        else:
            print("Invalid service_account response")
        return service_account_response

    elif command == "update_service_account":
        service_account_id = args.service_account_id
        etag = args.etag
        display_name = args.display_name
        service_account_response = client_config.update_service_account(service_account_id, etag, display_name,"description", [])
        if service_account_response:
            print_response(service_account_response)
        else:
            print("Invalid service_account response")
        return service_account_response

    elif command == "delete_service_account":
        service_account_id = args.service_account_id
        if args.etag:
            etag = args.etag
        else:
            etag = None

        delete_service_account_response = client_config.delete_service_account(service_account_id, etag, [])
        if delete_service_account_response:
            print(delete_service_account_response)
        else:
            print("Invalid delete_service_account response")
        return delete_service_account_response

    elif command == "service_account_credential":
        service_account_credential_id = args.service_account_credential_id
        service_account_credential = client_config.get_service_account_credential(service_account_credential_id)
        if service_account_credential:
            print_response(service_account_credential)
        else:
            print("Invalid service account id")

    elif command == "register_service_account_credential_jwk":
        service_account_id = args.service_account_id
        display_name = args.display_name
        jwk = None
        t = datetime.now().timestamp()
        expire_time_in_seconds = int(t) + 2678400 # now + one month example
        service_account_credential_response = client_config.register_service_account_credential_jwk(service_account_id,
                                                                                                    display_name, jwk,
                                                                                                    expire_time_in_seconds,
                                                                                                    [])
        if service_account_credential_response:
            print_credential(service_account_credential_response)
        else:
            print("Invalid service account response")
        return service_account_credential_response

    elif command == "register_service_account_credential_pem":
        service_account_id = args.service_account_id
        display_name = args.display_name
        default_tenant_id = args.default_tenant_id
        pem = None
        t = datetime.now().timestamp()
        expire_time_in_seconds = int(t) + 2678400 # now + one month example
        service_account_credential_response = client_config.register_service_account_credential_pem(service_account_id,
                                                                                             display_name, pem,
                                                                                             expire_time_in_seconds,
                                                                                             default_tenant_id, [])
        if service_account_credential_response:
            print_credential(service_account_credential_response)
        else:
            print("Invalid service account response")
        return service_account_credential_response

    elif command == "delete_service_account_credential":
        service_account_credential_id = args.service_account_credential_id

        delete_service_account_credential_response = client_config.delete_service_account_credential(service_account_credential_id, [])
        if delete_service_account_credential_response:
            print(delete_service_account_credential_response)
        else:
            print("Invalid delete_service_account_credential_response response")
        return delete_service_account_credential_response

    elif command == "create_email_service_config_node":
        location = args.customer_id
        name = args.name
        display_name = args.display_name
        description = args.description

        default_from_address_address="test+config@indykite.com"
        default_from_address_name="Test Config"

        sendgrid = SendGridProviderConfig(
            api_key="263343b5-983e-4d73-b666-069a98f1ef55",
            sandbox_mode=True,
            ip_pool_name=wrappers.StringValue(value="100.45.21.65.25"),
            host=wrappers.StringValue(value="https://api.sendgrid.com")
        )

        message_from = Email(address='test+from@indykite.com', name='Test From')
        message_to = [Email(address='test+to@indykite.com', name='Test To')]
        message_subject = "subject"
        message_text_content = "content text"
        message_html_content = "<html><body>content html</body></html>"

        email_service_config = EmailServiceConfig(
            default_from_address=Email(address=default_from_address_address,name=default_from_address_name),
            default=wrappers.BoolValue(value=True),
            sendgrid=sendgrid,
            authentication_message=EmailDefinition(message=EmailMessage(to=message_to, cc=[], bcc=[],
                                                                          subject=message_subject,
                                                                          text_content=message_text_content,
                                                                          html_content=message_html_content))
        )

        create_email_service_config_node_response = client_config.create_email_service_config_node(location, name,
                                                                                                   display_name,
                                                                                                   description,
                                                                                                   email_service_config,
                                                                                                   [])
        if create_email_service_config_node_response:
            print_response(create_email_service_config_node_response)
        else:
            print("Invalid create email service config node response")
        return create_email_service_config_node_response

    elif command == "read_config_node":
        config_node_id = args.config_node_id
        config_node = client_config.read_config_node(config_node_id,[])
        if config_node:
            print_response(config_node)
            if config_node.auth_flow_config:
                source = config_node.auth_flow_config.source
                if source:
                    print(json.loads(source.decode('utf-8')))
        else:
            print("Invalid config node id")

    elif command == "update_email_service_config_node":
        config_node_id = args.config_node_id
        etag = args.etag
        display_name = args.display_name
        description = args.description

        default_from_address_address="test+config@indykite.com"
        default_from_address_name="Test Config"

        sendgrid = SendGridProviderConfig(
            api_key="263343b5-983e-4d73-b666-069a98f1ef55",
            sandbox_mode=True,
            ip_pool_name=wrappers.StringValue(value="100.45.21.65.28"),
            host=wrappers.StringValue(value="https://api.sendgrid.com")
        )

        message_to = [Email(address='test+to@indykite.com', name='Test To')]
        message_subject = "subject2"
        message_text_content = "content text"
        message_html_content = "<html><body>content html</body></html>"

        email_service_config = EmailServiceConfig(
            default_from_address=Email(address=default_from_address_address,name=default_from_address_name),
            default=wrappers.BoolValue(value=True),
            sendgrid=sendgrid,
            authentication_message=EmailDefinition(message=EmailMessage(to=message_to, cc=[], bcc=[],
                                                                          subject=message_subject,
                                                                          text_content=message_text_content,
                                                                          html_content=message_html_content))
        )

        update_email_service_config_node_response = client_config.update_email_service_config_node(config_node_id, etag,
                                                                                                   display_name,
                                                                                                   description,
                                                                                                   email_service_config,
                                                                                                   [])
        if update_email_service_config_node_response:
            print_response(update_email_service_config_node_response)
        else:
            print("Invalid update email service config node response")
        return update_email_service_config_node_response

    elif command == "delete_config_node":
        config_node_id = args.config_node_id
        etag = args.etag
        config_node = client_config.delete_config_node(config_node_id, etag, [])
        if config_node:
            print_response(config_node)
        else:
            print("Invalid delete config node response")

    elif command == "create_auth_flow_config_node":
        location = args.app_space_id
        name = args.name
        display_name = args.display_name
        description = args.description

        with open("utils/sdk_simple_flow.json") as f:
            file_data = f.read()
        user_dict = json.loads(file_data)
        user_dict = json.dumps(user_dict, indent=4, separators=(',', ': ')).encode('utf-8')

        #only bare JSON or YAML source_format is support as input
        auth_flow_config = AuthFlowConfig(
            source_format="FORMAT_BARE_JSON",
            source=bytes(user_dict),
            default=wrappers.BoolValue(value=False)
        )

        create_auth_flow_config_node_response = client_config.create_auth_flow_config_node(location, name, display_name,
                                                                                           description, auth_flow_config,
                                                                                           [])
        if create_auth_flow_config_node_response:
            print_response(create_auth_flow_config_node_response)
        else:
            print("Invalid create auth flow config node response")
        return create_auth_flow_config_node_response

    elif command == "update_auth_flow_config_node":
        config_node_id = args.config_node_id
        etag = args.etag
        display_name = args.display_name
        description = args.description

        with open("utils/sdk_simple_flow.json") as f:
            file_data = f.read()
        user_dict = json.loads(file_data)
        user_dict = json.dumps(user_dict, indent=4, separators=(',', ': ')).encode('utf-8')

        auth_flow_config = AuthFlowConfig(
            source_format="FORMAT_BARE_JSON",
            source=bytes(user_dict),
            default=wrappers.BoolValue(value=False)
        )

        update_auth_flow_config_node_response = client_config.update_auth_flow_config_node(config_node_id, etag,display_name,
                                                                                           description, auth_flow_config, [])
        if update_auth_flow_config_node_response:
            print_response(update_auth_flow_config_node_response)
        else:
            print("Invalid update auth flow config node response")
        return update_auth_flow_config_node_response

    elif command == "create_oauth2_client_config_node":
        location = args.app_space_id
        name = args.name
        display_name = args.display_name
        description = args.description

        oauth2_client_config = OAuth2ClientConfig(
            provider_type="PROVIDER_TYPE_GOOGLE_COM",
            client_id="gt41g2ju85ol1j2u1t",
            client_secret="e45454JIIH45ven9e8sbfdv4d5",
            default_scopes=["openid", "profile", "email"],
            allowed_scopes=["openid", "profile", "email"]
        )

        create_oauth2_client_config_node_response = client_config.create_oauth2_client_config_node(location, name,
                                                                                                   display_name,
                                                                                                   description,
                                                                                                   oauth2_client_config, [])
        if create_oauth2_client_config_node_response:
            print_response(create_oauth2_client_config_node_response)
        else:
            print("Invalid create oauth2 client config node response")
        return create_oauth2_client_config_node_response

    elif command == "update_oauth2_client_config_node":
        config_node_id = args.config_node_id
        etag = args.etag
        display_name = args.display_name
        description = args.description

        oauth2_client_config = OAuth2ClientConfig(
            provider_type="PROVIDER_TYPE_GOOGLE_COM",
            client_id="gt41g2ju85ol1j2u1t",
            client_secret="e45454JIIH45ven9e8sbfdv4d5",
            default_scopes=["openid", "profile", "email"],
            allowed_scopes=["openid", "profile", "email"]
        )

        update_oauth2_client_config_node_response = client_config.update_oauth2_client_config_node(config_node_id, etag,
                                                                                                   display_name,
                                                                                                   description,
                                                                                                   oauth2_client_config, [])
        if update_oauth2_client_config_node_response:
            print_response(update_oauth2_client_config_node_response)
        else:
            print("Invalid update oauth2 client config node response")
        return update_oauth2_client_config_node_response

    elif command == "create_ingest_mapping_config_node":
        location = args.app_space_id
        name = args.name
        display_name = args.display_name
        description = args.description

        ingest_mapping_config=IngestMappingConfig(
            upsert=IngestMappingConfig.UpsertData(
                entities=[IngestMappingConfig.Entity(
                    tenant_id="gid:AAAAA9Q51FULGECVrvbfN0kUbSk",
                    labels=["DigitalTwin","Client"],
                    external_id=IngestMappingConfig.Property(
                        source_name="client",
                        mapped_name="user",
                        is_required=True),
                    properties=[IngestMappingConfig.Property(
                        source_name="family",
                        mapped_name="family",
                        is_required=False)],
                    relationships=[IngestMappingConfig.Relationship(
                        external_id="hetj4548484545f4",
                        type="MOTHER_OF",
                        direction="DIRECTION_INBOUND",
                        match_label="Mothers")]
                )]
            )
        )

        create_ingest_mapping_config_node_response = client_config.create_ingest_mapping_config_node(
            location, name, display_name, description, ingest_mapping_config, [])
        if create_ingest_mapping_config_node_response:
            print_response(create_ingest_mapping_config_node_response)
        else:
            print("Invalid create ingest mapping config node response")
        return create_ingest_mapping_config_node_response

    elif command == "update_ingest_mapping_config_node":
        config_node_id = args.config_node_id
        etag = args.etag
        display_name = args.display_name
        description = args.description

        ingest_mapping_config = IngestMappingConfig(
            upsert=IngestMappingConfig.UpsertData(
                entities=[IngestMappingConfig.Entity(
                    tenant_id="gid:AAAAA9Q51FULGECVrvbfN0kUbSk",
                    labels=["DigitalTwin", "Client"],
                    external_id=IngestMappingConfig.Property(
                        source_name="client",
                        mapped_name="user",
                        is_required=True),
                    properties=[IngestMappingConfig.Property(
                        source_name="family",
                        mapped_name="family",
                        is_required=False)],
                    relationships=[IngestMappingConfig.Relationship(
                        external_id="hetj4548484545f4",
                        type="MOTHER_OF",
                        direction="DIRECTION_INBOUND",
                        match_label="Mothers")]
                )]
            )
        )

        update_ingest_mapping_config_node_response = client_config.update_ingest_mapping_config_node(
            config_node_id,
            etag,
            display_name,
            description,
            ingest_mapping_config,
            [])

        if update_ingest_mapping_config_node_response:
            print_response(update_ingest_mapping_config_node_response)
        else:
            print("Invalid update ingest mapping config node response")
        return update_ingest_mapping_config_node_response

    elif command == "read_oauth2_provider":
        oauth2_provider_id = args.oauth2_provider_id
        config = client_config.read_oauth2_provider(oauth2_provider_id, [])
        if config:
            print_response(config)
        else:
            print("Invalid oauth2 provider id")

    elif command == "create_oauth2_provider":
        app_space_id = args.app_space_id
        name = args.name
        display_name = args.display_name
        description = args.description

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

        create_oauth2_provider_response = client_config.create_oauth2_provider(app_space_id,
                                                                               name,
                                                                               display_name,
                                                                               description,
                                                                               config,
                                                                               [])
        if create_oauth2_provider_response:
            print_response(create_oauth2_provider_response)
        else:
            print("Invalid create oauth2 provider response")
        return create_oauth2_provider_response

    elif command == "update_oauth2_provider":
        oauth2_provider_id = args.oauth2_provider_id
        etag = args.etag
        display_name = args.display_name
        description = args.description

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

        update_oauth2_provider_response = client_config.update_oauth2_provider(oauth2_provider_id,
                                                                               etag,
                                                                               display_name,
                                                                               description,
                                                                               config,
                                                                               [])
        if update_oauth2_provider_response:
            print_response(update_oauth2_provider_response)
        else:
            print("Invalid update oauth2 provider response")
        return update_oauth2_provider_response

    elif command == "delete_oauth2_provider":
        oauth2_provider_id = args.oauth2_provider_id
        etag = args.etag
        config = client_config.delete_oauth2_provider(oauth2_provider_id, etag, [])
        if config:
            print_response(config)
        else:
            print("Invalid delete oauth2 provider response")

    elif command == "read_oauth2_application":
        oauth2_application_id = args.oauth2_application_id
        config = client_config.read_oauth2_application(oauth2_application_id, [])
        if config:
            print_response(config)
        else:
            print("Invalid oauth2 application id")

    elif command == "create_oauth2_application":
        oauth2_provider_id = args.oauth2_provider_id
        name = args.name
        display_name = args.display_name
        description = args.description

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
            scopes = ["openid", "profile", "email"],
            token_endpoint_auth_method = "TOKEN_ENDPOINT_AUTH_METHOD_CLIENT_SECRET_BASIC",
            token_endpoint_auth_signing_alg = "ES256",
            grant_types=["GRANT_TYPE_AUTHORIZATION_CODE"],
            response_types=["RESPONSE_TYPE_CODE", "RESPONSE_TYPE_TOKEN"]
        )

        create_oauth2_application_response = client_config.create_oauth2_application(oauth2_provider_id,
                                                                                     name,
                                                                                     display_name,
                                                                                     description,
                                                                                     config,
                                                                                     [])
        if create_oauth2_application_response:
            print_response(create_oauth2_application_response)
        else:
            print("Invalid create oauth2 application response")
        return create_oauth2_application_response

    elif command == "update_oauth2_application":
        oauth2_application_id = args.oauth2_application_id
        etag = args.etag
        display_name = args.display_name
        description = args.description

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

        update_oauth2_application_response = client_config.update_oauth2_application(oauth2_application_id,
                                                                                     etag,
                                                                                     display_name,
                                                                                     description,
                                                                                     config,
                                                                                     [])
        if update_oauth2_application_response:
            print_response(update_oauth2_application_response)
        else:
            print("Invalid update oauth2 application response")
        return update_oauth2_application_response

    elif command == "delete_oauth2_application":
        oauth2_application_id = args.oauth2_application_id
        etag = args.etag
        config = client_config.delete_oauth2_application(oauth2_application_id, etag, [])
        if config:
            print_response(config)
        else:
            print("Invalid delete oauth2 application response")

    elif command == "import_digital_twins":

        entities = [ImportDigitalTwin(
            tenant_id="696e6479-6b69-4465-8000-030f00000001",
            kind="DIGITAL_TWIN_KIND_PERSON",
            state="DIGITAL_TWIN_STATE_ACTIVE",
            password=PasswordCredential(
                email=EmailIdentity(
                    email="test2000@example.com",
                    verified=True
                ),
                hash=PasswordHash(
                    password_hash=bytes("$2y$10$k64jP7oqwYfQpzmoqAN5OuhrtWI2wICn0wXUzYxMp.UA1PopI653G", "utf-8")
                )
            )
        )]
        hash_algorithm = Bcrypt()

        import_digital_twins_config_response = client.import_digital_twins(
            entities,hash_algorithm)
        if import_digital_twins_config_response:
            print_response(import_digital_twins_config_response)
        else:
            print("Invalid import digital twins response")
        return import_digital_twins_config_response


def print_verify_info(digital_twin_info):  # pragma: no cover
    print("Digital twin info")
    print("=================")
    print("Tenant: " + str(UUID(bytes=digital_twin_info.digital_twin.tenant_id)))
    print("Digital twin: " + str(UUID(bytes=digital_twin_info.digital_twin.id)))


def print_credential(credential):  # pragma: no cover
    print("Credential")
    print("==========")
    print("Credential id: " + str(credential.id))
    print("Kid: " + str(credential.kid))
    if hasattr(credential, 'agent_config'):
        print("Agent config: " + str(credential.agent_config))
    elif hasattr(credential, 'service_account_config'):
        print("Service account config: " + str(credential.service_account_config))
    print("Bookmark: " + str(credential.bookmark))
    print("Create time: " + str(credential.create_time))
    print("Expire time: " + str(credential.expire_time))


def print_token_info(token_info):  # pragma: no cover
    print("Token info")
    print("==========")
    print("Tenant: " + str(UUID(bytes=token_info.tenant_id)))
    print("Customer: " + str(UUID(bytes=token_info.customer_id)))
    print("App space: " + str(UUID(bytes=token_info.app_space_id)))
    print("Application: " + str(UUID(bytes=token_info.application_id)))
    print("Subject: " + str(UUID(bytes=token_info.subject_id)))
    print("Expire time: " + str(datetime.fromtimestamp(token_info.expire_time.seconds)))


def print_response(resp):  # pragma: no cover
    def get_default(x):
        if type(x) is datetime:
            return str(x)
        else:
            return x.__dict__

    if hasattr(resp, "DESCRIPTOR"):
        js = MessageToJson(resp)
        js_dict = json.loads(js)
        prettify(js_dict)
    else:
        js_dict = resp
    pretty_response = json.dumps(js_dict, indent=4, separators=(',', ': '), default=get_default)
    print(pretty_response)


def prettify(js):  # pragma: no cover
    for k, v in js.items():
        if isinstance(v, type(dict())):
            prettify(v)
        elif isinstance(v, type(list())):
            for val in v:
                if isinstance(val, type(str())):
                    val = format_convert(k, val)
                    pass
                elif isinstance(val, type(list())) | isinstance(val, type(float())) | isinstance(val, type(
                    bool())) | isinstance(val, type(None)):
                    pass
                else:
                    prettify(val)
        else:
            if isinstance(v, str):
                js[k] = format_convert(k, v)


def format_convert(k, v):  # pragma: no cover
    try:
        if "id" in k:
            i = int(v)
            return i
    except ValueError:
        pass
    return str(base64_to_uuid(v))


def base64_to_uuid(b):  # pragma: no cover
    try:
        s = b.encode('ascii')
        uid = UUID(bytes=base64.b64decode(s))
    except ValueError:
        return b
    return uid


def add_args_to_dict(all_args, action, values):  # pragma: no cover
    if action == "add" and values is not None:
        for v in values:
            all_args["add"].append(v)
    elif action == "add_by_ref" and values is not None:
        for v in values:
            all_args["add_by_ref"].append(v)
    elif action == "replace" and values is not None:
        for v in values:
            all_args["replace"].append(v)
    elif action == "replace_by_ref" and values is not None:
        for v in values:
            all_args["replace_by_ref"].append(v)
    elif action == "remove" and values is not None:
        for v in values:
            all_args["remove"].append(v)

    return all_args


if __name__ == '__main__':  # pragma: no cover
    main()
