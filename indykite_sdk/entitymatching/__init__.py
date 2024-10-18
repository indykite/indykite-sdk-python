import sys
from indykite_sdk.utils import jwt_credentials
from indykite_sdk.utils.logger import handle_excepthook, logger_error


class EntityMatchingClient(object):

    def __init__(self, token_source=None):
        sys.excepthook = handle_excepthook
        try:
            self.channel, self.stub, self.credentials, self.token_source = jwt_credentials.get_credentials(
                client="entitymatching",
                token_source=token_source
            )
        except Exception as exception:
            return logger_error(exception)

    # Imported methods
    from .read_suggested_property_mapping import read_suggested_property_mapping
    from .run_entity_matching_pipeline import run_entity_matching_pipeline
