from datetime import datetime

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
ACCOUNT_ID= "gid:AAAAEvQjp80tGkaYgkn48BAyZb8"
WRONG_ACCOUNT_ID= "gid:AAAAFJ6iGHyG8Ee8tIvW7DQ1hkE"
CUSTOMER_NAME = "wonka"
APP_SPACE_NAME = "factory"
CUSTOMER_ID = "gid:AAAAAWluZHlraURlgAAAAAAAAA8"
APP_SPACE_ID = "gid:AAAAAmluZHlraURlgAABDwAAAAA"
ISSUER_ID = "gid:AAAAD2hBE6FIJk2giSaKTPc1pKk"
TENANT_ID = "gid:AAAAA2luZHlraURlgAADDwAAAAE"
TENANT_NAME = "wonka-1"
APPLICATION_ID = "gid:AAAABEqRACGqX02ZqLJTxRFnoiY"
APPLICATION_NAME = "application-test-sdk"
APPLICATION_AGENT_ID = "gid:AAAABRDhZImWvU1qrAV3q5-PM4M"
APPLICATION_AGENT_NAME = "app-agent-sdk"
APPLICATION_AGENT_CREDENTIAL_ID = "gid:AAAABtGBMvCtJ0LRlJqWs9C2EbQ"

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
