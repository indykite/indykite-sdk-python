import sys
from indykite_sdk.utils import jwt_credentials
from indykite_sdk.utils.logger import handle_excepthook, logger_error


class KnowledgeClient(object):

    def __init__(self, token_source=None):
        sys.excepthook = handle_excepthook
        try:
            self.channel, self.stub, self.credentials, self.token_source = jwt_credentials.get_credentials(
                client="knowledge",
                token_source=token_source
            )
        except Exception as exception:
            return logger_error(exception)

    # Imported methods,
    from .identity_knowledge import (read, get_node_by_id, get_node_by_identifier,
                                     get_digital_twin_by_id, get_digital_twin_by_identifier,
                                     get_resource_by_id, get_resource_by_identifier,
                                     parse_multiple_nodes_from_paths, list_nodes_by_property, list_nodes,
                                     list_resources, list_digital_twins,
                                     list_resources_by_property, list_digital_twins_by_property,
                                     delete_all_with_node_type)
