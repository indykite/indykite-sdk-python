import time
import uuid
import re
import grpc
import certifi
import sys
import os
from authlib.jose import JsonWebKey, jwt
from datetime import datetime, timedelta
from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2_grpc as config_pb2_grpc
from indykite_sdk.indykite.identity.v1beta2 import identity_management_api_pb2_grpc as pb2_grpc
from indykite_sdk.indykite.ingest.v1beta3 import ingest_api_pb2_grpc as ingest_pb2_grpc
from indykite_sdk.indykite.authorization.v1beta1 import authorization_service_pb2_grpc as authz_pb2
from indykite_sdk.indykite.knowledge.v1beta2 import identity_knowledge_api_pb2_grpc as knowledge_pb2_grpc
from indykite_sdk.utils import credentials_config
from indykite_sdk.model.token import TokenSource, Token


TIMEDELTA_REGEX = (r'((?P<days>-?\d+)d)?'
                   r'((?P<hours>-?\d+)h)?'
                   r'((?P<minutes>-?\d+)m)?')
TIMEDELTA_PATTERN = re.compile(TIMEDELTA_REGEX, re.IGNORECASE)


def create_agent_jwt(credentials, client="identity"):
    jwk = credentials.get('privateKeyJWK')
    key = JsonWebKey.import_key(jwk)
    message = create_jwt_message(credentials, client)
    jwt_token = jwt.encode({
            'alg': 'ES256',
            'cty': 'JWT',
            'kid': jwk['kid']
    }, message, key)
    return jwt_token


def create_jwt_message(credentials, client):
    token_lifetime = None
    now = datetime.now()
    current_time = int(time.time())
    time_2min = current_time + 120
    time_day = current_time + 86400
    if "tokenLifetime" in credentials.keys():
        token_lifetime = get_int_from_datetime(now + parse_delta(credentials.get('tokenLifetime')))
    if not isinstance(token_lifetime, int) or token_lifetime < time_2min or token_lifetime > time_day:
        token_lifetime = get_int_from_datetime(now + timedelta(hours=1))
    if client == "config":
        message = {
                'exp': token_lifetime,
                'iat': get_int_from_datetime(now),
                'iss': credentials.get('serviceAccountId'),
                'jti': str(uuid.uuid4()),
                'sub': credentials.get('serviceAccountId'),
        }
    else:
        message = {
            'exp': token_lifetime,
            'iat': get_int_from_datetime(now),
            'iss': credentials.get('appAgentId'),
            'jti': str(uuid.uuid4()),
            'sub': credentials.get('appAgentId'),
        }
    return message


def get_credentials(client="identity", token_source=None):
    """
    get all credentials necessary info
    :param client: string
    :param token_source: TokenSource object
    :return: secure channel to a server, stub
    """
    try:
        credentials = credentials_config.lookup_env_credentials_variables(client)
        # create TokenSource if not exists or token not valid
        if not token_source:
            agent_token = create_agent_jwt(credentials, client)
            token_source = TokenSource()
            token_source = token_source.reusable_token_source(None, credentials)
            access_token_decode = jwt.decode(agent_token, credentials.get('privateKeyJWK'))
            token_source.token = Token(agent_token, "Bearer", access_token_decode.exp)
        if token_source.token:
            t = datetime.now().timestamp()
            # add 1 min because token will be issued every 1 minute by default
            expire_time_in_seconds = int(t) + 60
        if token_source.token is None or (token_source.token.expiry < expire_time_in_seconds):
            if token_source.reusable:
                agent_token = create_agent_jwt(credentials, client)
                access_token_decode = jwt.decode(agent_token, credentials.get('privateKeyJWK'))
                token_source.token = Token(agent_token, "Bearer", access_token_decode.exp)
            else:
                raise Exception("TokenSource is not reusable")
        else:
            agent_token = token_source.token.access_token

        call_credentials = grpc.access_token_call_credentials(agent_token.decode("utf-8"))
        certificate_path = certifi.where()
        endpoint = credentials.get("endpoint")

        with open(certificate_path, "rb") as cert_file:
            channel_credentials = grpc.ssl_channel_credentials(cert_file.read())

        composite_credentials = grpc.composite_channel_credentials(channel_credentials,
                                                                   call_credentials)

        channel = grpc.secure_channel(endpoint, composite_credentials)
        if client == "config":
            stub = config_pb2_grpc.ConfigManagementAPIStub(channel=channel)
        elif client == "ingest":
            stub = ingest_pb2_grpc.IngestAPIStub(channel=channel)
        elif client == "authz":
            stub = authz_pb2.AuthorizationAPIStub(channel=channel)
        elif client == "knowledge":
            stub = knowledge_pb2_grpc.IdentityKnowledgeAPIStub(channel=channel)
        else:
            stub = pb2_grpc.IdentityManagementAPIStub(channel=channel)
        return channel, stub, credentials, token_source

    except Exception as exception:
        tb = sys.exception().__traceback__
        raise exception(...).with_traceback(tb)


def get_int_from_datetime(dt):
    return int(time.mktime(dt.timetuple()))


def parse_delta(delta):
    # Parses a human readable timedelta (30m, 1d, 4h15m) into a datetime.timedelta
    match = TIMEDELTA_PATTERN.match(delta)
    if match:
        parts = {k: int(v) for k, v in match.groupdict().items() if v}
        return timedelta(**parts)
