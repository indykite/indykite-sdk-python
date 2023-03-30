from datetime import datetime
import sys
from indykite_sdk.identity import helper
from indykite_sdk.utils.logger import handle_excepthook, logger_error
from authlib.jose import JsonWebKey, jwt


class Token:
    def __init__(self, access_token, token_type=None, expiry=None):
        self.access_token = access_token
        self.token_type = token_type
        self.expiry = expiry

    def valid(self):
        t = datetime.now().timestamp()
        expire_time_in_seconds = int(t) + (30 * 1000)
        return self.expiry > expire_time_in_seconds


class TokenSource:
    def __init__(self, token=None, reusable=False, credentials=None):
        self.token = token
        self.reusable = reusable
        self.credentials = credentials

    def get_application_token(self):
        sys.excepthook = handle_excepthook
        try:
            if self.token is None:
                if self.reusable:
                    access_token = helper.create_agent_jwt(self.credentials)
                    access_token_decode = jwt.decode(access_token, self.credentials.get('privateKeyJWK'))
                    self.token = Token(access_token, "Bearer", access_token_decode.exp)
                else:
                    raise Exception("HTTP Client has no generated token")
            if not self.token.valid and self.reusable:
                access_token = helper.create_agent_jwt(self.credentials)
                access_token_decode = jwt.decode(access_token, self.credentials.get('privateKeyJWK'))
                self.token = Token(access_token, "Bearer", access_token_decode.exp)
        except Exception as exception:
            return logger_error(exception)

    @staticmethod
    def reusable_token_source(self, token: Token | None = None,
                              credentials=None):
        return TokenSource(token, True, credentials)

    @staticmethod
    def static_token_source(self, token: Token | None = None,
                            credentials=None):
        return TokenSource(token, False, credentials)
