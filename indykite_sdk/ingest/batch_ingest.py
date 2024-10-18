import sys

from indykite_sdk.indykite.ingest.v1beta3 import ingest_api_pb2 as pb2
from indykite_sdk.indykite.ingest.v1beta3 import model_pb2
from indykite_sdk.indykite.knowledge.objects.v1beta1 import ikg_pb2
from indykite_sdk.model.ingest_record import (BatchUpsertNodesResponse,
                                              BatchDeleteNodesResponse,
                                              BatchDeleteNodePropertiesResponse,
                                              BatchUpsertRelationshipsResponse,
                                              BatchDeleteRelationshipsResponse,
                                              BatchDeleteRelationshipPropertiesResponse,
                                              BatchDeleteNodeTagsResponse)
import indykite_sdk.utils.logger as logger


def batch_upsert_nodes(self, nodes):
    """
    ingest nodes up to 250
    :param self:
    :param nodes: Node array
    :return: array of info objects
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.BatchUpsertNodes(
            pb2.BatchUpsertNodesRequest(
                nodes=nodes
            )
        )
        if not response:
            return None
        return BatchUpsertNodesResponse.deserialize(response)
    except Exception as exception:
        return logger.logger_error(exception)


def batch_delete_nodes(self, nodes):
    """
    delete nodes up to 250
    :param self:
    :param nodes: NodeMatch array
    :return: array of info objects
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.BatchDeleteNodes(
            pb2.BatchDeleteNodesRequest(
                nodes=nodes
            )
        )
        if not response:
            return None
        return BatchDeleteNodesResponse.deserialize(response)
    except Exception as exception:
        return logger.logger_error(exception)


def batch_delete_node_properties(self, node_properties):
    """
    delete node properties up to 250
    :param self:
    :param node_properties: DeleteData.NodePropertyMatch array
    :return: array of info objects
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.BatchDeleteNodeProperties(
            pb2.BatchDeleteNodePropertiesRequest(
                node_properties=node_properties
            )
        )
        if not response:
            return None
        return BatchDeleteNodePropertiesResponse.deserialize(response)
    except Exception as exception:
        return logger.logger_error(exception)


def batch_upsert_relationships(self, relationships):
    """
    ingest relationships up to 250
    :param self:
    :param relationships: Relationship array
    :return: array of info objects
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.BatchUpsertRelationships(
            pb2.BatchUpsertRelationshipsRequest(
                relationships=relationships
            )
        )
        if not response:
            return None
        return BatchUpsertRelationshipsResponse.deserialize(response)
    except Exception as exception:
        return logger.logger_error(exception)


def batch_delete_relationships(self, relationships):
    """
    delete relationships up to 250
    :param self:
    :param relationships: Relationship array
    :return: array of info objects
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.BatchDeleteRelationships(
            pb2.BatchDeleteRelationshipsRequest(
                relationships=relationships
            )
        )
        if not response:
            return None
        return BatchDeleteRelationshipsResponse.deserialize(response)
    except Exception as exception:
        return logger.logger_error(exception)


def batch_delete_relationship_properties(self, relationship_properties):
    """
    delete relationship properties up to 250
    :param self:
    :param relationship_properties: DeleteData.RelationshipPropertyMatch array
    :return: array of info objects
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.BatchDeleteRelationshipProperties(
            pb2.BatchDeleteRelationshipPropertiesRequest(
                relationship_properties=relationship_properties
            )
        )
        if not response:
            return None
        return BatchDeleteRelationshipPropertiesResponse.deserialize(response)
    except Exception as exception:
        return logger.logger_error(exception)


def batch_delete_node_tags(self, node_tags):
    """
    delete node properties up to 250
    :param self:
    :param node_tags: DeleteData.NodeTagMatch array
    :return: array of info objects
    """
    sys.excepthook = logger.handle_excepthook
    try:
        response = self.stub.BatchDeleteNodeTags(
            pb2.BatchDeleteNodeTagsRequest(
                node_tags=node_tags
            )
        )
        if not response:
            return None
        return BatchDeleteNodeTagsResponse.deserialize(response)
    except Exception as exception:
        return logger.logger_error(exception)



def data_node(self,
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
        node = ikg_pb2.Node(
            id=str(id),
            external_id=str(external_id),
            type=str(type),
            tags=tags,
            properties=properties,
            is_identity=is_identity
        )
        return node
    except Exception as exception:
        return logger.logger_error(exception)


def data_relationship(self,
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
        relationship = model_pb2.Relationship(
            source=source_match,
            target=target_match,
            type=str(type),
            properties=properties
        )
        return relationship
    except Exception as exception:
        return logger.logger_error(exception)
