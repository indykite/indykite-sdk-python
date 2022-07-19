from datetime import datetime

URL = "https://jarvis-dev.indykite.com"
EMAIL_URL = "https://super-octo-waffle.indykite.com"
EMAIL_TOKEN = "MNvLADeDKphk7NoEbczc"
APPLICATION = "696e6479-6b69-4465-8000-020F00000000"
TENANT = "696e6479-6b69-4465-8000-030F00000001"
TENANT_EMAIL = "696e6479-6b69-4465-8000-030F00000002"
CODE_VERIFIER = "AAAAAAAAAAEAAAAAAAAAAgAAAAAAAAADAAAAAAAAAAQ"
CODE_CHALLENGE = "cjbADBcANsbeEzqHghDd1YVnqh0GGaD3D2njiub5Fuk"
# this is changes, if test starts failing, check it!!!
VERIFICATION_BEARER = "eyJhbGciOiJFUzI1NiIsImN0eSI6IkpXVCIsImtpZCI6IkVmVUVpRm5PekE1UENwOFNTa3NwN2lYdjdjSFJlaENzSUdvNk5BUTlIN3ciLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiI2OTZlNjQ3OS02YjY5LTQ0NjUtODAwMC0wMTBmMDAwMDAwMDAiLCJleHAiOjE2Mjk2MjkzNDcsImlhdCI6MTYxMzY0NTM0NywiaXNzIjoiNjk2ZTY0NzktNmI2OS00NDY1LTgwMDAtMDUwZjAwMDAwMDAwIiwianRpIjoiMWMwYWMwNGEtM2ZiOC00N2IxLWJjNzQtYjkwNWE1ZmI0ZDBmIiwic3ViIjoiNjk2ZTY0NzktNmI2OS00NDY1LTgwMDAtMDUwZjAwMDAwMDAwIn0.VX1SAdIzzoRd4Jd-f-_X8sD5Y6al4K05UWtw-Ekn_9y3xgwwmPEXJ0a-HYrkR9vA7BPs6XQngYn0locsIWinEA"
EXPIRED_TOKEN = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJpYmlzLWluLWdvbGQiLCJleHAiOjE2NDkxNzMzNzQsImlhdCI6MTY0Njc1NDE3NCwiaXNzIjoiaWJpcy1pbi1nb2xkIiwianRpIjoiZGRlZDhkMDgtYjIxZi00Y2E2LTk0OTgtNDE0NTcxMzIyYzgxIiwibmJmIjoxNjQ2NzU0MTczLCJzdWIiOiJkWE5sY2pvNE16TTJPRGcxWXkwMk16WXlMVFJoT1RndE9UVXpNUzFtT0RVek9EUmtZalprTm1JPSIsInR5cCI6ImFjY2VzcyJ9.2FPjAT2Lo9T-1FZ4iBVLCZwCWHLzuSa9yJlsArUDWfMFsRyb9tqzyzcZ-IrBOQoIIBI3s5ksiFnVdrxp-zXTmQ"
CONFIG_ID= "gid:AAAAFJ6iGHyG8Ee8tIvW7DQ1hkE"

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
