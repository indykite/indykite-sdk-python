from indykite_sdk.indykite.ingest.v1beta2 import ingest_api_pb2 as pb2
from indykite_sdk.indykite.ingest.v1beta2 import model_pb2
from indykite_sdk.model.ingest_record import IngestRecordResponse
import sys
import indykite_sdk.utils.logger as logger
from indykite_sdk.utils.message_to_value import arg_to_value


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


def upsert_data_node_digital_twin(self,
                                  external_id,
                                  type,
                                  tags=[],
                                  tenant_id="",
                                  identity_properties=[],
                                  properties=[]):
    """
    upsertData with digital twin
    :param self:
    :param external_id: id for client ref
    :param type:
    :param tags:
    :param tenant_id: tenant id of the DT
    :param identity_properties: List of IdentityProperty objects max 10
    :param properties: List of Property objects max 10
    :return: UpsertData object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        upsert = model_pb2.UpsertData(
            node=model_pb2.Node(
                digital_twin=model_pb2.DigitalTwin(
                    external_id=str(external_id),
                    type=str(type),
                    tags=tags,
                    tenant_id=str(tenant_id),
                    identity_properties=identity_properties,
                    properties=properties
                )
            )
        )
        return upsert
    except Exception as exception:
        return logger.logger_error(exception)


def identity_property(self, key, value):
    """
    create identity property
    :param self:
    :param key:
    :param value:
    :return: IdentityProperty object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        ip = model_pb2.IdentityProperty(
            key=str(key),
            value=arg_to_value(value)
            )
        return ip
    except Exception as exception:
        return logger.logger_error(exception)


def ingest_property(self, key, value):
    """
    create Property object
    :param self:
    :param key:
    :param value:
    :return: Property object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        ip = model_pb2.Property(
            key=str(key),
            value=arg_to_value(value)
            )
        return ip
    except Exception as exception:
        return logger.logger_error(exception)


def upsert_data_node_resource(self,
                              external_id,
                              type,
                              tags=[],
                              properties=[]):
    """
    upsertData with resource
    :param self:
    :param external_id: id for client reference
    :param type:
    :param tags:
    :param properties: List of Property objects max 10
    :return: upsertData object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        upsert = model_pb2.UpsertData(
            node=model_pb2.Node(
                resource=model_pb2.Resource(
                    external_id=str(external_id),
                    type=str(type),
                    tags=tags,
                    properties=properties
                )
            )
        )
        return upsert
    except Exception as exception:
        return logger.logger_error(exception)


def upsert_data_relation(self,
                         match,
                         properties=[]):
    """
    create upsertData with relation
    :param self:
    :param match: RelationMatch object
    :param properties: List of Property objects max 10
    :return: upsertData object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        upsert = model_pb2.UpsertData(
            relation=model_pb2.Relation(
                match=match,
                properties=properties
            )
        )
        return upsert
    except Exception as exception:
        return logger.logger_error(exception)


def relation_match(self, source_match, target_match, type=""):
    """
    create RelationMatch object
    :param self:
    :param source_match: NodeMatch
    :param target_match: NodeMatch
    :param type:
    :return: RelationMatch
    """
    sys.excepthook = logger.handle_excepthook
    try:
        rm = model_pb2.RelationMatch(
            source_match=source_match,
            target_match=target_match,
            type=str(type)
            )
        return rm
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


def node_property_match(self, match, key=""):
    """
    create DeleteData.NodePropertyMatch object
    :param self:
    :param match: NodeMatch object
    :param key: str
    :return: DeleteData.NodePropertyMatch
    """
    sys.excepthook = logger.handle_excepthook
    try:
        npm = model_pb2.DeleteData.NodePropertyMatch(
            match=match,
            key=str(key)
            )
        return npm
    except Exception as exception:
        return logger.logger_error(exception)


def relation_property_match(self, match, key=""):
    """
    create DeleteData.RelationPropertyMatch object
    :param self:
    :param match: RelationMatch object
    :param key: str
    :return: DeleteData.RelationPropertyMatch
    """
    sys.excepthook = logger.handle_excepthook
    try:
        npm = model_pb2.DeleteData.RelationPropertyMatch(
            match=match,
            key=str(key)
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


def delete_data_relation(self, relation):
    """
    create deleteData with relation
    :param self:
    :param relation RelationMatch object
    :return: deleteData object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        delete = model_pb2.DeleteData(
            relation=relation
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


def delete_data_relation_property(self, relation_property):
    """
    create deleteData with node
    :param self:
    :param relation_property RelationPropertyMatch object
    :return: deleteData object
    """
    sys.excepthook = logger.handle_excepthook
    try:
        delete = model_pb2.DeleteData(
            relation_property=relation_property
        )
        return delete
    except Exception as exception:
        return logger.logger_error(exception)
