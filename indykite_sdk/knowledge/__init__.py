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
    from .identity_knowledge import (identity_knowledge_read, get_node_by_id, get_node_by_identifier,
                                     get_identity_by_id, get_identity_by_identifier,
                                     get_node_by_id, get_node_by_identifier,
                                     list_nodes_by_property, list_nodes,
                                     list_identities, list_identities_by_property,
                                     list_nodes_by_property, list_nodes_by_property,
                                     delete_all_with_node_type)
