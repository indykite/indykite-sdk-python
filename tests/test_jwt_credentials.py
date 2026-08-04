import time

from joserfc import jwk

from indykite_sdk.utils import jwt_credentials


def _credentials(service_account_id="gid:AAAAATESTSERVICEACCOUNT"):
    return {
        "serviceAccountId": service_account_id,
        "privateKeyJWK": jwk.generate_key("EC", "P-256", private=True, auto_kid=True).as_dict(private=True),
    }


def test_create_agent_jwt_and_read_exp_config_client():
    credentials = _credentials()
    token = jwt_credentials.create_agent_jwt(credentials, client="config")
    exp = jwt_credentials.get_exp_from_jwt(token, credentials["privateKeyJWK"])

    assert isinstance(token, str)
    assert isinstance(exp, int)
    assert exp > int(time.time())


def test_create_agent_jwt_and_read_exp_identity_client():
    credentials = _credentials()
    credentials["appAgentId"] = "gid:AAAAATESTAPPAGENT"
    token = jwt_credentials.create_agent_jwt(credentials, client="identity")
    exp = jwt_credentials.get_exp_from_jwt(token, credentials["privateKeyJWK"])

    assert isinstance(token, str)
    assert isinstance(exp, int)
    assert exp > int(time.time())


def test_as_access_token_handles_str_and_bytes():
    assert jwt_credentials.as_access_token("abc") == "abc"
    assert jwt_credentials.as_access_token(b"abc") == "abc"
