import sys
import uuid
from indykite_sdk.indykite.knowledge.v1beta2 import identity_knowledge_api_pb2 as pb2
from indykite_sdk.indykite.knowledge.v1beta2 import model_pb2
from indykite_sdk.indykite.ingest.v1beta2 import model_pb2 as ingest_model_pb2
from indykite_sdk.model.identity_knowledge import IdentityKnowledgeReadResponse
import indykite_sdk.utils.logger as logger
from indykite_sdk.ingest import IngestClient


def identity_knowledge_read(self, query, input_params={}, returns=[]):
    """
    read ingested data
    :param self:
    :param query: string
    :param input_params: map{string, InputParam}
    :param returns: array of Identity Knowedge Returns
    :return: deserialized IdentityKnowledgeReadResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        identity_knowledge_response = self.stub.IdentityKnowledgeRead(
            pb2.IdentityKnowledgeReadRequest(
                query=query,
                input_params=request_input_params(input_params),
                returns=returns
            )
        )
        if not identity_knowledge_response:
            return None
        return IdentityKnowledgeReadResponse.deserialize(identity_knowledge_response)

    except Exception as exception:
        return logger.logger_error(exception)


def get_node_by_id(self, id , returns, is_identity=False):
    """
    read node by gid id
    :param self:
    :param id: string
    :param returns: array of Identity Knowledge Returns
    :param is_identity: boolean
    :return: Node
    """
    sys.excepthook = logger.handle_excepthook
    try:
        label = "Resource"
        if is_identity:
            label = "DigitalTwin"
        query: str = "MATCH (n:{flabel}) WHERE n.id=$id".format(flabel=label)
        params = {"id": id}
        identity_knowledge_response = self.stub.IdentityKnowledgeRead(
            pb2.IdentityKnowledgeReadRequest(
                    query=query,
                    input_params=request_input_params(params),
                    returns=returns
            )
        )
        if not identity_knowledge_response or len(identity_knowledge_response.nodes) == 0:
            return None
        if len(identity_knowledge_response.nodes) == 1:
            return identity_knowledge_response.nodes[0]
        else:
            raise Exception("Internal error: unable to complete request")
        return identity_knowledge_response
    except Exception as exception:
        return logger.logger_error(exception)


def get_node_by_identifier(self, external_id, type, returns, is_identity=False):
    """
    read node by identifier type + external_id
    :param self:
    :param external_id: string
    :param type: string
    :param returns: array of Identity Knowledge Returns
    :param is_identity: boolean
    :return: Node
    """
    sys.excepthook = logger.handle_excepthook
    try:
        label = "Resource"
        if is_identity:
            label = "DigitalTwin"
        query: str = "MATCH (n:{0}) WHERE n.external_id = '{1}' and n.type = '{2}'".format(
            label, external_id, type)
        params = {
            "external_id": external_id,
            "type": type
            }
        identity_knowledge_response = self.stub.IdentityKnowledgeRead(
            pb2.IdentityKnowledgeReadRequest(
                query=query,
                input_params=request_input_params(params),
                returns=returns
            )
        )
        if not identity_knowledge_response:
            return None
        return IdentityKnowledgeReadResponse.deserialize(identity_knowledge_response).nodes
    except Exception as exception:
        return logger.logger_error(exception)


def get_identity_by_id(self, id, returns):
    """
    get DT by id
    :param self:
    :param id: string
    :param returns: array of Identity Knowledge Returns
    :return: Node
    """
    node = self.get_node_by_id(id, returns, True)
    if not node:
        return None
    return node


def get_identity_by_identifier(self, external_id, type, returns):
    """
    get DT by identifier
    :param self:
    :param external_id: string
    :param type: string
    :param returns: array of Identity Knowledge Returns
    :return: Node
    """
    sys.excepthook = logger.handle_excepthook
    try:
        nodes = self.get_node_by_identifier(external_id, type, returns, True)
        if not nodes:
            return None
        return nodes

    except Exception as exception:
        return logger.logger_error(exception)


def list_nodes(self, returns, is_identity=False):
    """
    list all nodes, DTs like resources
    :param self:
    :param returns: array of Identity Knowledge Returns
    :param is_identity: boolean
    :return: list of Node objects
    """
    sys.excepthook = logger.handle_excepthook
    try:
        label = "Resource"
        if is_identity:
            label = "DigitalTwin"
        query: str = "MATCH (n:{0})".format(label)

        identity_knowledge_response = self.stub.IdentityKnowledgeRead(
            pb2.IdentityKnowledgeReadRequest(
                query=query,
                input_params={},
                returns=returns
            )
        )
        if not identity_knowledge_response:
            return None
        return IdentityKnowledgeReadResponse.deserialize(identity_knowledge_response).nodes
    except Exception as exception:
        return logger.logger_error(exception)


def list_nodes_by_property(self, property, returns, is_identity=False):
    """
    list all nodes, DTs like resources
    :param self:
    :param property: Knowledge Object Property
    :param returns: array of Identity Knowledge Returns
    :param is_identity: boolean
    :return: list of Node objects
    """
    sys.excepthook = logger.handle_excepthook
    try:
        (k, v), = property.items()
        label = "Resource"
        if is_identity:
            label = "DigitalTwin"
        query: str = "MATCH (n:{0}) WHERE n.{1} = ${2}".format(label, k, k)
        params = {k: v}
        identity_knowledge_response = self.stub.IdentityKnowledgeRead(
            pb2.IdentityKnowledgeReadRequest(
                query=query,
                input_params=request_input_params(params),
                returns=returns
            )
        )
        if not identity_knowledge_response:
            return None
        return IdentityKnowledgeReadResponse.deserialize(identity_knowledge_response).nodes
    except Exception as exception:
        return logger.logger_error(exception)


def list_identities(self, returns):
    """
    list all DTs
    :param self:
    :param returns: array of Identity Knowledge Returns
    :return: list of Node objects
    """
    nodes = self.list_nodes(returns, True)
    if not nodes:
        return None
    return nodes


def list_identities_by_property(self, property, returns):
    """
    list all identities
    :param property: dict
    :param returns: array of Identity Knowledge Returns
    :return: list of Node objects
    """
    nodes = self.list_nodes_by_property(property, returns, True)
    if not nodes:
        return None
    return nodes


def request_input_params(input_params):
    """
    transform into dict of format map<string InputParms>
    :param input_params: dict
    :return: dict input_params_dict
    """
    input_params_dict = {
        k: model_pb2.InputParam(string_value=str(v))
        for k, v in input_params.items()
    }
    return input_params_dict


def delete_all_with_node_type(self, node_type):
    """
    delete all nodes of defined type
    :param self:
    :param node_type: string in PascalCase
    :return: list of deleted responses
    """
    sys.excepthook = logger.handle_excepthook
    try:
        query: str = "MATCH (n:{0})".format(node_type)
        returns = [model_pb2.Return(variable="n")]
        identity_knowledge_response = self.stub.IdentityKnowledgeRead(
            pb2.IdentityKnowledgeReadRequest(
                query=query,
                input_params={},
                returns=returns
            )
        )
        if not identity_knowledge_response:
            return None
        records = []
        for node in identity_knowledge_response.nodes:
            node = ingest_model_pb2.NodeMatch(
                external_id=str(node.external_id),
                type=str(node.type)
            )
            delete = ingest_model_pb2.DeleteData(
                node=node
            )
            record = ingest_model_pb2.Record(
                id=str(uuid.uuid4()),
                delete=delete
            )
            records.append(record)
        client_ingest = IngestClient()
        if records:
            responses = client_ingest.stream_records(records)
            return responses
        return None
    except Exception as exception:
        return logger.logger_error(exception)
