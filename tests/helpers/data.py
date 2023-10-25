from datetime import datetime
import json
import os
from indykite_sdk.indykite.config.v1beta1.model_pb2 import (UniqueNameIdentifier, SendGridProviderConfig, MailJetProviderConfig,
                                                          AmazonSESProviderConfig, MailgunProviderConfig,EmailServiceConfig,
                                                          AuthFlowConfig, OAuth2ClientConfig, WebAuthnProviderConfig, AuthorizationPolicyConfig)
from indykite_sdk.indykite.config.v1beta1.model_pb2 import EmailAttachment, Email, EmailMessage, EmailTemplate, EmailDefinition
from indykite_sdk.indykite.config.v1beta1.model_pb2 import OAuth2ProviderConfig, OAuth2ApplicationConfig
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from google.protobuf.duration_pb2 import Duration
from indykite_sdk.config import ConfigClient


INDYKITE_SDK_URL = os.getenv('INDYKITE_SDK_URL')
EMAIL_URL = os.getenv('EMAIL_URL')
EMAIL_TOKEN = os.getenv('EMAIL_TOKEN')
APPLICATION = os.getenv('APPLICATION')
TENANT = os.getenv('TENANT')
TENANT_EMAIL = os.getenv('TENANT_EMAIL')
DIGITAL_TWIN = os.getenv('DIGITAL_TWIN')
DIGITAL_TWIN_TEST = os.getenv('DIGITAL_TWIN_TEST')
DIGITAL_TWIN_CONSENT = os.getenv('DIGITAL_TWIN_CONSENT')
DIGITAL_TWIN_PROPERTY = os.getenv('DIGITAL_TWIN_PROPERTY')
CODE_VERIFIER = os.getenv('CODE_VERIFIER')
CODE_CHALLENGE = os.getenv('CODE_CHALLENGE')
VERIFICATION_BEARER = os.getenv('VERIFICATION_BEARER')
EXPIRED_TOKEN = os.getenv('EXPIRED_TOKEN')
CONFIG_ID = os.getenv('CONFIG_ID')
ACCOUNT_ID = os.getenv('ACCOUNT_ID')
WRONG_ACCOUNT_ID = os.getenv('WRONG_ACCOUNT_ID')
SERVICE_ACCOUNT_NAME = os.getenv('SERVICE_ACCOUNT_NAME')
TEST_SERVICE_ACCOUNT = os.getenv('TEST_SERVICE_ACCOUNT')
CUSTOMER_NAME = os.getenv('CUSTOMER_NAME')
APP_SPACE_NAME = os.getenv('APP_SPACE_NAME')
CUSTOMER_ID = os.getenv('CUSTOMER_ID')
CUSTOMER_ID2 = os.getenv('CUSTOMER_ID2')
APP_SPACE_ID = os.getenv('APP_SPACE_ID')
ISSUER_ID = os.getenv('ISSUER_ID')
TENANT_ID = os.getenv('TENANT_ID')
TENANT_NAME = os.getenv('TENANT_NAME')
APPLICATION_ID = os.getenv('APPLICATION_ID')
APPLICATION_NAME = os.getenv('APPLICATION_NAME')
APPLICATION_AGENT_ID = os.getenv('APPLICATION_AGENT_ID')
APPLICATION_AGENT_NAME = os.getenv('APPLICATION_AGENT_NAME')
APPLICATION_AGENT_CREDENTIAL_ID = os.getenv('APPLICATION_AGENT_CREDENTIAL_ID')
SERVICE_ACCOUNT_CREDENTIAL_ID = os.getenv('SERVICE_ACCOUNT_CREDENTIAL_ID')
EMAIL_SERVICE_CONFIG_NODE = os.getenv('EMAIL_SERVICE_CONFIG_NODE')
AUTH_FLOW_CONFIG_NODE = os.getenv('AUTH_FLOW_CONFIG_NODE')
OAUTH2_CLIENT_CONFIG_NODE = os.getenv('OAUTH2_CLIENT_CONFIG_NODE')
WEBAUTHN_PROVIDER_CONFIG_NODE = os.getenv('WEBAUTHN_PROVIDER_CONFIG_NODE')
AUTHZ_POLICY_CONFIG_NODE = os.getenv('AUTHZ_POLICY_CONFIG_NODE')
KG_SCHEMA_CONFIG_NODE = os.getenv('KG_SCHEMA_CONFIG_NODE')
OAUTH2_PROVIDER = os.getenv('OAUTH2_PROVIDER')
OAUTH2_APPLICATION = os.getenv('OAUTH2_APPLICATION')
PASSWORD = os.getenv('PASSWORD')
NEW_PASSWORD = os.getenv('NEW_PASSWORD')
BCRYPT = os.getenv('BCRYPT')
SUBMITTER_SECRET = os.getenv('SUBMITTER_SECRET')
MANAGER_SECRET = os.getenv('MANAGER_SECRET')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
RELYING_PARTIES = os.getenv('RELYING_PARTIES')
ORGANIZATION_EXTERNAL_ID = os.getenv('ORGANIZATION_EXTERNAL_ID')
ASSET_EXTERNAL_ID = os.getenv('ASSET_EXTERNAL_ID')
INDIVIDUAL_EXTERNAL_ID = os.getenv('INDIVIDUAL_EXTERNAL_ID')
ORGANIZATION_ID = os.getenv('ORGANIZATION_ID')
ASSET_ID = os.getenv('ASSET_ID')
INDIVIDUAL_ID = os.getenv('INDIVIDUAL_ID')


def get_password():
    return PASSWORD


def get_old_password():
    return PASSWORD


def get_new_password():
    return NEW_PASSWORD


def get_new_email():
    email = "automation_"+str(datetime.now().timestamp())+"@yahoo.com"
    return email


def get_code_challenge():
    return CODE_CHALLENGE


def get_code_verifier():
    return CODE_VERIFIER


def get_application():
    return APPLICATION


def get_tenant():
    return TENANT


def get_tenant_email():
    return TENANT_EMAIL


def get_digital_twin():
    return DIGITAL_TWIN


def get_digital_twin_test():
    return DIGITAL_TWIN_TEST


def get_digital_twin_consent():
    return DIGITAL_TWIN_CONSENT


def get_digital_twin_property():
    return DIGITAL_TWIN_PROPERTY


def get_url():
    return INDYKITE_SDK_URL


def get_email_url():
    return EMAIL_URL


def get_email_token():
    return EMAIL_TOKEN


def get_verification_bearer():
    return VERIFICATION_BEARER


def get_expired_token():
    return EXPIRED_TOKEN


def get_config_id():
    return CONFIG_ID


def get_wrong_account_id():
    return WRONG_ACCOUNT_ID


def get_account_id():
    return ACCOUNT_ID


def get_customer_name():
    return CUSTOMER_NAME


def get_customer_id():
    return CUSTOMER_ID


def get_customer_id2():
    return CUSTOMER_ID2


def get_app_space_name():
    return APP_SPACE_NAME


def get_app_space_id():
    return APP_SPACE_ID


def get_issuer_id():
    return ISSUER_ID


def get_tenant_id():
    return TENANT_ID


def get_tenant_name():
    return TENANT_NAME


def get_application_id():
    return APPLICATION_ID


def get_application_name():
    return APPLICATION_NAME


def get_application_agent_id():
    return APPLICATION_AGENT_ID


def get_application_agent_name():
    return APPLICATION_AGENT_NAME


def get_application_agent_credential_id():
    return APPLICATION_AGENT_CREDENTIAL_ID


def get_service_account_id():
    return TEST_SERVICE_ACCOUNT


def get_service_account_name():
    return SERVICE_ACCOUNT_NAME


def get_service_account_credential_id():
    return SERVICE_ACCOUNT_CREDENTIAL_ID


def get_email_service_config_node_id():
    return EMAIL_SERVICE_CONFIG_NODE


def get_auth_flow_config_node_id():
    return AUTH_FLOW_CONFIG_NODE


def get_oauth2_client_config_node_id():
    return OAUTH2_CLIENT_CONFIG_NODE


def get_webauthn_provider_config_node_id():
    return WEBAUTHN_PROVIDER_CONFIG_NODE


def get_readid_provider_config_node_id():
    return READID_PROVIDER_CONFIG_NODE


def get_authz_policy_config_node_id():
    return AUTHZ_POLICY_CONFIG_NODE


def get_kg_schema_config_node_id():
    return KG_SCHEMA_CONFIG_NODE


def get_oauth2_provider_id():
    return OAUTH2_PROVIDER


def get_oauth2_application_id():
    return OAUTH2_APPLICATION


def get_email_service():
    default_from_address_address = os.getenv('INDYKITE_DEFAULT_FROM')
    default_from_address_name = "Test Config"

    sendgrid = SendGridProviderConfig(
        api_key=os.getenv('SENDGRID_KEY'),
        sandbox_mode=True,
        ip_pool_name=wrappers.StringValue(value=os.getenv('SENDGRID_IP')),
        host=wrappers.StringValue(value="https://api.sendgrid.com")
    )

    message_to = [Email(address=os.getenv('INDYKITE_DEFAULT_TO'), name='Test To')]
    message_subject = "subject"
    message_text_content = "content text"
    message_html_content = "<html><body>content html</body></html>"

    email_service_config = EmailServiceConfig(
        default_from_address=Email(address=default_from_address_address, name=default_from_address_name),
        sendgrid=sendgrid,
        invitation_message=EmailDefinition(message=EmailMessage(
            to=message_to,
            cc=[],
            bcc=[],
            subject=message_subject,
            text_content=message_text_content,
            html_content=message_html_content))
    )
    return email_service_config


def get_auth_flow():
    with open(os.path.dirname(__file__) + "/sdk_simple_flow.json") as f:
        file_data = f.read()
    user_dict = json.loads(file_data)
    user_dict = json.dumps(user_dict, indent=4, separators=(',', ': ')).encode('utf-8')
    auth_flow_config = ConfigClient().auth_flow_config(
        "FORMAT_BARE_JSON",
        user_dict
    )
    return auth_flow_config


def get_oauth2_client():
    oauth2_client_config = OAuth2ClientConfig(
        provider_type="PROVIDER_TYPE_GOOGLE_COM",
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'),
        default_scopes=["openid", "profile", "email"],
        allowed_scopes=["openid", "profile", "email"]
    )
    return oauth2_client_config


def get_oauth2_provider():
    config = OAuth2ProviderConfig(
        grant_types=["GRANT_TYPE_AUTHORIZATION_CODE"],
        response_types=["RESPONSE_TYPE_CODE", "RESPONSE_TYPE_TOKEN"],
        scopes=["openid", "profile", "email"],
        token_endpoint_auth_method=["TOKEN_ENDPOINT_AUTH_METHOD_CLIENT_SECRET_BASIC",
                                    "TOKEN_ENDPOINT_AUTH_METHOD_CLIENT_SECRET_POST"],
        token_endpoint_auth_signing_alg=["ES256", "ES384", "ES512"],
        # local env example
        front_channel_login_uri={"default": "http://localhost:3000/login/oauth2"},
        front_channel_consent_uri={"default": "http://localhost:3000/consent"}
    )
    return config


def get_oauth2_application():
    config = OAuth2ApplicationConfig(
        display_name="Oauth2 Application Config",
        # local env example
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
    return config


def get_webauthn_provider():
    webauthn_provider_config = ConfigClient().webauthn_provider_config(
        {"http://localhost": "localhost"},
        "CONVEYANCE_PREFERENCE_NONE",
        "AUTHENTICATOR_ATTACHMENT_DEFAULT",
        False,
        "USER_VERIFICATION_REQUIREMENT_PREFERRED",
        Duration(seconds=30),
        Duration(seconds=60)
    )
    return webauthn_provider_config


def get_webauthn_provider_exception():
    webauthn_provider_config = ConfigClient().webauthn_provider_config(
        {"localhost": "localhost"},
        "CONVEYANCE_PREFERENCE_NONE",
        "AUTHENTICATOR_ATTACHMENT_DEFAULT",
        False,
        "USER_VERIFICATION_REQUIREMENT_PREFERRED",
        Duration(seconds=30),
        Duration(seconds=60)
    )
    return webauthn_provider_config


def get_authz_policy():
    with open(os.path.dirname(__file__) + "/sdk_policy_config.json") as f:
        file_data = f.read()
    policy_dict = json.loads(file_data)
    policy_dict = json.dumps(policy_dict)
    policy_config = ConfigClient().authorization_policy_config(str(policy_dict), "STATUS_ACTIVE", [])
    return policy_config


def get_kg_schema():
    with open(os.path.dirname(__file__) + "/sdk_schema.txt", "r") as file:
        file_data = "\n".join(file.read().split("\n"))
    schema_config = ConfigClient().knowledge_graph_schema_config(file_data)
    return schema_config


def get_readid_provider():
    submitter_secret = os.getenv('SUBMITTER_SECRET')
    manager_secret = os.getenv('MANAGER_SECRET')
    # random example
    submitter_password = "1234566677"
    host_address = "<https://saas-preprod.readid.com>"
    readid_property = ConfigClient().readid_property("c.secondaryIdentifier", True)
    property_map = {"givenname": readid_property}
    unique_property_name = "uniquepropertyname"

    readid_provider_config = ConfigClient().readid_provider_config(
        submitter_secret,
        manager_secret,
        submitter_password,
        host_address,
        property_map,
        unique_property_name
    )
    return readid_provider_config


def get_readid_provider_exception():
    submitter_secret = "randomvalue"
    manager_secret = "randomvalue"
    submitter_password = "444466677"
    host_address = "saas-preprod.readid.com"
    property_map = {"givenname": []}
    unique_property_name = "uniquepropertyname"

    readid_provider_config = ConfigClient().readid_provider_config(
        submitter_secret,
        manager_secret,
        submitter_password,
        host_address,
        property_map,
        unique_property_name
    )
    return readid_provider_config
