import os

import pytest


@pytest.fixture(name="set_env")
def set_env():
    if os.getenv("INDYKITE_APPLICATION_CREDENTIALS") or os.getenv("INDYKITE_APPLICATION_CREDENTIALS_FILE"):
        return True
    print("Missing config file (INDYKITE_APPLICATION_CREDENTIALS_FILE), not able to run the tests")
    return False
