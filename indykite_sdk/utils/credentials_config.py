import json
import os
import sys
from pathlib import Path


def load_credentials(path):
    path = Path(path).resolve(strict=True)  # ensures the path exists and resolves symlinks
    if not path.is_file():
        raise FileNotFoundError(f"{path} is not a valid file.")

    with path.open("r", encoding="utf-8") as file:
        raw_content = file.read()
    return json.loads(raw_content)


def load_json(content):
    return json.loads(content)


def lookup_env_credentials_variables(client="identity"):
    """Get credentials from env variables
    :param client: string ["config", "authz", "ingest", "identity"]
    :return: credentials as dict
    """
    try:
        if client == "config":
            config = "INDYKITE_SERVICE_ACCOUNT_CREDENTIALS"
            config_file = "INDYKITE_SERVICE_ACCOUNT_CREDENTIALS_FILE"
        else:
            config = "INDYKITE_APPLICATION_CREDENTIALS"
            config_file = "INDYKITE_APPLICATION_CREDENTIALS_FILE"
        cred = os.getenv(config)
        # Load the config from File (secondary)
        if not cred:
            cred = os.getenv(config_file)
            if not cred:
                raise Exception("Missing " + config + " or " + config_file + " environment variable")

            credentials = os.path.join(os.path.dirname(cred), os.path.basename(cred))
            credentials = load_credentials(credentials)

        # Load the credential json (primary)
        else:
            credentials = load_json(cred)

        return credentials

    except Exception as exception:
        tb = sys.exception().__traceback__
        raise exception(...).with_traceback(tb)
