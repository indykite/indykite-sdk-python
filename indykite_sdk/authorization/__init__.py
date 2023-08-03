import sys
from indykite_sdk.utils import jwt_credentials
from indykite_sdk.utils.logger import handle_excepthook, logger_error


class AuthorizationClient(object):

    def __init__(self, local=False, token_source=None):
        sys.excepthook = handle_excepthook
        try:
            self.channel, self.stub, self.credentials, self.token_source = jwt_credentials.get_credentials(
                client="authz",
                local=local,
                token_source=token_source
            )
        except Exception as exception:
            return logger_error(exception)
    # Imported methods
    from .is_authorized import is_authorized_token, is_authorized_digital_twin, is_authorized_property_filter
    from .what_authorized import what_authorized_token, what_authorized_digital_twin, what_authorized_property_filter
    from .who_authorized import who_authorized
