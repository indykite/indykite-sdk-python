import json
import time
import uuid
from authlib.jose import JsonWebKey, jwt
from datetime import datetime, timedelta, timezone


def load_credentials(path):
    with open(path, 'r') as file:
        raw_content = file.read()
    return json.loads(raw_content)


def load_json(content):
    return json.loads(content)


def create_agent_jwt(credentials):
    jwk = credentials.get('privateKeyJWK')
    key = JsonWebKey.import_key(jwk)
    message = create_jwt_message(credentials)
    jwt_token = jwt.encode({
            'alg': 'ES256',
            'cty': 'JWT',
            'kid': jwk['kid']
    }, message, key)
    return jwt_token


def create_jwt_message(credentials):
    message = {
            'exp': get_int_from_datetime(datetime.now(timezone.utc) + timedelta(hours=24)),
            'iat': get_int_from_datetime(datetime.now(timezone.utc)),
            'iss': credentials.get('appAgentId'),
            'jti': str(uuid.uuid4()),
            'sub': credentials.get('appAgentId'),
    }
    return message


def get_int_from_datetime(dt):
    return int(time.mktime(dt.timetuple()))

