from datetime import datetime
import json
import os
from indykite_sdk.config import ConfigClient


INDYKITE_SDK_URL = os.getenv('INDYKITE_SDK_URL')
EMAIL_URL = os.getenv('EMAIL_URL')
EMAIL_TOKEN = os.getenv('EMAIL_TOKEN')
APPLICATION = os.getenv('APPLICATION')
IDENTITY_NODE = os.getenv('IDENTITY_NODE')
IDENTITY_NODE_TEST = os.getenv('IDENTITY_NODE_TEST')
IDENTITY_NODE_CONSENT = os.getenv('IDENTITY_NODE_CONSENT')
IDENTITY_NODE_PROPERTY = os.getenv('IDENTITY_NODE_PROPERTY')
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
APPLICATION_ID = os.getenv('APPLICATION_ID')
APPLICATION_NAME = os.getenv('APPLICATION_NAME')
APPLICATION_AGENT_ID = os.getenv('APPLICATION_AGENT_ID')
APPLICATION_AGENT_NAME = os.getenv('APPLICATION_AGENT_NAME')
APPLICATION_AGENT_CREDENTIAL_ID = os.getenv('APPLICATION_AGENT_CREDENTIAL_ID')
SERVICE_ACCOUNT_CREDENTIAL_ID = os.getenv('SERVICE_ACCOUNT_CREDENTIAL_ID')
AUTHZ_POLICY_CONFIG_NODE = os.getenv('AUTHZ_POLICY_CONFIG_NODE')
CONSENT_CONFIG_NODE = os.getenv('CONSENT_CONFIG_NODE')
CONSENT_ID = os.getenv('CONSENT_ID')
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


def get_application():
    return APPLICATION


def get_identity_node():
    return INDIVIDUAL_ID


def get_identity_node_external_id():
    return INDIVIDUAL_EXTERNAL_ID


def get_identity_node_test():
    return IDENTITY_NODE_TEST


def get_identity_node_consent():
    return IDENTITY_NODE_CONSENT


def get_identity_node_property():
    return IDENTITY_NODE_PROPERTY


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


def get_authz_policy_config_node_id():
    return AUTHZ_POLICY_CONFIG_NODE


def get_consent_config_node_id():
    return CONSENT_CONFIG_NODE


def get_consent_id():
    return CONSENT_ID


def get_authz_policy():
    with open(os.path.dirname(__file__) + "/sdk_policy_config.json") as f:
        file_data = f.read()
    policy_dict = json.loads(file_data)
    policy_dict = json.dumps(policy_dict)
    policy_config = ConfigClient().authorization_policy_config(str(policy_dict), "STATUS_ACTIVE", [])
    return policy_config


def get_consent_config():
    consent_config = ConfigClient().consent_config(
        purpose = "Taking control",
        data_points = {"lastname", "firstname", "email"},
        application_id = get_application_id(),
        validity_period = 86400,
        revoke_after_use = False
    )
    return consent_config
