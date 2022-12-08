import os

import pytest

from tests.helpers import api_requests as helper
from tests.helpers import data


@pytest.fixture(name="set_env")
def set_env():
    if os.getenv("INDYKITE_APPLICATION_CREDENTIALS") or os.getenv("INDYKITE_APPLICATION_CREDENTIALS_FILE"):
        return True
    else:
        print("Missing config file (INDYKITE_APPLICATION_CREDENTIALS_FILE), not able to run the tests")
        return False


@pytest.fixture(name="login")
def login():
    token, refresh_token = helper.login("Abby.Sanford4@yahoo.com", data.get_password())
    return token, refresh_token


@pytest.fixture(name="registration")
def registration():
    token, refresh_token = helper.registration(data.get_new_email(), data.get_password())
    return token, refresh_token


@pytest.fixture(name="registration_with_email_verification")
def registration_with_email_verification():
    token, refresh_token = helper.registration_with_email_verification(data.get_new_email(), data.get_password())
    return token, refresh_token


@pytest.fixture(name="registration_until_email_arrives")
def registration_until_email_arrives():
    token = helper.registration_until_email_arrives(data.get_new_email(), data.get_password())
    return token
