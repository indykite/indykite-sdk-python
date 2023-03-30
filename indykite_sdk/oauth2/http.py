import sys
import indykite_sdk.utils.logger as logger
from indykite_sdk.model.token import TokenSource

"""
get_refreshable_token_source returns a token or an error.
Token must be safe for concurrent use by multiple routines.
The returned Token must not be modified.
"""


def get_refreshable_token_source(self, token_source, credentials):
    sys.excepthook = logger.handle_excepthook
    try:
        if credentials is None:
            raise Exception("Credentials not found")
            return None

        if token_source is None:
            token_source = TokenSource()
            token_source = token_source.reusable_token_source(self, None, credentials)
        token_source.get_application_token()
        return token_source

    except Exception as exception:
        return logger.logger_error(exception)


"""
get_http_client returns an authenticated HTTP client
that always injects a valid token.
   """


def get_http_client(self, token_source=None):
    sys.excepthook = logger.handle_excepthook
    try:
        credentials = self.get_credentials()
        token_source = get_refreshable_token_source(self, token_source, credentials)
        self.get_http(token_source)
        return self
    except Exception as exception:
        return logger.logger_error(exception)


def get_token(self):
    sys.excepthook = logger.handle_excepthook
    try:
        self.token_source.get_application_token()
        access_token = self.token_source.token.access_token
        return access_token.decode('utf-8')
    except Exception as exception:
        return logger.logger_error(exception)
