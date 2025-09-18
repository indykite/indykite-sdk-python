import sys

from indykite_sdk.utils import jwt_credentials
from indykite_sdk.utils.logger import handle_excepthook, logger_error


class IngestClient:
    def __init__(self, token_source=None):
        sys.excepthook = handle_excepthook
        try:
            self.channel, self.stub, self.credentials, self.token_source = jwt_credentials.get_credentials(
                client="ingest",
                token_source=token_source,
            )
        except Exception as exception:
            return logger_error(exception)

    # Imported methods
    from .batch_ingest import (
        batch_delete_node_properties,
        batch_delete_node_tags,
        batch_delete_nodes,
        batch_delete_relationship_properties,
        batch_delete_relationships,
        batch_upsert_nodes,
        batch_upsert_relationships,
        data_node,
        data_relationship,
    )
    from .ingest_record import (
        delete_data_node,
        delete_data_node_property,
        delete_data_relationship,
        delete_data_relationship_property,
        ingest_external_value,
        ingest_metadata,
        ingest_property,
        ingest_record,
        node_match,
        node_property_match,
        node_tag_match,
        record_delete,
        record_upsert,
        relationship_property_match,
        upsert_data_node,
        upsert_data_relationship,
    )
    from .stream_records import generate_records_request, stream_records
