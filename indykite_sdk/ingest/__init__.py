import sys
from indykite_sdk.utils import jwt_credentials
from indykite_sdk.utils.logger import handle_excepthook, logger_error


class IngestClient(object):

    def __init__(self, token_source=None):
        sys.excepthook = handle_excepthook
        try:
            self.channel, self.stub, self.credentials, self.token_source = jwt_credentials.get_credentials(
                client="ingest",
                token_source=token_source
            )
        except Exception as exception:
            return logger_error(exception)

    # Imported methods
    from .ingest_record import ingest_record, upsert_data_node_digital_twin, identity_property, ingest_property, \
        upsert_data_node_resource, upsert_data_relation, relation_match, node_match, node_property_match, \
        relation_property_match, ingest_record, delete_data_node, delete_data_relation, delete_data_node_property, \
        delete_data_relation_property, record_upsert, record_delete
    from .stream_records import generate_records_request, stream_records
