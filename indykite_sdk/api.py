"""
Commandline interface for making an API request with the SDK.
"""
import argparse
import json
import uuid
import time
import requests
import os
from datetime import datetime
from google.protobuf.duration_pb2 import Duration
import logging
from indykite_sdk.identity import IdentityClient
from indykite_sdk.config import ConfigClient
from indykite_sdk.authorization import AuthorizationClient
from indykite_sdk.oauth2 import HttpClient
from indykite_sdk.indykite.config.v1beta1.model_pb2 import (SendGridProviderConfig, MailJetProviderConfig,
                                                            AmazonSESProviderConfig, MailgunProviderConfig)
from indykite_sdk.indykite.config.v1beta1.model_pb2 import (EmailServiceConfig, AuthFlowConfig, OAuth2ClientConfig,
                                                            WebAuthnProviderConfig, AuthorizationPolicyConfig)
from indykite_sdk.indykite.config.v1beta1.model_pb2 import OAuth2ProviderConfig, OAuth2ApplicationConfig, \
    UniquePropertyConstraint, UsernamePolicy
from indykite_sdk.indykite.config.v1beta1.model_pb2 import EmailAttachment, Email, EmailMessage, EmailTemplate, \
    EmailDefinition
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from indykite_sdk.indykite.knowledge.v1beta2.model_pb2 import Return as ReturnKnowledge
from indykite_sdk.model.is_authorized import IsAuthorizedResource
from indykite_sdk.model.what_authorized import WhatAuthorizedResourceTypes
from indykite_sdk.model.who_authorized import WhoAuthorizedResource
from indykite_sdk.model.tenant import Tenant
from indykite_sdk.ingest import IngestClient
from indykite_sdk.knowledge import KnowledgeClient
from indykite_sdk.model.identity_knowledge import Node as NodeModel, Metadata
from indykite_sdk.utils import credentials_config
from indykite_sdk.utils.message_to_value import param_to_value
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
    # INTROSPECT
    introspect_parser = subparsers.add_parser("introspect")
    introspect_parser.add_argument("user_token", help="JWT bearer token")

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

    # customer_name_token
    customer_name_token_parser = subparsers.add_parser("customer_name_token")
    customer_name_token_parser.add_argument("customer_name", help="Customer name (not display name)")

    # read_customer_config
    read_customer_config_parser = subparsers.add_parser("read_customer_config")
    read_customer_config_parser.add_argument("customer_id", help="Customer gid id")

    # update_customer_config
    update_customer_config_parser = subparsers.add_parser("update_customer_config")
    update_customer_config_parser.add_argument("customer_id", help="Customer gid id")
    update_customer_config_parser.add_argument("etag", help="Etag")
    update_customer_config_parser.add_argument("default_auth_flow_id", help="Default auth flow gid id")

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

    # read_app_space_config
    read_app_space_config_parser = subparsers.add_parser("read_app_space_config")
    read_app_space_config_parser.add_argument("app_space_id", help="AppSpace gid id")

    # update_app_space_config
    update_app_space_config_parser = subparsers.add_parser("update_app_space_config")
    update_app_space_config_parser.add_argument("app_space_id", help="AppSpace gid id")
    update_app_space_config_parser.add_argument("etag", help="Etag")
    update_app_space_config_parser.add_argument("tenant_id", help="Tenant default gid id")
    update_app_space_config_parser.add_argument("default_auth_flow_id", help="Default auth flow gid id")

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

    # read_tenant_config
    read_tenant_config_parser = subparsers.add_parser("read_tenant_config")
    read_tenant_config_parser.add_argument("tenant_id", help="Tenant gid id")

    # update_tenant_config
    update_tenant_config_parser = subparsers.add_parser("update_tenant_config")
    update_tenant_config_parser.add_argument("tenant_id", help="Tenant gid id")
    update_tenant_config_parser.add_argument("etag", help="Etag")
    update_tenant_config_parser.add_argument("default_auth_flow_id", help="Default auth flow gid id")

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
    register_application_agent_credential_jwk_parser.add_argument("default_tenant_id", help="Default tenant id")

    # register_application_agent_credential_pem
    register_application_agent_credential_pem_parser = subparsers.add_parser(
        "register_application_agent_credential_pem")
    register_application_agent_credential_pem_parser.add_argument("application_agent_id",
                                                                  help="Application agent credential id")
    register_application_agent_credential_pem_parser.add_argument("display_name", help="Display name")
    register_application_agent_credential_pem_parser.add_argument("default_tenant_id", help="Default tenant id")

    # delete_application_agent_credential
    delete_application_agent_credential_parser = subparsers.add_parser("delete_application_agent_credential")
    delete_application_agent_credential_parser.add_argument("application_agent_credential_id",
                                                            help="Application agent credential id")
    delete_application_agent_credential_parser.add_argument("etag", help="Etag")

    # create_application_with_agent_credentials
    create_application_with_agent_credentials_parser = subparsers.add_parser(
        "create_application_with_agent_credentials")
    create_application_with_agent_credentials_parser.add_argument("app_space_id", help="AppSpace Id (gid)")
    create_application_with_agent_credentials_parser.add_argument("tenant_id", help="Tenant Id (gid)")
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
    update_oauth2_application_parser.add_argument("oauth2_application_id",
                                                  help="OAuth2 application id (gid)")
    update_oauth2_application_parser.add_argument("etag", help="Etag")
    update_oauth2_application_parser.add_argument("display_name", help="Display name")
    update_oauth2_application_parser.add_argument("description", help="Description")

    # delete_oauth2_application
    delete_oauth2_application_parser = subparsers.add_parser("delete_oauth2_application")
    delete_oauth2_application_parser.add_argument("oauth2_application_id",
                                                  help="OAuth2 application id (gid)")
    delete_oauth2_application_parser.add_argument("etag", help="Etag")

    # is_authorized_identity_node
    is_authorized_identity_node_parser = subparsers.add_parser("is_authorized_identity_node")
    is_authorized_identity_node_parser.add_argument("identity_node_id",
                                         help="Identity node gid (node with is_identity equal True)")

    # is_authorized_token
    is_authorized_token_parser = subparsers.add_parser("is_authorized_token")
    is_authorized_token_parser.add_argument("access_token")

    # is_authorized_property
    is_authorized_property_parser = subparsers.add_parser("is_authorized_property")
    is_authorized_property_parser.add_argument("property_type", help="Identity node Identity Property")
    is_authorized_property_parser.add_argument("property_value",
                                               help="Identity node Identity Property value")

    # is_authorized_external_id
    is_authorized_external_id_parser = subparsers.add_parser("is_authorized_external_id")
    is_authorized_external_id_parser.add_argument("type", help="Identity node type")
    is_authorized_external_id_parser.add_argument("external_id", help="Identity node external id")

    # what_authorized_identity_node
    what_authorized_identity_node_parser = subparsers.add_parser("what_authorized_identity_node")
    what_authorized_identity_node_parser.add_argument("identity_node_id",
                                           help="Identity node gid (node with is_identity equal True)")

    # what_authorized_token
    what_authorized_token_parser = subparsers.add_parser("what_authorized_token")
    what_authorized_token_parser.add_argument("access_token")

    # what_authorized_property
    what_authorized_property_parser = subparsers.add_parser("what_authorized_property")
    what_authorized_property_parser.add_argument("property_type", help="Identity node Identity Property")
    what_authorized_property_parser.add_argument("property_value",
                                                 help="Identity node Identity Property value")

    # what_authorized_external_id
    what_authorized_external_id_parser = subparsers.add_parser("what_authorized_external_id")
    what_authorized_external_id_parser.add_argument("node_type", help="Identity node node type")
    what_authorized_external_id_parser.add_argument("external_id", help="Identity node external_id")

    # who_authorized
    who_authorized_parser = subparsers.add_parser("who_authorized")

    # create_consent
    create_consent_parser = subparsers.add_parser("create_consent")
    create_consent_parser.add_argument("pii_processor_id", help="ID of OAuth2 Application")
    create_consent_parser.add_argument("pii_principal_id",
                                       help="Identity node gid (node with is_identity equal True)")

    # list_consents
    list_consents_parser = subparsers.add_parser("list_consents")
    list_consents_parser.add_argument("pii_principal_id",
                                      help="Identity node gid (node with is_identity equal True)")

    # revoke_consent
    revoke_consent_parser = subparsers.add_parser("revoke_consent")
    revoke_consent_parser.add_argument("pii_principal_id",
                                       help="Identity node gid (node with is_identity equal True)")
    revoke_consent_parser.add_argument("consent_ids", nargs='*',
                                       help="List of consent ids separated by space")

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

    # get_http_client
    get_http_client = subparsers.add_parser("get_http_client")
    get_http_client.add_argument("base_url", help="knowledge endpoint")

    # get_refreshable_token_source
    get_refreshable_token_source = subparsers.add_parser("get_refreshable_token_source")

    # ingest
    ingest_record_identity_node_parser = subparsers.add_parser("ingest_record_identity_node")
    ingest_record_resource_parser = subparsers.add_parser("ingest_record_resource")
    ingest_record_relation_parser = subparsers.add_parser("ingest_record_relation")
    delete_record_relation_property_parser = subparsers.add_parser("delete_record_relation_property")
    delete_record_node_property_parser = subparsers.add_parser("delete_record_node_property")
    delete_record_relation_parser = subparsers.add_parser("delete_record_relation")
    delete_record_node_parser = subparsers.add_parser("delete_record_node")
    stream_records_parser = subparsers.add_parser("stream_records")
    edges_parser = subparsers.add_parser("edges")

    # knowledge
    read_identity_knowledge_parser = subparsers.add_parser("read_identity_knowledge")

    get_identity_by_id_parser = subparsers.add_parser("get_identity_by_id")
    get_identity_by_id_parser.add_argument("id",
                                           help="Identity node gid (node with is_identity equal True)")

    get_identity_by_identifier_parser = subparsers.add_parser("get_identity_by_identifier")
    get_identity_by_identifier_parser.add_argument("external_id", help="Identity node external id")
    get_identity_by_identifier_parser.add_argument("type", help="Identity node type")

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
    client = IdentityClient()
    client_config = ConfigClient()
    client_authorization = AuthorizationClient()
    client_ingest = IngestClient()
    client_knowledge = KnowledgeClient()

    command = args.command

    if command == "introspect":
        # token_introspect method: to get info on a user token
        user_token = args.user_token
        token_info = client.token_introspect(user_token)
        if token_info is not None:
            api_helper.print_response(token_info)
        else:
            print("Invalid token")

    elif command == "enrich-token":
        # enrich_token method: to allow a session and an access token to be enriched with additional data
        # with user token (access token) and token claims (dict) and session claims (dict) as arguments
        user_token = args.user_token
        token_claims = args.token_claims
        session_claims = args.session_claims
        response = client.enrich_token(user_token, token_claims, session_claims)
        if response is not None:
            print("Successfully enriched token")
        else:
            print("Invalid token")

    elif command == "create_consent":
        # create_consent method: to create a consent to an application (pii_processor_id ID in GID format)
        # given by an identity node (pii_principal_id ID in GID format)
        pii_processor_id = args.pii_processor_id
        pii_principal_id = args.pii_principal_id
        properties = ["icecream"]
        consent_response = client.create_consent(pii_processor_id, pii_principal_id, properties)
        if consent_response:
            api_helper.print_response(consent_response)
        else:
            print("Invalid consent response")
        return consent_response

    elif command == "list_consents":
        # list_consents method: to list the consents given by an identity node (pii_principal_id ID in GID format)
        pii_principal_id = args.pii_principal_id
        consent_response = client.list_consents(pii_principal_id)
        if consent_response:
            for c in consent_response:
                api_helper.print_response(c)
        else:
            print("Invalid consent response")
        return consent_response

    elif command == "revoke_consent":
        # revoke_consent method: to revoke list of consents (IDs in GID format)
        # given by an identity node (pii_principal_id ID in GID format)
        pii_principal_id = args.pii_principal_id
        consent_ids = args.consent_ids
        consent_response = client.revoke_consent(pii_principal_id, consent_ids)
        if consent_response:
            api_helper.print_response(consent_response)
        else:
            print("Invalid consent response")
        return consent_response

    elif command == "check_oauth2_consent_challenge":
        # check_oauth2_consent_challenge method: read the Consent Challenge from DB
        # with the code challenge as an argument
        challenge = args.challenge
        consent_response = client.check_oauth2_consent_challenge(challenge)
        if consent_response:
            api_helper.print_response(consent_response)
        else:
            print("Invalid consent response")
        return consent_response

    elif command == "create_oauth2_consent_verifier_approval":
        # create_oauth2_consent_verifier_approval method: to create a new ConsentApproval verifier
        consent_challenge = args.consent_challenge
        grant_scopes = ["openid", "email", "profile"]
        granted_audiences = []
        # custom claims for jwk (map values to enrich token)
        access_token = json.loads(args.access_token)
        consent_response = client.create_oauth2_consent_verifier_approval(
            consent_challenge,
            grant_scopes,
            granted_audiences,
            access_token,
            {},
            {},
            False,
            None
        )
        if consent_response:
            api_helper.print_response(consent_response)
        else:
            print("Invalid consent response")
        return consent_response

    elif command == "create_oauth2_consent_verifier_denial":
        # create_oauth2_consent_verifier_denial method: to create a new DenialResponse verifier
        consent_challenge = args.consent_challenge
        error = "access_denied"
        error_description = "Access is denied"
        error_hint = "Your consent challenge may be not valid: check your OAuth2 host and your clientID"
        status_code = 403
        consent_response = client.create_oauth2_consent_verifier_denial(
            consent_challenge, error,
            error_description,
            error_hint,
            status_code
        )
        if consent_response:
            api_helper.print_response(consent_response)
        else:
            print("Invalid consent response")
        return consent_response

    elif command == "create_email_invitation":
        # create_email_invitation method: to create an invitation email
        # with reference id, tenant GID id and recipient email as arguments
        reference_id = str(uuid.uuid4())
        # any unique external reference id
        print(reference_id)
        tenant_id = args.tenant_id
        email = args.email
        invitation_response = client.create_email_invitation(
            tenant_id,
            reference_id,
            email,
            invite_at_time=None,
            expire_time=None,
            message_attributes=None
        )
        if invitation_response is not None:
            print(invitation_response)
        else:
            print("Invalid invitation response")

    elif command == "create_email_invitation_with_date":
        # create_email_invitation method: to create an invitation email
        # with reference id, tenant GID id, recipient email, invitation date, expiration and
        # message attributes (attributes passed into message sender)  as arguments
        reference_id = str(uuid.uuid4())
        print(reference_id)
        tenant_id = args.tenant_id
        email = args.email
        t = datetime.now().timestamp()
        invite_at_time_in_seconds = int(t) + 3600
        expire_time_in_seconds = invite_at_time_in_seconds + 172800  # now + 2 days example
        message_attributes = {"attr1": "value1"}
        invitation_response = client.create_email_invitation(
            tenant_id,
            reference_id,
            email,
            invite_at_time_in_seconds,
            expire_time_in_seconds,
            message_attributes
        )
        if invitation_response is not None:
            print(invitation_response)
        else:
            print("Invalid invitation response")

    elif command == "check_invitation_state":
        # check_invitation_state method: to return the state of invitation and its data
        reference_id = args.reference_id
        # check with either reference_id or invitation_token
        invitation_response = client.check_invitation_state(reference_id, None)
        if invitation_response is not None:
            api_helper.print_response(invitation_response)
        else:
            print("Invalid invitation response")

    elif command == "resend_invitation":
        # resend_invitation method: expects reference ID of invitation to send email again
        reference_id = args.reference_id
        invitation_response = client.resend_invitation(reference_id)
        if invitation_response is not None:
            print(invitation_response)
        else:
            print("Invalid invitation response")

    elif command == "cancel_invitation":
        # cancel_invitation method: expects reference ID of invitation to cancel
        reference_id = args.reference_id
        invitation_response = client.cancel_invitation(reference_id)
        if invitation_response is not None:
            print(invitation_response)
        else:
            print("Invalid invitation response")

    elif command == "customer_id":
        # read_customer_by_id method: to get customer info from customer gid id
        # (extracted here from service account credentials)
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

    elif command == "customer_name":
        # read_customer_by_name method: to get customer info from customer name
        customer_name = args.customer_name
        customer = client_config.read_customer_by_name(customer_name)
        if customer:
            api_helper.print_response(customer)
        else:
            print("Invalid customer id")

    elif command == "customer_name_token":
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

    elif command == "read_customer_config":
        # read_customer_config method: to get customer config  info from customer gid id
        bookmark = []  # or value returned by last write operation
        customer_config = client_config.read_customer_config(args.customer_id, bookmark)
        if customer_config:
            api_helper.print_response(customer_config)
        else:
            print("None")

    elif command == "update_customer_config":
        customer_id = args.customer_id
        etag = args.etag
        default_auth_flow_id = args.default_auth_flow_id
        bookmark = []  # or value returned by last write operation
        customer_config = client_config.create_customer_config(default_auth_flow_id=default_auth_flow_id,
                                                               default_email_service_id=None)
        customer_config_response = client_config.update_customer_config(customer_id, etag, customer_config, bookmark)
        if customer_config_response:
            api_helper.print_response(customer_config_response)
        else:
            print("None")
        return customer_config_response

    elif command == "service_account":
        # read_service_account method: to get service account info from service account gid id
        # (extracted here from service account credentials)
        service_account = client_config.read_service_account()
        if service_account:
            api_helper.print_response(service_account)
        else:
            print("Invalid service account")

    elif command == "app_space_id":
        # read_app_space_by_id method: to get AppSpace info from AppSpace gid id
        app_space_id = args.app_space_id
        app_space = client_config.read_app_space_by_id(app_space_id)
        if app_space:
            api_helper.print_response(app_space)
        else:
            print("Invalid app_space id")

    elif command == "app_space_name":
        # read_app_space_by_name method: to get AppSpace info from AppSpace name and customer gid id
        app_space_name = args.app_space_name
        customer_id = args.customer_id
        app_space = client_config.read_app_space_by_name(customer_id, app_space_name)
        if app_space:
            api_helper.print_response(app_space)
        else:
            print("Invalid app_space name")

    elif command == "create_app_space":
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
        return app_space_response

    elif command == "update_app_space":
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
            for app_space in list_app_spaces_response:
                api_helper.print_response(app_space)
        else:
            print("Invalid list_app_spaces response")
        return list_app_spaces_response

    elif command == "delete_app_space":
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
        return delete_app_space_response

    elif command == "read_app_space_config":
        # read_app_space_config method: to get appSpace config  info from appSpace gid id
        bookmark = []  # or value returned by last write operation
        app_space_config = client_config.read_app_space_config(args.app_space_id, bookmark)
        if app_space_config:
            api_helper.print_response(app_space_config)
        else:
            print("None")

    elif command == "update_app_space_config":
        app_space_id = args.app_space_id
        etag = args.etag
        tenant_id = args.tenant_id
        default_auth_flow_id = args.default_auth_flow_id
        bookmark = []  # or value returned by last write operation
        app_space_config = client_config.create_app_space_config(
            default_tenant_id=tenant_id,
            default_auth_flow_id=default_auth_flow_id,
            default_email_service_id=None,
            unique_property_constraints={"constraint": client_config.unique_property_constraints(
                tenant_unique=True,
                canonicalization=["unicode", "case-insensitive"])},
            username_policy=client_config.username_policy(
                allowed_username_formats=["email", "mobile", "username"],
                valid_email=False,
                verify_email=False
            )
        )
        app_space_config_response = client_config.update_app_space_config(app_space_id, etag, app_space_config,
                                                                          bookmark)
        if app_space_config_response:
            api_helper.print_response(app_space_config_response)
        else:
            print("None")
        return app_space_config_response

    elif command == "tenant_id":
        tenant_id = args.tenant_id
        tenant = client_config.read_tenant_by_id(tenant_id)
        logger = logging.getLogger()
        if tenant and isinstance(tenant, Tenant):
            api_helper.print_response(tenant)
        else:
            print("Invalid tenant id")

    elif command == "tenant_name":
        tenant_name = args.tenant_name
        app_space_id = args.app_space_id
        tenant = client_config.read_tenant_by_name(app_space_id, tenant_name)
        if tenant:
            api_helper.print_response(tenant)
        else:
            print("Invalid tenant name")

    elif command == "create_tenant":
        tenant_name = args.tenant_name
        issuer_id = args.issuer_id
        display_name = args.display_name
        bookmark = []  # or value returned by last write operation
        tenant_response = client_config.create_tenant(issuer_id, tenant_name, display_name, "description", bookmark)
        if tenant_response:
            api_helper.print_response(tenant_response)
        else:
            print("Invalid tenant response")
        return tenant_response

    elif command == "update_tenant":
        tenant_id = args.tenant_id
        etag = args.etag
        display_name = args.display_name
        bookmark = []  # or value returned by last write operation
        tenant_response = client_config.update_tenant(tenant_id, etag, display_name, "description update", bookmark)
        if tenant_response:
            api_helper.print_response(tenant_response)
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
            for tenant in list_tenants_response:
                api_helper.print_response(tenant)
        else:
            print("Invalid list_tenants response")
        return list_tenants_response

    elif command == "delete_tenant":
        tenant_id = args.tenant_id
        if args.etag:
            etag = args.etag
        else:
            etag = None
        bookmark = []  # or value returned by last write operation
        delete_tenant_response = client_config.delete_tenant(tenant_id, etag, bookmark)
        if delete_tenant_response:
            print(delete_tenant_response)
        else:
            print("Invalid delete_tenant_response response")
        return delete_tenant_response

    elif command == "read_tenant_config":
        # read_tenant_config method: to get tenant config  info from tenant gid id
        bookmark = []  # or value returned by last write operation
        tenant_config = client_config.read_tenant_config(args.tenant_id, bookmark)
        if tenant_config:
            api_helper.print_response(tenant_config)
        else:
            print("None")

    elif command == "update_tenant_config":
        tenant_id = args.tenant_id
        etag = args.etag
        default_auth_flow_id = args.default_auth_flow_id
        bookmark = []  # or value returned by last write operation
        tenant_config = client_config.create_tenant_config(
            default_auth_flow_id=default_auth_flow_id,
            default_email_service_id=None,
            username_policy=client_config.username_policy(
                allowed_username_formats=["email", "mobile", "username"],
                valid_email=False,
                verify_email=False
            )
        )
        tenant_config_response = client_config.update_tenant_config(tenant_id, etag, tenant_config, bookmark)
        if tenant_config_response:
            api_helper.print_response(tenant_config_response)
        else:
            print("None")
        return tenant_config_response

    elif command == "application_id":
        application_id = args.application_id
        application = client_config.read_application_by_id(application_id)
        if application:
            api_helper.print_response(application)
        else:
            print("Invalid application id")

    elif command == "application_name":
        application_name = args.application_name
        app_space_id = args.app_space_id
        application = client_config.read_application_by_name(app_space_id, application_name)
        if application:
            api_helper.print_response(application)
        else:
            print("Invalid application name")

    elif command == "create_application":
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
        return application_response

    elif command == "update_application":
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
        bookmark = []  # or value returned by last write operation
        delete_application_response = client_config.delete_application(application_id, etag, bookmark)
        if delete_application_response:
            print(delete_application_response)
        else:
            print("Invalid delete_application_response response")
        return delete_application_response

    elif command == "application_agent_id":
        application_agent_id = args.application_agent_id
        application_agent = client_config.read_application_agent_by_id(application_agent_id)
        if application_agent:
            api_helper.print_response(application_agent)
        else:
            print("Invalid application agent id")

    elif command == "application_agent_name":
        application_agent_name = args.application_agent_name
        app_space_id = args.app_space_id
        application_agent = client_config.read_application_agent_by_name(app_space_id, application_agent_name)
        if application_agent:
            api_helper.print_response(application_agent)
        else:
            print("Invalid application agent name")

    elif command == "create_application_agent":
        application_id = args.application_id
        application_agent_name = args.application_agent_name
        display_name = args.display_name
        bookmark = []  # or value returned by last write operation
        application_agent_response = client_config.create_application_agent(
            application_id,
            application_agent_name,
            display_name,
            "description",
            bookmark)
        if application_agent_response:
            api_helper.print_response(application_agent_response)
        else:
            print("Invalid application agent response")
        return application_agent_response

    elif command == "update_application_agent":
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
        bookmark = []  # or value returned by last write operation
        delete_application_agent_response = client_config.delete_application_agent(
            application_agent_id,
            etag,
            bookmark)
        if delete_application_agent_response:
            print(delete_application_agent_response)
        else:
            print("Invalid delete_application_response_agent response")
        return delete_application_agent_response

    elif command == "application_agent_credential":
        application_agent_credential_id = args.application_agent_credential_id
        application_agent_credential = client_config.read_application_agent_credential(application_agent_credential_id)
        if application_agent_credential:
            api_helper.print_response(application_agent_credential)
        else:
            print("Invalid application agent id")

    elif command == "register_application_agent_credential_jwk":
        application_agent_id = args.application_agent_id
        display_name = args.display_name
        default_tenant_id = args.default_tenant_id
        jwk = None  # or replace by your JWK public key
        t = datetime.now().timestamp()
        expire_time_in_seconds = int(t) + 2678400  # now + one month example
        bookmark = []  # or value returned by last write operation
        application_agent_credential_response = client_config.register_application_agent_credential_jwk(
            application_agent_id,
            display_name,
            jwk,
            expire_time_in_seconds,
            default_tenant_id,
            bookmark
        )
        if application_agent_credential_response:
            api_helper.print_credential(application_agent_credential_response)
        else:
            print("Invalid application agent response")
        return application_agent_credential_response

    elif command == "register_application_agent_credential_pem":
        application_agent_id = args.application_agent_id
        display_name = args.display_name
        default_tenant_id = args.default_tenant_id
        pem = None  # or replace by your pem public certificate
        t = datetime.now().timestamp()
        expire_time_in_seconds = int(t) + 2678400  # now + one month example
        bookmark = []  # or value returned by last write operation
        application_agent_credential_response = client_config.register_application_agent_credential_pem(
            application_agent_id,
            display_name,
            pem,
            expire_time_in_seconds,
            default_tenant_id,
            bookmark
        )
        if application_agent_credential_response:
            api_helper.print_credential(application_agent_credential_response)
        else:
            print("Invalid application agent response")
        return application_agent_credential_response

    elif command == "delete_application_agent_credential":
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
        return delete_application_agent_credential_response

    elif command == "create_application_with_agent_credentials":
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
            args.tenant_id,
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
        return create_application_with_agent_credentials_response

    elif command == "service_account_id":
        service_account_id = args.service_account_id
        bookmark = []  # or value returned by last write operation
        service_account = client_config.read_service_account(service_account_id, bookmark)
        if service_account:
            api_helper.print_response(service_account)
        else:
            print("Invalid service account")

    elif command == "service_account_name":
        customer_id = args.customer_id
        service_account_name = args.service_account_name
        bookmark = []  # or value returned by last write operation
        service_account = client_config.read_service_account_by_name(customer_id, service_account_name, bookmark)
        if service_account:
            api_helper.print_response(service_account)
        else:
            print("Invalid service_account name")

    elif command == "create_service_account":
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
        return service_account_response

    elif command == "update_service_account":
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
        return service_account_response

    elif command == "delete_service_account":
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
        return delete_service_account_response

    elif command == "read_service_account_credential":
        service_account_credential_id = args.service_account_credential_id
        service_account_credential = client_config.read_service_account_credential(service_account_credential_id)
        if service_account_credential:
            api_helper.print_response(service_account_credential)
        else:
            print("Invalid service account id")

    elif command == "register_service_account_credential_jwk":
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
        return service_account_credential_response

    elif command == "register_service_account_credential_pem":
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
        return service_account_credential_response

    elif command == "delete_service_account_credential":
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
        return delete_service_account_credential_response

    elif command == "create_email_service_config_node":
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
        return create_email_service_config_node_response

    elif command == "read_config_node":
        config_node_id = args.config_node_id
        bookmark = []  # or value returned by last write operation
        version = 0
        config_node = client_config.read_config_node(config_node_id, bookmark, version)
        if config_node:
            api_helper.print_response(config_node)
        else:
            print("Invalid config node id")

    elif command == "update_email_service_config_node":
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
        return update_email_service_config_node_response

    elif command == "delete_config_node":
        config_node_id = args.config_node_id
        etag = args.etag
        config_node = client_config.delete_config_node(config_node_id, etag, [])
        if config_node:
            api_helper.print_response(config_node)
        else:
            print("Invalid delete config node response")

    elif command == "list_config_node_versions":
        config_node_id = args.config_node_id
        list_config_nodes = client_config.list_config_node_versions(config_node_id)
        if list_config_nodes:
            api_helper.print_response(list_config_nodes)
        else:
            print("Invalid list_config_nodes response")
        return list_config_nodes

    elif command == "create_auth_flow_config_node":
        location = args.app_space_id
        name = args.name
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
        return create_auth_flow_config_node_response

    elif command == "update_auth_flow_config_node":
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
        return update_auth_flow_config_node_response

    elif command == "create_oauth2_client_config_node":
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
        return create_oauth2_client_config_node_response

    elif command == "update_oauth2_client_config_node":
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
        return update_oauth2_client_config_node_response

    elif command == "create_webauthn_provider_config_node":
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
        return create_webauthn_provider_config_node_response

    elif command == "update_webauthn_provider_config_node":
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
        return update_webauthn_provider_config_node_response

    elif command == "create_authorization_policy_config_node":
        location = args.app_space_id
        name = args.name
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
        return create_authorization_policy_config_node_response

    elif command == "update_authorization_policy_config_node":
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
        return update_authorization_policy_config_node_response

    elif command == "read_oauth2_provider":
        oauth2_provider_id = args.oauth2_provider_id
        bookmark = []  # or value returned by last write operation
        config = client_config.read_oauth2_provider(oauth2_provider_id, bookmark)
        if config:
            api_helper.print_response(config)
        else:
            print("Invalid oauth2 provider id")

    elif command == "create_oauth2_provider":
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
        return create_oauth2_provider_response

    elif command == "update_oauth2_provider":
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
        return update_oauth2_provider_response

    elif command == "delete_oauth2_provider":
        oauth2_provider_id = args.oauth2_provider_id
        etag = args.etag
        bookmark = []  # or value returned by last write operation
        config = client_config.delete_oauth2_provider(oauth2_provider_id, etag, bookmark)
        if config:
            api_helper.print_response(config)
        else:
            print("Invalid delete oauth2 provider response")

    elif command == "read_oauth2_application":
        oauth2_application_id = args.oauth2_application_id
        bookmark = []  # or value returned by last write operation
        config = client_config.read_oauth2_application(oauth2_application_id, bookmark)
        if config:
            api_helper.print_response(config)
        else:
            print("Invalid oauth2 application id")

    elif command == "create_oauth2_application":
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
        return create_oauth2_application_response

    elif command == "update_oauth2_application":
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
        return update_oauth2_application_response

    elif command == "delete_oauth2_application":
        oauth2_application_id = args.oauth2_application_id
        etag = args.etag
        bookmark = []  # or value returned by last write operation
        config = client_config.delete_oauth2_application(oauth2_application_id, etag, bookmark)
        if config:
            api_helper.print_response(config)
        else:
            print("Invalid delete oauth2 application response")

    elif command == "is_authorized_identity_node":
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
        return is_authorized

    elif command == "is_authorized_token":
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
        return is_authorized

    elif command == "is_authorized_property":
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
        return is_authorized

    elif command == "is_authorized_external_id":
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
        return is_authorized

    elif command == "what_authorized_identity_node":
        identity_node_id = args.identity_node_id
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
        return what_authorized

    elif command == "what_authorized_token":
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
        return what_authorized

    elif command == "what_authorized_property":
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
        return what_authorized

    elif command == "what_authorized_external_id":
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
            api_helper.print_response(who_authorized)
        else:
            print("Invalid who_authorized")
        return who_authorized

    elif command == "get_http_client":
        token = None

        # generate an authenticated http client and generate a bearer token from the provided credentials
        client_http = HttpClient()
        response_http = client_http.get_http_client(token)
        client = "identity"
        credentials = credentials_config.lookup_env_credentials_variables(client)
        # call get_refreshable_token_source again to check the token is the same
        response_source = client_http.get_refreshable_token_source(response_http.token_source, credentials)
        print(response_source.token.access_token)
        # call get_http_client again to generate another http client and check if the token is the same
        response_http2 = client_http.get_http_client(response_http.token_source)
        access_token = response_http2.get_token()
        print(response_http2.token_source.token.access_token)
        # make a Knowledge API query
        endpoint = args.base_url
        data = {"query": "query ExampleQuery { identityProperties { id }}", "variables": {},
                "operationName": "ExampleQuery"}
        headers = {"Authorization": "Bearer " + access_token,
                   'Content-Type': 'application/json'}
        response_post = requests.post(endpoint, json=data, headers=headers)
        if response_post.text is not None:
            api_helper.print_response(response_post.text)

    elif command == "get_refreshable_token_source":
        token_source = None
        client_http = HttpClient()
        client = "identity"
        credentials = credentials_config.lookup_env_credentials_variables(client)
        response = client_http.get_refreshable_token_source(token_source, credentials, client)
        access_token_bytes = response.token.access_token
        print(access_token_bytes)

    elif command == "ingest_record_identity_node":
        # replace with actual values
        record_id = "96523658"
        external_id = "external-dt-id22737"
        type = "CarOwner"
        ingest_property = client_ingest.ingest_property("something", "741")
        properties = [ingest_property]
        upsert = client_ingest.upsert_data_node(
            external_id,
            type,
            [],
            properties,
            "",
            True
        )
        record = client_ingest.record_upsert(record_id, upsert)
        ingest_record_identity_node = client_ingest.ingest_record(record)
        if ingest_record_identity_node:
            api_helper.print_response(ingest_record_identity_node)
        else:
            print("Invalid upsert")
        return ingest_record_identity_node

    elif command == "ingest_record_resource":
        record_id = "74158100"
        external_id = "lot-1"
        type = "ParkingLot"
        ingest_property = client_ingest.ingest_property("customProp100", "9654")
        properties = [ingest_property]
        tags = []
        upsert = client_ingest.upsert_data_node(
            external_id,
            type,
            tags,
            properties,
            "",
            False)
        record = client_ingest.record_upsert(record_id, upsert)
        ingest_record_resource = client_ingest.ingest_record(record)
        if ingest_record_resource:
            api_helper.print_response(ingest_record_resource)
        else:
            print("Invalid upsert")
        return ingest_record_resource

    elif command == "ingest_record_relation":
        record_id = "7415890"
        type = "CAN_USE"
        source_match = client_ingest.node_match("vehicle-1", "Vehicle")
        target_match = client_ingest.node_match("lot-1", "ParkingLot")
        ingest_property = client_ingest.ingest_property("customProp", "8742")
        properties = [ingest_property]
        upsert = client_ingest.upsert_data_relationship(
            source_match, target_match, type,
            properties)
        record = client_ingest.record_upsert(record_id, upsert)
        ingest_record_relation = client_ingest.ingest_record(record)
        if ingest_record_relation:
            api_helper.print_response(ingest_record_relation)
        else:
            print("Invalid upsert")
        return ingest_record_relation

    elif command == "delete_record_node":
        record_id = "745890"
        node = client_ingest.node_match("vehicle-1", "Vehicle")
        delete = client_ingest.delete_data_node(node)
        record = client_ingest.record_delete(record_id, delete)
        delete_record_node = client_ingest.ingest_record(record)
        if delete_record_node:
            api_helper.print_response(delete_record_node)
        else:
            print("Invalid delete")
        return delete_record_node

    elif command == "delete_record_relation":
        record_id = "745890"
        type = "CAN_USE"
        source_match = client_ingest.node_match("vehicle-1", "Vehicle")
        target_match = client_ingest.node_match("lot-1", "ParkingLot")
        relationship = client_ingest.relationship(source_match, target_match, type, [])
        delete = client_ingest.delete_data_relation(relationship)
        record = client_ingest.record_delete(record_id, delete)
        delete_record_relation = client_ingest.ingest_record(record)
        if delete_record_relation:
            api_helper.print_response(delete_record_relation)
        else:
            print("Invalid delete")
        return delete_record_relation

    elif command == "delete_record_node_property":
        record_id = "745890"
        match = client_ingest.node_match("vehicle-1", "Vehicle")
        property_type = "nodePropertyName"
        node_property = client_ingest.node_property_match(match, property_type)
        delete = client_ingest.delete_data_node_property(node_property)
        record = client_ingest.record_delete(record_id, delete)
        delete_record_node_property = client_ingest.ingest_record(record)
        if delete_record_node_property:
            api_helper.print_response(delete_record_node_property)
        else:
            print("Invalid delete")
        return delete_record_node_property

    elif command == "delete_record_relation_property":
        record_id = "745890"
        type = "CAN_USE"
        source_match = client_ingest.node_match("vehicle-1", "Vehicle")
        target_match = client_ingest.node_match("lot-1", "ParkingLot")
        property_type = "relationPropertyName"
        relationship_property = client_ingest.relationship_property_match(source_match, target_match, type, property_type)
        delete = client_ingest.delete_data_relation_property(relationship_property)
        record = client_ingest.record_delete(record_id, delete)
        delete_record_relation_property = client_ingest.ingest_record(record)
        if delete_record_relation_property:
            api_helper.print_response(delete_record_relation_property)
        else:
            print("Invalid delete")
        return delete_record_relation_property

    elif command == "stream_records":
        # replace with actual values
        record_id = "114589904"
        external_id = "external-dt-id9004"
        type = "Person"
        tags = []
        ingest_property = client_ingest.ingest_property("customPropST1904", "741")
        properties = [ingest_property]
        upsert = client_ingest.upsert_data_node(
            external_id,
            type,
            tags,
            properties,
            "",
            True)
        record = client_ingest.record_upsert(record_id, upsert)

        record_id2 = "114589905"
        external_id = "lot-9050"
        type = "ParkingLot"
        ingest_property = client_ingest.ingest_property("customProp905", "9654")
        properties = [ingest_property]
        tags = []
        upsert2 = client_ingest.upsert_data_node(
            external_id,
            type,
            tags,
            properties)
        record2 = client_ingest.record_upsert(record_id2, upsert2)
        responses = client_ingest.stream_records([record, record2])
        if responses:
            for response in responses:
                api_helper.print_response(response)
        else:
            print("Invalid ingestion")
        return response

    elif command == "read_identity_knowledge":
        # replace with actual values
        input_params = {"external_id": "CJnoXYgnPNDAiMg", "type": "Organization"}
        query = "MATCH (n:Resource) WHERE n.external_id = $external_id and n.type=$type"
        returns = [ReturnKnowledge(variable="n")]
        responses = client_knowledge.identity_knowledge_read(query, input_params, returns)
        api_helper.print_response(responses)

    elif command == "get_identity_by_id":
        id = args.id
        response = client_knowledge.get_identity_by_id(id)
        if response:
            api_helper.print_response(response)
        else:
            print("No result")

    elif command == "get_identity_by_identifier":
        external_id = args.external_id
        type = args.type
        responses = client_knowledge.get_identity_by_identifier(external_id, type)
        if responses:
            for response in responses:
                api_helper.print_response(response)
        else:
            print("No result")

    elif command == "get_node_by_id":
        id = args.id
        response = client_knowledge.get_node_by_id(id)
        if response:
            api_helper.print_response(response)
        else:
            print("No result")

    elif command == "get_node_by_identifier":
        external_id = args.external_id
        type = args.type
        responses = client_knowledge.get_node_by_identifier(external_id, type)
        if responses:
            for response in responses:
                api_helper.print_response(response)
        else:
            print("No result")

    elif command == "list_nodes":
        responses = client_knowledge.list_nodes()
        if responses:
            for response in responses:
                api_helper.print_response(response)
        else:
            print("No result")

    elif command == "list_identities":
        responses = client_knowledge.list_identities()
        if responses:
            for response in responses:
                print(vars(response))
        else:
            print("No result")

    elif command == "list_nodes_by_property":
        # replace by own values
        property = {"color": "white"}
        responses = client_knowledge.list_nodes_by_property(property)
        if responses:
            for response in responses:
               print(vars(response))
        else:
            print("No result")

    elif command == "list_identities_by_property":
        # replace by own values
        property = {"last_name": "mushu"}
        responses = client_knowledge.list_identities_by_property(property)
        if responses:
            for response in responses:
                print(vars(response))
        else:
            print("No result")

    elif command == "get_property":
        node1 = NodeModel(
            id="gid:AAAAFVCygmDZtk8KtTtw9CBopC8",
            external_id="PEpkjOvUJQvqTFw",
            type="individual",
            tags=[],
            properties=[
                {
                    "key": "last_name",
                    "value": {
                        "stringValue": "mushu"
                    }
                }
            ])
        property1 = node1.get_property(node1, "last_name")
        print(property1)

    elif command == "get_metadata":
        metadata1 = Metadata(
            assurance_level=1,
            verification_time=datetime.now().timestamp(),
            source="Myself",
            custom_metadata={
                "customData": param_to_value("customValue")
            }
        )
        node1 = NodeModel(
            id="gid:AAAAFVCygmDZtk8KtTtw9CBopC8",
            external_id="PEpkjOvUJQvqTFw",
            type="individual",
            tags=[],
            properties=[
                {
                    "key": "last_name",
                    "value": {
                        "stringValue": "mushu"
                    },
                    "metadata": metadata1
                }
            ])
        metadata1 = node1.get_metadata(node1, "last_name")
        print(metadata1.__dir__())

    elif command == "delete_all_nodes":
        responses = client_knowledge.delete_all_with_node_type(args.node_type)
        if responses:
            for response in responses:
                api_helper.print_response(response)
        else:
            print("No result")


if __name__ == '__main__':  # pragma: no cover
    main()
