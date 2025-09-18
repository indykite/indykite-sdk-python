import sys
import uuid

from indykite_sdk.indykite.ingest.v1beta3 import model_pb2 as ingest_model_pb2
from indykite_sdk.indykite.knowledge.v1beta2 import identity_knowledge_api_pb2 as pb2
from indykite_sdk.indykite.knowledge.v1beta2 import model_pb2
from indykite_sdk.ingest import IngestClient
from indykite_sdk.model.identity_knowledge import IdentityKnowledgeReadResponse
from indykite_sdk.utils import logger
from indykite_sdk.utils.message_to_value import param_to_value


def identity_knowledge_read(self, query, input_params={}, returns=[]):
    """Read ingested data
    :param self:
    :param query: string
    :param input_params: map{string, indykite.objects.v1beta2.Value}
    :param returns: array of Identity Knowledge Return {string[1-50] variable, array of strings properties}
    :return: deserialized IdentityKnowledgeReadResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        identity_knowledge_response = self.stub.IdentityKnowledgeRead(
            pb2.IdentityKnowledgeReadRequest(
                query=query,
                input_params=request_input_params(input_params),
                returns=returns,
            ),
        )
        if not identity_knowledge_response:
            return None
        return IdentityKnowledgeReadResponse.deserialize(identity_knowledge_response)

    except Exception as exception:
        return logger.logger_error(exception)


def get_node_by_id(self, id, is_identity=False):
    """Read node by gid id
    :param self:
    :param id: string
    :param is_identity: boolean
    :return: Node
    """
    sys.excepthook = logger.handle_excepthook
    try:
        if not id:
            raise Exception("id is missing")
        label = "Resource"
        if is_identity:
            label = "DigitalTwin"
        query: str = f"MATCH (n:{label}) WHERE n.id=$id"
        params = {"id": id}
        returns = [model_pb2.Return(variable="n")]
        identity_knowledge_response = self.stub.IdentityKnowledgeRead(
            pb2.IdentityKnowledgeReadRequest(query=query, input_params=request_input_params(params), returns=returns),
        )
        if not identity_knowledge_response or len(identity_knowledge_response.nodes) == 0:
            return None
        if len(identity_knowledge_response.nodes) == 1:
            return identity_knowledge_response.nodes[0]
        raise Exception("Internal error: unable to complete request")
        return identity_knowledge_response
    except Exception as exception:
        return logger.logger_error(exception)


def get_node_by_identifier(self, external_id, type, is_identity=False):
    """Read node by identifier type + external_id
    :param self:
    :param external_id: string
    :param type: string
    :param is_identity: boolean
    :return: Node
    """
    sys.excepthook = logger.handle_excepthook
    try:
        label = "Resource"
        if is_identity:
            label = "DigitalTwin"
        query: str = f"MATCH (n:{label}) WHERE n.external_id = '{external_id!s}' and n.type = '{type!s}'"
        params = {"external_id": str(external_id), "type": str(type)}
        returns = [model_pb2.Return(variable="n")]
        identity_knowledge_response = self.stub.IdentityKnowledgeRead(
            pb2.IdentityKnowledgeReadRequest(query=query, input_params=request_input_params(params), returns=returns),
        )
        if not identity_knowledge_response:
            return None
        return IdentityKnowledgeReadResponse.deserialize(identity_knowledge_response).nodes
    except Exception as exception:
        return logger.logger_error(exception)


def get_identity_by_id(self, id):
    """Get DT by id
    :param self:
    :param id: string
    :return: Node
    """
    node = self.get_node_by_id(id, True)
    if not node:
        return None
    return node


def get_identity_by_identifier(self, external_id, type):
    """Get DT by identifier
    :param self:
    :param external_id: string
    :param type: string
    :return: Node
    """
    sys.excepthook = logger.handle_excepthook
    try:
        nodes = self.get_node_by_identifier(external_id, type, True)
        if not nodes:
            return None
        return nodes

    except Exception as exception:
        return logger.logger_error(exception)


def list_nodes(self, node_type="Resource"):
    """List all nodes, DTs like resources
    :param self:
    :param node_type: string
    :return: list of Node objects
    """
    sys.excepthook = logger.handle_excepthook
    try:
        label = node_type
        query: str = f"MATCH (n:{label})"
        returns = [model_pb2.Return(variable="n")]
        identity_knowledge_response = self.stub.IdentityKnowledgeRead(
            pb2.IdentityKnowledgeReadRequest(query=query, input_params={}, returns=returns),
        )
        if not identity_knowledge_response:
            return None
        return IdentityKnowledgeReadResponse.deserialize(identity_knowledge_response).nodes
    except Exception as exception:
        return logger.logger_error(exception)


def list_nodes_by_property(self, property, is_identity=False):
    """List all nodes, DTs like resources
    :param self:
    :param property: dict key/value
    :param is_identity: boolean
    :return: list of Node objects
    """
    sys.excepthook = logger.handle_excepthook
    try:
        ((k, v),) = property.items()
        label = "Resource"
        if is_identity:
            label = "DigitalTwin"
        query: str = f"MATCH (n:{label}) -[:HAS]->(p:Property) WHERE p.type = '{k!s}' and p.value = '{v}'"
        params = {k: v}
        returns = [model_pb2.Return(variable="n")]
        identity_knowledge_response = self.stub.IdentityKnowledgeRead(
            pb2.IdentityKnowledgeReadRequest(query=query, input_params=request_input_params(params), returns=returns),
        )
        if not identity_knowledge_response:
            return None
        return IdentityKnowledgeReadResponse.deserialize(identity_knowledge_response).nodes
    except Exception as exception:
        return logger.logger_error(exception)


def list_identities(self):
    """List all DTs
    :param self:
    :return: list of Node objects
    """
    nodes = self.list_nodes("DigitalTwin")
    if not nodes:
        return None
    return nodes


def list_identities_by_property(self, property):
    """List all identities
    :param property: dict
    :return: list of Node objects
    """
    nodes = self.list_nodes_by_property(property, True)
    if not nodes:
        return None
    return nodes


def request_input_params(input_params):
    """Transform into dict of format map<string InputParms>
    :param input_params: dict
    :return: dict input_params_dict
    """
    input_params_dict = {k: param_to_value(v) for k, v in input_params.items()}
    return input_params_dict


def delete_all_with_node_type(self, node_type):
    """Delete all nodes of defined type
    :param self:
    :param node_type: string in PascalCase
    :return: list of deleted responses
    """
    sys.excepthook = logger.handle_excepthook
    try:
        query: str = f"MATCH (n:{node_type})"
        returns = [model_pb2.Return(variable="n")]
        identity_knowledge_response = self.stub.IdentityKnowledgeRead(
            pb2.IdentityKnowledgeReadRequest(query=query, input_params={}, returns=returns),
        )
        if not identity_knowledge_response:
            return None
        records = []
        for node in identity_knowledge_response.nodes:
            node = ingest_model_pb2.NodeMatch(external_id=str(node.external_id), type=str(node.type))
            delete = ingest_model_pb2.DeleteData(node=node)
            record = ingest_model_pb2.Record(id=str(uuid.uuid4()), delete=delete)
            records.append(record)
        client_ingest = IngestClient()
        if records:
            responses = client_ingest.stream_records(records)
            return responses
        return None
    except Exception as exception:
        return logger.logger_error(exception)
