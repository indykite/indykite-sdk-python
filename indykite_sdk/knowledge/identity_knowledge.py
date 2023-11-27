import sys
import uuid
from indykite_sdk.indykite.knowledge.v1beta1 import identity_knowledge_api_pb2 as pb2
from indykite_sdk.indykite.knowledge.v1beta1 import model_pb2
from indykite_sdk.indykite.ingest.v1beta2 import model_pb2 as ingest_model_pb2
from indykite_sdk.model.identity_knowledge import Path
import indykite_sdk.utils.logger as logger
from indykite_sdk.model.operation import Operation
from indykite_sdk.ingest import IngestClient


def read(self, path, conditions, input_params={}):
    """
    read ingested data
    :param self:
    :param path: string
    :param conditions: string
    :param input_params: map{string, InputParam}
    :return: array of IdentityKnowledgeResponse paths
    """
    sys.excepthook = logger.handle_excepthook
    try:
        identity_knowledge_response = self.stub.IdentityKnowledge(
            pb2.IdentityKnowledgeRequest(
                operation=Operation.OPERATION_READ.value,
                path=path,
                conditions=conditions,
                input_params=request_input_params(input_params),
            )
        )
        if not identity_knowledge_response:
            return []
        res = [Path.deserialize(path)
               for path in identity_knowledge_response.paths]
        return res

    except Exception as exception:
        return logger.logger_error(exception)


def get_node_by_id(self, id, node_type):
    """
    read node by gid id
    :param self:
    :param id: string
    :param node_type: string in PascalCase
    :return: Node
    """
    sys.excepthook = logger.handle_excepthook
    try:
        path: str = "(n:{0})".format(node_type)
        conditions: str = "WHERE n.{0} = ${1}".format("id", "id")
        params = {"id": id}
        identity_knowledge_response = self.stub.IdentityKnowledge(
            pb2.IdentityKnowledgeRequest(
                    operation=Operation.OPERATION_READ.value,
                    path=path,
                    conditions=conditions,
                    input_params=request_input_params(params),
            )
        )
        if not identity_knowledge_response or len(identity_knowledge_response.paths) == 0:
            return None
        if len(identity_knowledge_response.paths) == 1 and identity_knowledge_response.paths[0].nodes[0]:
            return identity_knowledge_response.paths[0].nodes[0]
        else:
            raise Exception("Internal error: unable to complete request")
    except Exception as exception:
        return logger.logger_error(exception)


def get_node_by_identifier(self, node_type, external_id, type):
    """
    read node by gid id
    :param self:
    :param node_type: string in PascalCase
    :param external_id: string
    :param type: string
    :return: Node
    """
    sys.excepthook = logger.handle_excepthook
    try:
        path: str = "(n:{0})".format(node_type)
        conditions: str = "WHERE n.{0} = ${1} and n.{2} = ${3}".format(
            "external_id", "external_id", "type", "type")
        params = {
            "external_id": external_id,
            "type": type
            }
        identity_knowledge_response = self.stub.IdentityKnowledge(
            pb2.IdentityKnowledgeRequest(
                    operation=Operation.OPERATION_READ.value,
                    path=path,
                    conditions=conditions,
                    input_params=request_input_params(params),
            )
        )
        if not identity_knowledge_response:
            return None
        responses = [Path.deserialize(path)
                     for path in identity_knowledge_response.paths]
        return parse_multiple_nodes_from_paths(responses)
    except Exception as exception:
        return logger.logger_error(exception)


def get_digital_twin_by_id(self, id):
    """
    get DT by id
    :param self:
    :param id: string
    :return: Node
    """
    node = self.get_node_by_id(id, "DigitalTwin")
    if not node:
        return None
    return node


def get_digital_twin_by_identifier(self, external_id, type):
    """
    get DT by identifier
    :param self:
    :param external_id: string
    :param type: string
    :return: Node
    """
    sys.excepthook = logger.handle_excepthook
    try:
        nodes = self.get_node_by_identifier("DigitalTwin", external_id, type)
        if not nodes:
            return None
        return nodes

    except Exception as exception:
        return logger.logger_error(exception)


def get_resource_by_id(self, id):
    """
    get DT by id
    :param self:
    :param id: string
    :return: Node
    """
    node = self.get_node_by_id(id, "Resource")
    if not node:
        return None
    return node


def get_resource_by_identifier(self, external_id, type):
    """
    get DT by identifier
    :param self:
    :param external_id: string
    :param type: string
    :return: Node
    """
    sys.excepthook = logger.handle_excepthook
    try:
        nodes = self.get_node_by_identifier("Resource", external_id, type)
        if not nodes:
            return None
        return nodes

    except Exception as exception:
        return logger.logger_error(exception)


def list_nodes(self, node_type):
    """
    list all nodes, DTs like resources
    :param self:
    :param node_type: string in PascalCase
    :return: list of Node objects
    """
    sys.excepthook = logger.handle_excepthook
    try:
        path: str = "(:{0})".format(node_type)
        identity_knowledge_response = self.stub.IdentityKnowledge(
            pb2.IdentityKnowledgeRequest(
                    operation=Operation.OPERATION_READ.value,
                    path=path
            )
        )
        if not identity_knowledge_response:
            return None
        responses = [Path.deserialize(path)
                     for path in identity_knowledge_response.paths]
        return parse_multiple_nodes_from_paths(responses)
    except Exception as exception:
        return logger.logger_error(exception)


def list_nodes_by_property(self, node_type, property):
    """
    list all nodes, DTs like resources
    :param self:
    :param node_type: string in PascalCase
    :return: list of Node objects
    """
    sys.excepthook = logger.handle_excepthook
    try:
        path: str = "(n:{0})".format(node_type)
        (k, v), = property.items()
        conditions: str = "WHERE n.{0} = ${1}".format(k, k)
        if not isinstance(v, int) and not isinstance(v, str):
            raise Exception("InvalidArgument: only string or integer properties can be used for queries")
        params = {k: v}
        identity_knowledge_response = self.stub.IdentityKnowledge(
            pb2.IdentityKnowledgeRequest(
                operation=Operation.OPERATION_READ.value,
                path=path,
                conditions=conditions,
                input_params=request_input_params(params)
            )
        )
        if not identity_knowledge_response:
            return None
        responses = [Path.deserialize(path)
                     for path in identity_knowledge_response.paths]
        return parse_multiple_nodes_from_paths(responses)
    except Exception as exception:
        return logger.logger_error(exception)


def list_resources(self):
    """
    list all resources
    :param self:
    :return: list of Node objects
    """
    nodes = self.list_nodes("Resource")
    if not nodes:
        return None
    return nodes


def list_digital_twins(self):
    """
    list all DTs
    :param self:
    :return: list of Node objects
    """
    nodes = self.list_nodes("DigitalTwin")
    if not nodes:
        return None
    return nodes


def list_resources_by_property(self, property):
    """
    list all resources
    :param self:
    :param property: dict
    :return: list of Node objects
    """

    nodes = self.list_nodes_by_property("Resource", property)
    if not nodes:
        return None
    return nodes


def list_digital_twins_by_property(self, property):
    """
    list all DTs
    :param property: dict
    :return: list of Node objects
    """
    nodes = self.list_nodes_by_property("DigitalTwin", property)
    if not nodes:
        return None
    return nodes


def parse_multiple_nodes_from_paths(paths):
    """
    get nodes from paths
    :param paths IdentityKnowledgeRequest.paths
    :return: list of node objects
    """
    nodes = []
    for path in paths:
        nodes.append(path.nodes[0])
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
        path: str = "(:{0})".format(node_type)
        identity_knowledge_response = self.stub.IdentityKnowledge(
            pb2.IdentityKnowledgeRequest(
                    operation=Operation.OPERATION_READ.value,
                    path=path
            )
        )
        if not identity_knowledge_response:
            return None
        records = []
        for path in identity_knowledge_response.paths:
            for node in path.nodes:
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
