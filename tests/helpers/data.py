from datetime import datetime
import json
import os
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import (UniqueNameIdentifier, SendGridProviderConfig, MailJetProviderConfig,
                                                          AmazonSESProviderConfig, MailgunProviderConfig,EmailServiceConfig,
                                                          AuthFlowConfig, OAuth2ClientConfig, IngestMappingConfig)
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import EmailAttachment, Email, EmailMessage, EmailTemplate, EmailDefinition
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import OAuth2ProviderConfig, OAuth2ApplicationConfig
from jarvis_sdk.indykite.config.v1beta1.model_pb2 import google_dot_protobuf_dot_wrappers__pb2 as wrappers


URL = "https://jarvis-dev.indykite.com"
EMAIL_URL = "https://super-octo-waffle.indykite.com"
EMAIL_TOKEN = "MNvLADeDKphk7NoEbczc"
APPLICATION = "gid:AAAABGluZHlraURlgAACDwAAAAA"
TENANT = "696e6479-6b69-4465-8000-030f00000001"
TENANT_EMAIL = "696e6479-6b69-4465-8000-030F00000002"
DIGITAL_TWIN = "6cdf1133-ba32-4dbb-a977-60b0d5d5e713"
CODE_VERIFIER = "AAAAAAAAAAEAAAAAAAAAAgAAAAAAAAADAAAAAAAAAAQ"
CODE_CHALLENGE = "cjbADBcANsbeEzqHghDd1YVnqh0GGaD3D2njiub5Fuk"
# this is changes, if test starts failing, check it!!!
VERIFICATION_BEARER = "eyJhbGciOiJFUzI1NiIsImN0eSI6IkpXVCIsImtpZCI6IkVmVUVpRm5PekE1UENwOFNTa3NwN2lYdjdjSFJlaENzSUdvNk5BUTlIN3ciLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiI2OTZlNjQ3OS02YjY5LTQ0NjUtODAwMC0wMTBmMDAwMDAwMDAiLCJleHAiOjE2Mjk2MjkzNDcsImlhdCI6MTYxMzY0NTM0NywiaXNzIjoiNjk2ZTY0NzktNmI2OS00NDY1LTgwMDAtMDUwZjAwMDAwMDAwIiwianRpIjoiMWMwYWMwNGEtM2ZiOC00N2IxLWJjNzQtYjkwNWE1ZmI0ZDBmIiwic3ViIjoiNjk2ZTY0NzktNmI2OS00NDY1LTgwMDAtMDUwZjAwMDAwMDAwIn0.VX1SAdIzzoRd4Jd-f-_X8sD5Y6al4K05UWtw-Ekn_9y3xgwwmPEXJ0a-HYrkR9vA7BPs6XQngYn0locsIWinEA"
EXPIRED_TOKEN = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJpYmlzLWluLWdvbGQiLCJleHAiOjE2NDkxNzMzNzQsImlhdCI6MTY0Njc1NDE3NCwiaXNzIjoiaWJpcy1pbi1nb2xkIiwianRpIjoiZGRlZDhkMDgtYjIxZi00Y2E2LTk0OTgtNDE0NTcxMzIyYzgxIiwibmJmIjoxNjQ2NzU0MTczLCJzdWIiOiJkWE5sY2pvNE16TTJPRGcxWXkwMk16WXlMVFJoT1RndE9UVXpNUzFtT0RVek9EUmtZalprTm1JPSIsInR5cCI6ImFjY2VzcyJ9.2FPjAT2Lo9T-1FZ4iBVLCZwCWHLzuSa9yJlsArUDWfMFsRyb9tqzyzcZ-IrBOQoIIBI3s5ksiFnVdrxp-zXTmQ"
CONFIG_ID= "gid:AAAAFJ6iGHyG8Ee8tIvW7DQ1hkE"
ACCOUNT_ID= "gid:AAAAEgGym_wUPEZfjV8TIdsImsE"
WRONG_ACCOUNT_ID= "gid:AAAAFJ6iGHyG8Ee8tIvW7DQ1hkE"
SERVICE_ACCOUNT_NAME = "serviceaccount-sdk"
TEST_SERVICE_ACCOUNT = "gid:AAAAEiuyZi3zVE9hvsu0gSqgi-g"
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
EMAIL_SERVICE_CONFIG_NODE = "gid:AAAACMMM3RvRwkbPgJGsM-uJaDs"
AUTH_FLOW_CONFIG_NODE = "gid:AAAAB3csFdhUY0SEvn_vJGKiA0c"
OAUTH2_CLIENT_CONFIG_NODE = "gid:AAAACgrCyXGVWkWBuEXw7aUmnmw"
INGEST_MAPPING_CONFIG_NODE = "gid:AAAAFKF1oNEdmEEArkQjezYRBPE"
OAUTH2_PROVIDER = "gid:AAAAEezCvUQGV0HgotmCoeCJAck"
OAUTH2_APPLICATION = "gid:AAAAC6mMTIwN40frlKWVz788QX8"
PASSWORD = "Password"
NEW_PASSWORD = "Password1"


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


def get_oauth2_provider_id():
    return OAUTH2_PROVIDER


def get_oauth2_application_id():
    return OAUTH2_APPLICATION


def get_email_service():
    default_from_address_address = "test+config@indykite.com"
    default_from_address_name = "Test Config"

    sendgrid = SendGridProviderConfig(
        api_key="263343b5-983e-4d73-b666-069a98f1ef55",
        sandbox_mode=True,
        ip_pool_name=wrappers.StringValue(value="100.45.21.65.25"),
        host=wrappers.StringValue(value="https://api.sendgrid.com")
    )

    message_to = [Email(address='test+to@indykite.com', name='Test To')]
    message_subject = "subject"
    message_text_content = "content text"
    message_html_content = "<html><body>content html</body></html>"

    email_service_config = EmailServiceConfig(
        default_from_address=Email(address=default_from_address_address, name=default_from_address_name),
        default=wrappers.BoolValue(value=True),
        sendgrid=sendgrid,
        authentication_message=EmailDefinition(message=EmailMessage(to=message_to, cc=[], bcc=[],
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


def get_ingest_mapping():
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
    return ingest_mapping_config


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
