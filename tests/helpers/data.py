from datetime import datetime
import json
import os
from indykite_sdk.indykite.config.v1beta1.model_pb2 import (UniqueNameIdentifier, SendGridProviderConfig, MailJetProviderConfig,
                                                          AmazonSESProviderConfig, MailgunProviderConfig,EmailServiceConfig,
                                                          AuthFlowConfig, OAuth2ClientConfig, IngestMappingConfig, WebAuthnProviderConfig, AuthorizationPolicyConfig)
from indykite_sdk.indykite.config.v1beta1.model_pb2 import EmailAttachment, Email, EmailMessage, EmailTemplate, EmailDefinition
from indykite_sdk.indykite.config.v1beta1.model_pb2 import OAuth2ProviderConfig, OAuth2ApplicationConfig
from indykite_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers
from google.protobuf.duration_pb2 import Duration


URL = os.getenv('INDYKITE_SDK_URL')
EMAIL_URL = os.getenv('EMAIL_URL')
EMAIL_TOKEN = "MNvLADeDKphk7NoEbczc"
APPLICATION = "gid:AAAABGluZHlraURlgAACDwAAAAA"
TENANT = "gid:AAAAA2CHw7x3Dk68uWSkjl7FoG0"
TENANT_EMAIL = "gid:AAAAA2luZHlraURlgAADDwAAAAI"
DIGITAL_TWIN = "gid:AAAAFZVCTOBCHEPMgdvP44aZLbg"
DIGITAL_TWIN_TEST = "gid:AAAAFf_ZpzyM2UpRuG22DJLLNq0"
DIGITAL_TWIN_CONSENT = "gid:AAAAFQQTyHL70kRJsvm0rnkDFKQ"
CODE_VERIFIER = "AAAAAAAAAAEAAAAAAAAAAgAAAAAAAAADAAAAAAAAAAQ"
CODE_CHALLENGE = "cjbADBcANsbeEzqHghDd1YVnqh0GGaD3D2njiub5Fuk"
# this is changes, if test starts failing, check it!!!
VERIFICATION_BEARER = "eyJhbGciOiJFUzI1NiIsImN0eSI6IkpXVCIsImtpZCI6IkVmVUVpRm5PekE1UENwOFNTa3NwN2lYdjdjSFJlaENzSUdvNk5BUTlIN3ciLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiI2OTZlNjQ3OS02YjY5LTQ0NjUtODAwMC0wMTBmMDAwMDAwMDAiLCJleHAiOjE2Mjk2MjkzNDcsImlhdCI6MTYxMzY0NTM0NywiaXNzIjoiNjk2ZTY0NzktNmI2OS00NDY1LTgwMDAtMDUwZjAwMDAwMDAwIiwianRpIjoiMWMwYWMwNGEtM2ZiOC00N2IxLWJjNzQtYjkwNWE1ZmI0ZDBmIiwic3ViIjoiNjk2ZTY0NzktNmI2OS00NDY1LTgwMDAtMDUwZjAwMDAwMDAwIn0.VX1SAdIzzoRd4Jd-f-_X8sD5Y6al4K05UWtw-Ekn_9y3xgwwmPEXJ0a-HYrkR9vA7BPs6XQngYn0locsIWinEA"
EXPIRED_TOKEN = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJpYmlzLWluLWdvbGQiLCJleHAiOjE2NDkxNzMzNzQsImlhdCI6MTY0Njc1NDE3NCwiaXNzIjoiaWJpcy1pbi1nb2xkIiwianRpIjoiZGRlZDhkMDgtYjIxZi00Y2E2LTk0OTgtNDE0NTcxMzIyYzgxIiwibmJmIjoxNjQ2NzU0MTczLCJzdWIiOiJkWE5sY2pvNE16TTJPRGcxWXkwMk16WXlMVFJoT1RndE9UVXpNUzFtT0RVek9EUmtZalprTm1JPSIsInR5cCI6ImFjY2VzcyJ9.2FPjAT2Lo9T-1FZ4iBVLCZwCWHLzuSa9yJlsArUDWfMFsRyb9tqzyzcZ-IrBOQoIIBI3s5ksiFnVdrxp-zXTmQ"
CONFIG_ID= "gid:AAAAFJ6iGHyG8Ee8tIvW7DQ1hkE"
ACCOUNT_ID= "gid:AAAAEgGym_wUPEZfjV8TIdsImsE"
WRONG_ACCOUNT_ID= "gid:AAAAFJ6iGHyG8Ee8tIvW7DQ1hkE"
SERVICE_ACCOUNT_NAME = "serviceaccount-sdk"
TEST_SERVICE_ACCOUNT = "gid:AAAAEv3GiONu2UdplM9ML9eCrus"
CUSTOMER_NAME = "sdk-customer"
APP_SPACE_NAME = "sdk-appspace"
CUSTOMER_ID = "gid:AAAAAbHLUExsxkqsqRoI93amR30"
APP_SPACE_ID = "gid:AAAAAi7tSAs-qkg_his0YnvKuJ4"
ISSUER_ID = "gid:AAAAD1DBxqIze0UniM_vaogDx6Y"
TENANT_ID = "gid:AAAAA9Q51FULGECVrvbfN0kUbSk"
TENANT_NAME = "sdk-test-tenant"
APPLICATION_ID = "gid:AAAABNetL1rt6UKumXoYni2kQE0"
APPLICATION_NAME = "application-sdk"
APPLICATION_AGENT_ID = "gid:AAAABbPQM7m4OUbXnsfyef2zOc0"
APPLICATION_AGENT_NAME = "appagent-sdk"
APPLICATION_AGENT_CREDENTIAL_ID = "gid:AAAABhgLSrxgg0_nuVeZppYYSGs"
SERVICE_ACCOUNT_CREDENTIAL_ID = "gid:AAAAE0rMcwG_RUbSjzclsV7bdjg"
EMAIL_SERVICE_CONFIG_NODE = "gid:AAAACPZyR178jEYLj0wizNxtO4Q"
AUTH_FLOW_CONFIG_NODE = "gid:AAAAB0Vg1IohjEV4uDLA_hFawKI"
OAUTH2_CLIENT_CONFIG_NODE = "gid:AAAACtBSbo_Sf0XXpOzuoNfzMk8"
INGEST_MAPPING_CONFIG_NODE = "gid:AAAAFLk0_fECVENquHrfZUTjaic"
WEBAUTHN_PROVIDER_CONFIG_NODE = "gid:AAAADRcYFyi8IUUIv-P5IJwlXQ0"
AUTHZ_POLICY_CONFIG_NODE = "gid:AAAAFqlGrfMyt0Pnlo5uozu_4oM"
OAUTH2_PROVIDER = "gid:AAAAEXX8LPjXo0bmvR1VWQEwrQI"
OAUTH2_APPLICATION = "gid:AAAAC5wPdP0VEUHqvLdEOwkVJCA"
PASSWORD = "Password"
NEW_PASSWORD = "Password1"
BCRYPT = "$2y$10$k64jP7oqwYfQpzmoqAN5OuhrtWI2wICn0wXUzYxMp.UA1PopI653G"


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


def get_url():
    return URL


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


def get_ingest_mapping_config_node_id():
    return INGEST_MAPPING_CONFIG_NODE


def get_webauthn_provider_config_node_id():
    return WEBAUTHN_PROVIDER_CONFIG_NODE


def get_authz_policy_config_node_id():
    return AUTHZ_POLICY_CONFIG_NODE


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
        default=wrappers.BoolValue(value=True),
        sendgrid=sendgrid,
        invitation_message=EmailDefinition(message=EmailMessage(to=message_to, cc=[], bcc=[],
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

    auth_flow_config = AuthFlowConfig(
        source_format="FORMAT_BARE_JSON",
        source=bytes(user_dict),
        default=wrappers.BoolValue(value=False)
    )
    return auth_flow_config


def get_oauth2_client():
    oauth2_client_config = OAuth2ClientConfig(
        provider_type="PROVIDER_TYPE_GOOGLE_COM",
        client_id="gt41g2ju85ol1j2u1t",
        client_secret="e45454JIIH45ven9e8sbfdv4d5",
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
        front_channel_login_uri={"default": "http://localhost:3000/login/oauth2"},
        front_channel_consent_uri={"default": "http://localhost:3000/consent"}
    )
    return config


def get_oauth2_application():
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
    return config


def get_webauthn_provider():
    webauthn_provider_config = WebAuthnProviderConfig(
        relying_parties={"http://localhost":"localhost"},
        attestation_preference="CONVEYANCE_PREFERENCE_NONE",
        require_resident_key=False,
        user_verification="USER_VERIFICATION_REQUIREMENT_PREFERRED",
        authenticator_attachment="AUTHENTICATOR_ATTACHMENT_DEFAULT",
        registration_timeout=Duration(seconds=30),
        authentication_timeout=Duration(seconds=60)
    )
    return webauthn_provider_config


def get_webauthn_provider_exception():
    webauthn_provider_config = WebAuthnProviderConfig(
        relying_parties={"localhost": "localhost"},
        attestation_preference="CONVEYANCE_PREFERENCE_NONE",
        require_resident_key=False,
        user_verification="USER_VERIFICATION_REQUIREMENT_PREFERRED",
        authenticator_attachment="AUTHENTICATOR_ATTACHMENT_DEFAULT",
        registration_timeout=Duration(seconds=30),
        authentication_timeout=Duration(seconds=60)
    )
    return webauthn_provider_config


def get_authz_policy():
    with open(os.path.dirname(__file__) + "/sdk_policy_config.json") as f:
        file_data = f.read()
    policy_dict = json.loads(file_data)
    policy_dict = json.dumps(policy_dict)
    policy_config = AuthorizationPolicyConfig(
        policy=str(policy_dict),
        status="STATUS_ACTIVE",
        tags=[]
    )
    return policy_config
