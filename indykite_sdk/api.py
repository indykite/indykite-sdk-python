"""
Commandline interface for making an API request with the SDK.
"""
import argparse
import base64
import json
from datetime import datetime
from uuid import UUID
import uuid
from google.protobuf.json_format import MessageToJson
from google.protobuf.duration_pb2 import Duration
import os
import requests
from indykite_sdk.utils.hash_methods import encrypt_bcrypt
from indykite_sdk.identity import IdentityClient
from indykite_sdk.config import ConfigClient
from indykite_sdk.authorization import AuthorizationClient
from indykite_sdk.oauth2 import HttpClient
from indykite_sdk.indykite.config.v1beta1.model_pb2 import (SendGridProviderConfig, MailJetProviderConfig, AmazonSESProviderConfig, MailgunProviderConfig)
from indykite_sdk.indykite.config.v1beta1.model_pb2 import (EmailServiceConfig, AuthFlowConfig, OAuth2ClientConfig, IngestMappingConfig, WebAuthnProviderConfig, AuthorizationPolicyConfig )
from indykite_sdk.indykite.config.v1beta1.model_pb2 import OAuth2ProviderConfig, OAuth2ApplicationConfig
from indykite_sdk.indykite.identity.v1beta2.import_pb2 import ImportDigitalTwinsRequest, ImportDigitalTwin
from indykite_sdk.indykite.identity.v1beta2.import_pb2 import PasswordCredential, PasswordHash, Bcrypt, SHA256
from indykite_sdk.indykite.config.v1beta1.model_pb2 import EmailAttachment, Email, EmailMessage, EmailTemplate, EmailDefinition
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from indykite_sdk.indykite.identity.v1beta2.import_pb2 import Email as EmailIdentity
from indykite_sdk.model.is_authorized import IsAuthorizedResource
from indykite_sdk.model.what_authorized import WhatAuthorizedResourceTypes
from indykite_sdk.model.who_authorized import WhoAuthorizedResource
from indykite_sdk.model.tenant import Tenant
from indykite_sdk.indykite.identity.v1beta2 import attributes_pb2 as attributes
from indykite_sdk.ingest import IngestClient
from indykite_sdk.identity import helper
import logging


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

    # SESSION_INTROSPECT
    session_introspect_parser = subparsers.add_parser("session_introspect")
    session_introspect_parser.add_argument("tenant_id", help="gid ID of the tenant")
    session_introspect_parser.add_argument("access_token", help="JWT bearer token")

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

    # create_application_with_agent_credentials
    create_application_with_agent_credentials_parser = subparsers.add_parser("create_application_with_agent_credentials")
    create_application_with_agent_credentials_parser.add_argument("app_space_id", help="AppSpace Id (gid)")
    create_application_with_agent_credentials_parser.add_argument("tenant_id", help="Tenant Id (gid)")
    create_application_with_agent_credentials_parser.add_argument("application_name", help="Application name")
    create_application_with_agent_credentials_parser.add_argument("application_agent_name", help="Application Agent Name")
    create_application_with_agent_credentials_parser.add_argument("application_agent_credentials_name", help="Application Agent Credentials Name")
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
    delete_service_account_credential_parser.add_argument("etag", nargs='?', help="Optional Etag")

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

    # import_digital_twins
    import_digital_twins_parser = subparsers.add_parser("import_digital_twins")
    import_digital_twins_parser.add_argument("tenant_id", help="Tenant id (gid)")

    # import_digital_twins_hash
    import_digital_twins_hash_parser = subparsers.add_parser("import_digital_twins_hash")
    import_digital_twins_hash_parser.add_argument("tenant_id", help="Tenant id (gid)")

    # import_digital_twins_hash_sha
    import_digital_twins_hash_sha_parser = subparsers.add_parser("import_digital_twins_hash_sha")
    import_digital_twins_hash_sha_parser.add_argument("tenant_id", help="Tenant id (gid)")
    import_digital_twins_hash_sha_parser.add_argument("hash_password", help="Hashed password")

    # import_digital_twins_update
    import_digital_twins_update_parser = subparsers.add_parser("import_digital_twins_update")
    import_digital_twins_update_parser.add_argument("id", help="Digital Twin id (gid)")
    import_digital_twins_update_parser.add_argument("tenant_id", help="Tenant id (gid)")

    # is_authorized_dt
    is_authorized_dt_parser = subparsers.add_parser("is_authorized_dt")
    is_authorized_dt_parser.add_argument("digital_twin_id", help="Digital Twin id (gid)")
    is_authorized_dt_parser.add_argument("tenant_id", help="Tenant id (gid)")

    # is_authorized_token
    is_authorized_token_parser = subparsers.add_parser("is_authorized_token")
    is_authorized_token_parser.add_argument("access_token")

    # is_authorized_property
    is_authorized_property_parser = subparsers.add_parser("is_authorized_property")
    is_authorized_property_parser.add_argument("property_type", help="Digital Twin Identity Property")
    is_authorized_property_parser.add_argument("property_value", help="Digital Twin Identity Property value")

    # what_authorized_dt
    what_authorized_dt_parser = subparsers.add_parser("what_authorized_dt")
    what_authorized_dt_parser.add_argument("digital_twin_id", help="Digital Twin id (gid)")
    what_authorized_dt_parser.add_argument("tenant_id", help="Tenant id (gid)")

    # what_authorized_token
    what_authorized_token_parser = subparsers.add_parser("what_authorized_token")
    what_authorized_token_parser.add_argument("access_token")

    # what_authorized_property
    what_authorized_property_parser = subparsers.add_parser("what_authorized_property")
    what_authorized_property_parser.add_argument("property_type", help="Digital Twin Identity Property")
    what_authorized_property_parser.add_argument("property_value", help="Digital Twin Identity Property value")

    # who_authorized
    who_authorized_parser = subparsers.add_parser("who_authorized")

    # create_consent
    create_consent_parser = subparsers.add_parser("create_consent")
    create_consent_parser.add_argument("pii_processor_id", help="ID of OAuth2 Application")
    create_consent_parser.add_argument("pii_principal_id", help="DigitalTwin Id (gid)")

    # list_consents
    list_consents_parser = subparsers.add_parser("list_consents")
    list_consents_parser.add_argument("pii_principal_id", help="DigitalTwin Id (gid)")

    # revoke_consent
    revoke_consent_parser = subparsers.add_parser("revoke_consent")
    revoke_consent_parser.add_argument("pii_principal_id", help="DigitalTwin Id (gid)")
    revoke_consent_parser.add_argument("consent_ids", nargs='*', help="List of consent ids separated by space")

    # check_oauth2_consent_challenge
    check_oauth2_consent_challenge_parser = subparsers.add_parser("check_oauth2_consent_challenge")
    check_oauth2_consent_challenge_parser.add_argument("challenge",
                                                       help="Consent challenge extracted from consent URL")

    # create_oauth2_consent_verifier_approval
    create_oauth2_consent_verifier_approval_parser = subparsers.add_parser("create_oauth2_consent_verifier_approval")
    create_oauth2_consent_verifier_approval_parser.add_argument("consent_challenge",
                                                                help="Consent challenge extracted from consent URL")
    create_oauth2_consent_verifier_approval_parser.add_argument("access_token")

    # create_oauth2_consent_verifier_denial
    create_oauth2_consent_verifier_denial_parser = subparsers.add_parser("create_oauth2_consent_verifier_denial")
    create_oauth2_consent_verifier_denial_parser.add_argument("consent_challenge",
                                                              help="Consent challenge extracted from consent URL")

    # FORGOTTEN_PASSWORD
    start_forgotten_password = subparsers.add_parser("start_forgotten_password")
    start_forgotten_password.add_argument("digital_twin_id", help="gid ID of the digital twin with forgotten password")
    start_forgotten_password.add_argument("tenant_id", help="gid ID of the tenant")

    # create_email_invitation
    create_email_invitation = subparsers.add_parser("create_email_invitation")
    create_email_invitation.add_argument("tenant_id", help="gid ID of the tenant")
    create_email_invitation.add_argument("email", help="invitee's email")

    # create_email_invitation_with_date
    create_email_invitation_with_date = subparsers.add_parser("create_email_invitation_with_date")
    create_email_invitation_with_date.add_argument("tenant_id", help="gid ID of the tenant")
    create_email_invitation_with_date.add_argument("email", help="invitee's email")

    # create_mobile_invitation
    create_mobile_invitation = subparsers.add_parser("create_mobile_invitation")
    create_mobile_invitation.add_argument("tenant_id", help="gid ID of the tenant")
    create_mobile_invitation.add_argument("mobile", help="invitee's mobile")

    # check_invitation_state
    check_invitation_state = subparsers.add_parser("check_invitation_state")
    check_invitation_state.add_argument("reference_id", help="external ID of the invitation reference")

    # resend_invitation
    resend_invitation = subparsers.add_parser("resend_invitation")
    resend_invitation.add_argument("reference_id", help="external ID of the invitation reference")

    # cancel_invitation
    cancel_invitation = subparsers.add_parser("cancel_invitation")
    cancel_invitation.add_argument("reference_id", help="external ID of the invitation reference")

    # register_digital_twin_without_credential
    register_digital_twin_without_credential = subparsers.add_parser("register_digital_twin_without_credential")
    register_digital_twin_without_credential.add_argument("tenant_id", help="gid ID of the tenant")

    # get_http_client
    get_http_client = subparsers.add_parser("get_http_client")
    get_http_client.add_argument("base_url", help="knowledge endpoint")

    # get_refreshable_token_source
    get_refreshable_token_source = subparsers.add_parser("get_refreshable_token_source")

    # ingest
    ingest_record_digital_twin = subparsers.add_parser("ingest_record_digital_twin")
    ingest_record_resource = subparsers.add_parser("ingest_record_resource")
    ingest_record_relation = subparsers.add_parser("ingest_record_relation")
    delete_record_relation_property = subparsers.add_parser("delete_record_relation_property")
    delete_record_node_property = subparsers.add_parser("delete_record_node_property")
    delete_record_relation = subparsers.add_parser("delete_record_relation")
    delete_record_node = subparsers.add_parser("delete_record_node")
    stream_records = subparsers.add_parser("stream_records")

    args = parser.parse_args()
    local = args.local
    client = IdentityClient(local)
    client_config = ConfigClient(local)
    client_authorization = AuthorizationClient(local)
    client_ingest = IngestClient(local)

    command = args.command

    if command == "introspect":
        user_token = args.user_token
        token_info = client.token_introspect(user_token)
        if token_info is not None:
            print_response(token_info)
        else:
            print("Invalid token")

    elif command == "session_introspect":
        tenant_id = args.tenant_id
        access_token = args.access_token
        session_response = client.session_introspect(tenant_id, access_token)
        if session_response is not None:
            print_response(session_response)
        else:
            print("Invalid session token")

    elif command == "verify":
        verification_token = args.verification_token
        digital_twin_info = client.verify_digital_twin_email(verification_token)
        if digital_twin_info is not None:
            print_response({ "digitalTwin": digital_twin_info })

    elif command == "change-password":
        user_token = args.user_token
        new_password = args.new_password
        response = client.change_password(user_token, new_password)
        if response is not None:
            print(response)

    elif command == "change-password-of-user":
        digital_twin_id = args.digital_twin_id
        tenant_id = args.tenant_id
        new_password = args.new_password
        response = client.change_password_of_user(digital_twin_id, tenant_id, new_password)
        if response is not None:
            print(response)

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
            service_account = client_config.read_service_account()
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

        service_account = client_config.read_service_account()
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
        logger = logging.getLogger()
        if tenant and isinstance(tenant, Tenant):
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

    elif command == "create_application_with_agent_credentials":
        # example public key
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
            args.tenant_id,
            args.application_name,
            args.application_agent_name,
            args.application_agent_credentials_name,
            args.public_key_type,
            public_key=public_key_encoded,
            expire_time=None)
        if create_application_with_agent_credentials_response:
            print_response(create_application_with_agent_credentials_response["response_application"])
            print_response(create_application_with_agent_credentials_response["response_application_agent"])
            print_credential(create_application_with_agent_credentials_response["response_application_agent_credentials"])
        else:
            print("Invalid create_application_with_agent_credentials_response")
        return create_application_with_agent_credentials_response

    elif command == "service_account_id":
        service_account_id = args.service_account_id
        service_account = client_config.read_service_account(service_account_id)
        if service_account:
            print_response(service_account)
        else:
            print("Invalid service account")

    elif command == "service_account_name":
        customer_id = args.customer_id
        service_account_name = args.service_account_name
        service_account = client_config.read_service_account_by_name(customer_id, service_account_name)
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
        service_account_credential = client_config.read_service_account_credential(service_account_credential_id)
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
        pem = None
        t = datetime.now().timestamp()
        expire_time_in_seconds = int(t) + 2678400 # now + one month example
        service_account_credential_response = client_config.register_service_account_credential_pem(service_account_id,
                                                                                             display_name, pem,
                                                                                             expire_time_in_seconds,
                                                                                             [])
        if service_account_credential_response:
            print_credential(service_account_credential_response)
        else:
            print("Invalid service account response")
        return service_account_credential_response

    elif command == "delete_service_account_credential":
        service_account_credential_id = args.service_account_credential_id
        if args.etag:
            etag = args.etag
        else:
            etag = None

        delete_service_account_credential_response = client_config.delete_service_account_credential(
            service_account_credential_id,
            etag,
            []
        )
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

        default_from_address_address=os.getenv('INDYKITE_DEFAULT_FROM')
        default_from_address_name="Test Config"

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
        config_node = client_config.read_config_node(config_node_id, [])
        if config_node:
            print_response(config_node)
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

    elif command == "create_webauthn_provider_config_node":
        location = args.app_space_id
        name = args.name
        display_name = args.display_name
        description = args.description

        webauthn_provider_config = WebAuthnProviderConfig(
            relying_parties={"http://localhost":"localhost"},
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
            print_response(create_webauthn_provider_config_node_response)
        else:
            print("Invalid create webauthn provider config node response")
        return create_webauthn_provider_config_node_response

    elif command == "update_webauthn_provider_config_node":
        config_node_id = args.config_node_id
        etag = args.etag
        display_name = args.display_name
        description = args.description

        webauthn_provider_config = WebAuthnProviderConfig(
            relying_parties={"http://localhost":"localhost"},
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
            [])

        if update_webauthn_provider_config_node_response:
            print_response(update_webauthn_provider_config_node_response)
        else:
            print("Invalid update webauthn provider config node response")
        return update_webauthn_provider_config_node_response

    elif command == "create_authorization_policy_config_node":
        location = args.app_space_id
        name = args.name
        display_name = args.display_name
        description = args.description

        with open("utils/sdk_policy_config.json") as f:
            file_data = f.read()
        policy_dict = json.loads(file_data)
        policy_dict = json.dumps(policy_dict)
        policy_config = AuthorizationPolicyConfig(
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
            []
        )

        if create_authorization_policy_config_node_response:
            print_response(create_authorization_policy_config_node_response)
        else:
            print("Invalid create authorization policy config node response")
        return create_authorization_policy_config_node_response

    elif command == "update_authorization_policy_config_node":
        config_node_id = args.config_node_id
        etag = args.etag
        display_name = args.display_name
        description = args.description

        with open("utils/sdk_policy_config.json") as f:
            file_data = f.read()
        policy_dict = json.loads(file_data)
        policy_dict = json.dumps(policy_dict)

        policy_config = AuthorizationPolicyConfig(
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
            []
        )
        if update_authorization_policy_config_node_response:
            print_response(update_authorization_policy_config_node_response)
        else:
            print("Invalid update authorization policy config node response")
        return update_authorization_policy_config_node_response

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
            tenant_id=args.tenant_id,
            kind="DIGITAL_TWIN_KIND_PERSON",
            state="DIGITAL_TWIN_STATE_ACTIVE",
            password=PasswordCredential(
                email=EmailIdentity(
                    email="test2208@example.com",
                    verified=True
                ),
                value="password"
            )
        ),
            ImportDigitalTwin(
                tenant_id=args.tenant_id,
                kind="DIGITAL_TWIN_KIND_PERSON",
                state="DIGITAL_TWIN_STATE_ACTIVE",
                password=PasswordCredential(
                    email=EmailIdentity(
                        email="test2209@example.com",
                        verified=True
                    ),
                    value="password"
                )
            ),
            ImportDigitalTwin(
                tenant_id=args.tenant_id,
                kind="DIGITAL_TWIN_KIND_PERSON",
                state="DIGITAL_TWIN_STATE_ACTIVE",
                password=PasswordCredential(
                    email=EmailIdentity(
                        email="test2210@example.com",
                        verified=True
                    ),
                    value="password"
                )
            )
        ]
        hash_algorithm = None

        import_digital_twins_config_response = client.import_digital_twins(
            entities, hash_algorithm)
        if import_digital_twins_config_response:
            for response in import_digital_twins_config_response:
                print_response(response)
        else:
            print("Invalid import digital twins response")
        return import_digital_twins_config_response

    elif command == "import_digital_twins_hash":

        password = 'passwordabc'
        hash_dict = encrypt_bcrypt(password)
        for key in hash_dict:
            salt = key
            hash_password = hash_dict[key]

        entities = [ImportDigitalTwin(
            tenant_id=args.tenant_id,
            kind="DIGITAL_TWIN_KIND_PERSON",
            state="DIGITAL_TWIN_STATE_ACTIVE",
            password=PasswordCredential(
                email=EmailIdentity(
                    email="test2002@example.com",
                    verified=True
                ),
                hash=PasswordHash(password_hash=hash_password,salt=salt)
            )
        )]
        hash_algorithm = {"bcrypt": {}}

        import_digital_twins_config_response = client.import_digital_twins(
            entities, hash_algorithm)
        if import_digital_twins_config_response:
            for response in import_digital_twins_config_response:
                print_response(response)
        else:
            print("Invalid import digital twins response")
        return import_digital_twins_config_response

    elif command == "import_digital_twins_hash_sha":
        entities = [ImportDigitalTwin(
            tenant_id=args.tenant_id,
            kind="DIGITAL_TWIN_KIND_PERSON",
            state="DIGITAL_TWIN_STATE_ACTIVE",
            password=PasswordCredential(
                email=EmailIdentity(
                    email="test2002@example.com",
                    verified=True
                ),
                hash=PasswordHash(password_hash=args.hash_password)
            )
        )]
        hash_algorithm = {"sha256": SHA256(rounds=14)}

        import_digital_twins_config_response = client.import_digital_twins(
            entities, hash_algorithm)
        if import_digital_twins_config_response:
            for response in import_digital_twins_config_response:
                print_response(response)
        else:
            print("Invalid import digital twins response")
        return import_digital_twins_config_response

    elif command == "import_digital_twins_update":
        entities = [ImportDigitalTwin(
            id=args.id,
            tenant_id=args.tenant_id,
            kind="DIGITAL_TWIN_KIND_PERSON",
            state="DIGITAL_TWIN_STATE_ACTIVE",
            password=PasswordCredential(
                email=EmailIdentity(
                    email="test2003@example.com",
                    verified=True
                ),
                value="password"
            )
        )]
        hash_algorithm = None

        import_digital_twins_config_response = client.import_digital_twins(
            entities, hash_algorithm)
        if import_digital_twins_config_response:
            for response in import_digital_twins_config_response:
                print_response(response)
        else:
            print("Invalid import digital twins response")
        return import_digital_twins_config_response

    elif command == "is_authorized_dt":
        digital_twin_id = args.digital_twin_id
        tenant_id = args.tenant_id
        actions = ["ACTION1", "ACTION2"]
        resources = [IsAuthorizedResource("resourceID", "TypeName", actions),
                     IsAuthorizedResource("resource2ID", "TypeName", actions)]
        input_params = {"age": "21"}
        policy_tags = ["Car", "Rental", "Sharing"]
        is_authorized = client_authorization.is_authorized_digital_twin(
            digital_twin_id,
            tenant_id,
            resources,
            input_params,
            policy_tags)

        if is_authorized:
            print_response(is_authorized)
        else:
            print("Invalid is_authorized")
        return is_authorized

    elif command == "is_authorized_token":
        access_token = args.access_token
        actions = ["ACTION1", "ACTION2"]
        resources = [IsAuthorizedResource("resourceID", "TypeName", actions),
                     IsAuthorizedResource("resource2ID", "TypeName", actions)]
        input_params = {}
        is_authorized = client_authorization.is_authorized_token(access_token, resources, input_params, [])
        if is_authorized:
            print_response(is_authorized)
        else:
            print("Invalid is_authorized")
        return is_authorized

    elif command == "is_authorized_property":
        property_type = args.property_type #e.g "email"
        property_value = args.property_value #e.g test@example.com
        actions = ["ACTION1", "ACTION2"]
        resources = [IsAuthorizedResource("resourceID", "TypeName", actions),
                     IsAuthorizedResource("resource2ID", "TypeName", actions)]
        input_params = {"age":"21"}
        is_authorized = client_authorization.is_authorized_property_filter(
            property_type,
            property_value,
            resources,
            input_params,
            [])
        if is_authorized:
            print_response(is_authorized)
        else:
            print("Invalid is_authorized")
        return is_authorized

    elif command == "what_authorized_dt":
        digital_twin_id = args.digital_twin_id
        tenant_id = args.tenant_id
        actions = ["ACTION1", "ACTION2"]
        resource_types = [WhatAuthorizedResourceTypes("TypeName", actions),
                          WhatAuthorizedResourceTypes("TypeNameSecond", actions)]
        input_params = {"age": "21"}
        policy_tags = ["Car", "Rental", "Sharing"]
        what_authorized = client_authorization.what_authorized_digital_twin(
            digital_twin_id,
            tenant_id,
            resource_types,
            input_params,
            policy_tags)

        if what_authorized:
            print_response(what_authorized)
        else:
            print("Invalid what_authorized")
        return what_authorized

    elif command == "what_authorized_token":
        access_token = args.access_token
        actions = ["ACTION1", "ACTION2"]
        resource_types = [WhatAuthorizedResourceTypes("TypeName", actions),
                          WhatAuthorizedResourceTypes("TypeNameSecond", actions)]
        input_params = {}
        what_authorized = client_authorization.what_authorized_token(access_token, resource_types, input_params, [])
        if what_authorized:
            print_response(what_authorized)
        else:
            print("Invalid what_authorized")
        return what_authorized

    elif command == "what_authorized_property":
        property_type = args.property_type #e.g "email"
        property_value = args.property_value #e.g test@example.com
        actions = ["ACTION1", "ACTION2"]
        resource_types = [WhatAuthorizedResourceTypes("TypeName", actions),
                          WhatAuthorizedResourceTypes("TypeNameSecond", actions)]
        input_params = {"age":"21"}
        what_authorized = client_authorization.what_authorized_property_filter(
            property_type,
            property_value,
            resource_types,
            input_params,
            [])
        if what_authorized:
            print_response(what_authorized)
        else:
            print("Invalid what_authorized")
        return what_authorized

    elif command == "who_authorized":
        actions = ["HAS_FREE_PARKING"]
        resources = [WhoAuthorizedResource("parking-lot-id1", "ParkingLot", actions)]
        input_params = {}
        policy_tags = []
        who_authorized = client_authorization.who_authorized(
            resources,
            input_params,
            policy_tags)

        if who_authorized:
            print_response(who_authorized)
        else:
            print("Invalid who_authorized")
        return who_authorized

    elif command == "create_consent":
        pii_processor_id = args.pii_processor_id
        pii_principal_id = args.pii_principal_id
        properties = ["icecream"]
        consent_response = client.create_consent(pii_processor_id, pii_principal_id, properties)
        if consent_response:
            print_response(consent_response)
        else:
            print("Invalid consent response")
        return consent_response

    elif command == "list_consents":
        pii_principal_id = args.pii_principal_id
        consent_response = client.list_consents(pii_principal_id)
        if consent_response:
            for c in consent_response:
                print_response(c)
        else:
            print("Invalid consent response")
        return consent_response

    elif command == "revoke_consent":
        pii_principal_id = args.pii_principal_id
        consent_ids = args.consent_ids
        consent_response = client.revoke_consent(pii_principal_id, consent_ids)
        if consent_response:
            print_response(consent_response)
        else:
            print("Invalid consent response")
        return consent_response

    elif command == "check_oauth2_consent_challenge":
        challenge = args.challenge
        consent_response = client.check_oauth2_consent_challenge(challenge)
        if consent_response:
            print_response(consent_response)
        else:
            print("Invalid consent response")
        return consent_response

    elif command == "create_oauth2_consent_verifier_approval":
        consent_challenge = args.consent_challenge
        grant_scopes = ["openid", "email", "profile"]
        granted_audiences = []
        # custom claims for jwk (map values to enrich token)
        access_token = json.loads(args.access_token)
        consent_response = client.create_oauth2_consent_verifier_approval(consent_challenge, grant_scopes,
                                                                          granted_audiences, access_token, {}, {},
                                                                          False, None)
        if consent_response:
            print_response(consent_response)
        else:
            print("Invalid consent response")
        return consent_response

    elif command == "create_oauth2_consent_verifier_denial":
        consent_challenge = args.consent_challenge
        error = "access_denied"
        error_description = "Access is denied"
        error_hint = "Your consent challenge may be not valid: check your OAuth2 host and your clientID"
        status_code = 403
        consent_response = client.create_oauth2_consent_verifier_denial(consent_challenge, error,
                                                                        error_description,
                                                                        error_hint, status_code)
        if consent_response:
            print_response(consent_response)
        else:
            print("Invalid consent response")
        return consent_response

    elif command == "start_forgotten_password":
        digital_twin_id = args.digital_twin_id
        tenant_id = args.tenant_id
        forgotten_response = client.start_forgotten_password_flow(digital_twin_id, tenant_id)
        if forgotten_response is not None:
            print(forgotten_response)
        else:
            print("Invalid forgotten password response")

    elif command == "create_email_invitation":
        reference_id = str(uuid.uuid4())
        # any unique external reference id
        print(reference_id)
        tenant_id = args.tenant_id
        email = args.email
        invitation_response = client.create_email_invitation(tenant_id, reference_id, email, invite_at_time=None,
                                                             expire_time=None, message_attributes=None)
        if invitation_response is not None:
            print(invitation_response)
        else:
            print("Invalid invitation response")

    elif command == "create_email_invitation_with_date":
        reference_id = str(uuid.uuid4())
        print(reference_id)
        tenant_id = args.tenant_id
        email = args.email
        t = datetime.now().timestamp()
        invite_at_time_in_seconds = int(t) + 3600
        expire_time_in_seconds = invite_at_time_in_seconds + 172800 # now + 2 days example
        message_attributes = {"attr1": "value1"}
        invitation_response = client.create_email_invitation(tenant_id, reference_id, email,
                                                             invite_at_time_in_seconds,
                                                             expire_time_in_seconds,
                                                             message_attributes)
        if invitation_response is not None:
            print(invitation_response)
        else:
            print("Invalid invitation response")

    elif command == "check_invitation_state":
        reference_id = args.reference_id
        # check with either reference_id or invitation_token
        invitation_response = client.check_invitation_state(reference_id, None)
        if invitation_response is not None:
            print_response(invitation_response)
        else:
            print("Invalid invitation response")

    elif command == "resend_invitation":
        reference_id = args.reference_id
        invitation_response = client.resend_invitation(reference_id)
        if invitation_response is not None:
            print(invitation_response)
        else:
            print("Invalid invitation response")

    elif command == "cancel_invitation":
        reference_id = args.reference_id
        invitation_response = client.cancel_invitation(reference_id)
        if invitation_response is not None:
            print(invitation_response)
        else:
            print("Invalid invitation response")

    elif command == "register_digital_twin_without_credential":
        tenant_id = args.tenant_id
        properties = []
        definition1 = attributes.PropertyDefinition(
                property="extid"
            )
        property1 = helper.create_property(definition1, None, "44")
        properties.append(property1)
        register_response = client.register_digital_twin_without_credential(
            tenant_id,
            1,
            [],
            properties,
            [])
        if register_response is not None:
            print_response(register_response)
        else:
            print("Invalid invitation response")

    elif command == "get_http_client":
        token = None

        # generate an authenticated http client and generate a bearer token from the provided credentials
        client_http = HttpClient()
        response_http = client_http.get_http_client(token)
        credentials = client_http.get_credentials()
        # call get_refreshable_token_source again to check the token is the same
        response_source = client_http.get_refreshable_token_source(response_http.token_source, credentials)
        # call get_http_client again to generate another http client and check if the token is the same
        response_http2 = client_http.get_http_client(response_http.token_source)
        access_token = response_http2.get_token()
        # make a Knowledge API query
        endpoint = args.base_url
        data = {"query":"query ExampleQuery { identityProperties { id }}","variables":{},"operationName":"ExampleQuery"}
        headers = {"Authorization": "Bearer "+access_token,
                   'Content-Type': 'application/json'}
        response_post = requests.post(endpoint, json=data, headers=headers)
        print(response_http2.token_source.token.access_token)
        if response_post.text is not None:
            print_response(response_post.text)

    elif command == "get_refreshable_token_source":
        token_source = None
        client_http = HttpClient()
        credentials = client_http.get_credentials()
        response = client_http.get_refreshable_token_source(token_source, credentials)
        access_token_bytes = response.token.access_token

    elif command == "ingest_record_digital_twin":
        record_id = "745898"
        external_id = "external-dt-id3"
        kind = "DIGITAL_TWIN_KIND_PERSON"
        tenant_id = "gid:AAAAA9Q51FULGECVrvbfN0kUbSk"
        type = "CarOwner"
        identity_property = client_ingest.identity_property("customIdProp", "456")
        identity_properties = [identity_property]
        ingest_property = client_ingest.ingest_property("customProp", "741")
        properties = [ingest_property]
        upsert = client_ingest.upsert_data_node_digital_twin(
                                      external_id,
                                      type,
                                      [],
                                      tenant_id,
                                      identity_properties,
                                      properties)
        ingest_record_digital_twin = client_ingest.ingest_record_upsert(record_id, upsert)
        if ingest_record_digital_twin:
            print_response(ingest_record_digital_twin)
        else:
            print("Invalid upsert")
        return ingest_record_digital_twin

    elif command == "ingest_record_resource":
        record_id = "745899"
        external_id = "lot-1"
        type = "ParkingLot"
        ingest_property = client_ingest.ingest_property("customProp", "9654")
        properties = [ingest_property]
        upsert = client_ingest.upsert_data_node_resource(
                                      external_id,
                                      type,
                                      [],
                                      properties)
        ingest_record_resource = client_ingest.ingest_record_upsert(record_id, upsert)
        if ingest_record_resource:
            print_response(ingest_record_resource)
        else:
            print("Invalid upsert")
        return ingest_record_resource

    elif command == "ingest_record_relation":
        record_id = "745890"
        type = "CAN_USE"
        source_match = client_ingest.node_match("vehicle-1", "Vehicle")
        target_match = client_ingest.node_match("lot-1", "ParkingLot")
        match = client_ingest.relation_match(source_match, target_match, type)
        ingest_property = client_ingest.ingest_property("customProp", "8742")
        properties = [ingest_property]
        upsert = client_ingest.upsert_data_relation(
                                      match,
                                      properties)
        ingest_record_relation = client_ingest.ingest_record_upsert(record_id, upsert)
        if ingest_record_relation:
            print_response(ingest_record_relation)
        else:
            print("Invalid upsert")
        return ingest_record_relation

    elif command == "delete_record_node":
        record_id = "745890"
        node = client_ingest.node_match("vehicle-1", "Vehicle")
        delete = client_ingest.delete_data_node(node)
        delete_record_node = client_ingest.ingest_record_delete(id=record_id, delete=delete)
        if delete_record_node:
            print_response(delete_record_node)
        else:
            print("Invalid delete")
        return delete_record_node

    elif command == "delete_record_relation":
        record_id = "745890"
        type = "CAN_USE"
        source_match = client_ingest.node_match("vehicle-1", "Vehicle")
        target_match = client_ingest.node_match("lot-1", "ParkingLot")
        relation = client_ingest.relation_match(source_match, target_match, type)
        delete = client_ingest.delete_data_relation(relation)
        delete_record_relation = client_ingest.ingest_record_delete(id=record_id, delete=delete)
        if delete_record_relation:
            print_response(delete_record_relation)
        else:
            print("Invalid delete")
        return delete_record_relation

    elif command == "delete_record_node_property":
        record_id = "745890"
        match = client_ingest.node_match("vehicle-1", "Vehicle")
        key = "nodePropertyName"
        node_property = client_ingest.node_property_match(match, key)
        delete = client_ingest.delete_data_node_property(node_property)
        delete_record_node_property = client_ingest.ingest_record_delete(id=record_id, delete=delete)
        if delete_record_node_property:
            print_response(delete_record_node_property)
        else:
            print("Invalid delete")
        return delete_record_node_property

    elif command == "delete_record_relation_property":
        record_id = "745890"
        type = "CAN_USE"
        source_match = client_ingest.node_match("vehicle-1", "Vehicle")
        target_match = client_ingest.node_match("lot-1", "ParkingLot")
        match = client_ingest.relation_match(source_match, target_match, type)
        key = "relationPropertyName"
        relation_property = client_ingest.relation_property_match(match, key)
        delete = client_ingest.delete_data_relation_property(relation_property)
        delete_record_relation_property = client_ingest.ingest_record_delete(id=record_id,
                                                                                delete=delete)
        if delete_record_relation_property:
            print_response(delete_record_relation_property)
        else:
            print("Invalid delete")
        return delete_record_relation_property

    elif command == "stream_records":
        record_id = "145898"
        external_id = "external-dt-id1"
        tenant_id = "gid:AAAAA9Q51FULGECVrvbfN0kUbSk"
        type = "Person"
        upsert = client_ingest.upsert_data_node_digital_twin(
            external_id,
            type,
            [],
            tenant_id,
            [],
            [])
        record = client_ingest.record_upsert(record_id, upsert)

        record_id2 = "145899"
        external_id = "lot-1"
        type = "ParkingLot"
        ingest_property = client_ingest.ingest_property("customProp", "9654")
        properties = [ingest_property]
        upsert2 = client_ingest.upsert_data_node_resource(
            external_id,
            type,
            [],
            properties)
        record2 = client_ingest.record_upsert(record_id2, upsert2)
        responses = client_ingest.stream_records([record, record2])
        if responses:
            for response in responses:
                print_response(response)
        else:
            print("Invalid ingestion")
        return response


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
