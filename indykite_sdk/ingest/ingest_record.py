import sys

from indykite_sdk.indykite.ingest.v1beta3 import ingest_api_pb2 as pb2
from indykite_sdk.indykite.ingest.v1beta3 import model_pb2
from indykite_sdk.indykite.knowledge.objects.v1beta1 import ikg_pb2
from indykite_sdk.model.ingest_record import IngestRecordResponse
import indykite_sdk.utils.logger as logger
from indykite_sdk.utils.message_to_value import param_to_value
from indykite_sdk.utils import date_to_timestamp, timestamp_to_date


def ingest_record(self, record):
    """
    data ingestion
    :param self:
    :param record: Record object
    :return: record_error
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.IngestRecord(
            pb2.IngestRecordRequest(
                record=record
            )
        )
        if not response:
            return None
        return IngestRecordResponse.deserialize(response)

    except Exception as exception:
        return logger.logger_error(exception)


def record_upsert(self, id, upsert):
    """
    create record
    :param self:
    :param id: id record for client ref
    :param upsert: UpsertData object
    :return: record
    """
    sys.excepthook = logger.handle_excepthook
    try:
        record = model_pb2.Record(
            id=str(id),
            upsert=upsert
        )
        if not record:
            return None
        return record
    except Exception as exception:
        return logger.logger_error(exception)


def record_delete(self, id, delete):
    """
    create record
    :param self:
    :param id: id record for client ref
    :param delete: DeleteData object
    :return: record
    """
    sys.excepthook = logger.handle_excepthook
    try:
        record = model_pb2.Record(
            id=str(id),
            delete=delete
        )
        if not record:
            return None
        return record
    except Exception as exception:
        return logger.logger_error(exception)


def ingest_property(self, type, value, metadata=None):
    """
    create Property object
    :param self:
    :param type:
    :param value:
    :param metadata:MetadataObject
    :return: Property object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        if not type:
            raise Exception('type is missing')
        if not value:
            raise Exception('value is missing')
        ip = ikg_pb2.Property(
            type=str(type),
            value=param_to_value(value),
            metadata=metadata
            )
        return ip
    except Exception as exception:
        return logger.logger_error(exception)


def ingest_metadata(self,
                    assurance_level=None,
                    verification_time=None,
                    source=None,
                    custom_metadata={}):
    """
    create Metadata object
    :param self:
    :param assurance_level: 1,2,3
    :param verification_time: datetime
    :param source: string
    :param custom_metadata: dict
    :return: Metadata object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        custom_metadata_dict = {}
        if custom_metadata:
            custom_metadata_dict = {
                k: param_to_value(v)
                for k, v in custom_metadata.items()
             }
        ip = ikg_pb2.Metadata(
            assurance_level=assurance_level,
            verification_time=date_to_timestamp(verification_time),
            source=source,
            custom_metadata=custom_metadata_dict
            )
        return ip
    except Exception as exception:
        return logger.logger_error(exception)


def upsert_data_node(self,
                     external_id,
                     type,
                     tags=[],
                     properties=[],
                     id="",
                     is_identity=False):
    """
    upsertData with node
    :param self:
    :param external_id: id for client reference
    :param type: string
    :param tags: array of strings
    :param properties: List of Property objects max 10
    :param id: gid
    :param is_identity: boolean
    :return: upsertData object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        upsert = model_pb2.UpsertData(
            node=ikg_pb2.Node(
                id=str(id),
                external_id=str(external_id),
                type=str(type),
                tags=tags,
                properties=properties,
                is_identity=is_identity
            )
        )
        return upsert
    except Exception as exception:
        return logger.logger_error(exception)


def upsert_data_relationship(self,
                             source_match,
                             target_match,
                             type="",
                             properties=[]):
    """
    create upsertData with relation
    :param self:
    :param source_match: NodeMatch
    :param target_match: NodeMatch
    :param type: string
    :param properties: List of Property objects max 10
    :return: upsertData object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        upsert = model_pb2.UpsertData(
            relationship=model_pb2.Relationship(
                source=source_match,
                target=target_match,
                type=str(type),
                properties=properties
            )
        )
        return upsert
    except Exception as exception:
        return logger.logger_error(exception)


def node_match(self, external_id, type=""):
    """
    create NodeMatch object
    :param self:
    :param external_id: str
    :param type: str
    :return: NodeMatch
    """
    nm = model_pb2.NodeMatch(
        external_id=str(external_id),
        type=str(type)
        )
    return nm


def node_property_match(self, match, property_type=""):
    """
    create DeleteData.NodePropertyMatch object
    :param self:
    :param match: NodeMatch object
    :param property_type: str
    :return: DeleteData.NodePropertyMatch
    """
    sys.excepthook = logger.handle_excepthook
    try:
        npm = model_pb2.DeleteData.NodePropertyMatch(
            match=match,
            property_type=str(property_type)
            )
        return npm
    except Exception as exception:
        return logger.logger_error(exception)


def relationship_property_match(self, source, target, type, property_type=""):
    """
    create DeleteData.RelationshipPropertyMatch object
    :param self:
    :param source: NodeMatch object
    :param target: NodeMatch object
    :param type: str
    :param property_type: str
    :return: DeleteData.RelationshipPropertyMatch
    """
    sys.excepthook = logger.handle_excepthook
    try:
        npm = model_pb2.DeleteData.RelationshipPropertyMatch(
            source=source,
            target=target,
            type=type,
            property_type=str(property_type)
            )
        return npm
    except Exception as exception:
        return logger.logger_error(exception)


def delete_data_node(self, node):
    """
    create deleteData with node
    :param self:
    :param node NodeMatch object
    :return: deleteData object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        delete = model_pb2.DeleteData(
            node=node
        )
        return delete
    except Exception as exception:
        return logger.logger_error(exception)


def delete_data_relationship(self, relationship):
    """
    create deleteData with relation
    :param self:
    :param relationship is a Relationship object
    :return: deleteData object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        delete = model_pb2.DeleteData(
            relationship=relationship
        )
        return delete
    except Exception as exception:
        return logger.logger_error(exception)


def delete_data_node_property(self, node_property):
    """
    create deleteData with node_property
    :param self:
    :param node_property DeleteData.NodePropertyMatch object
    :return: deleteData object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        delete = model_pb2.DeleteData(
            node_property=node_property
        )
        return delete
    except Exception as exception:
        return logger.logger_error(exception)


def delete_data_relationship_property(self, relationship_property):
    """
    create deleteData with node
    :param self:
    :param relationship_property RelationshipPropertyMatch object
    :return: deleteData object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        delete = model_pb2.DeleteData(
            relationship_property=relationship_property
        )
        return delete
    except Exception as exception:
        return logger.logger_error(exception)
