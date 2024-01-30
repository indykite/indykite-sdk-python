import os

from indykite_sdk.indykite.knowledge.v1beta2 import identity_knowledge_api_pb2 as pb2
from indykite_sdk.model.identity_knowledge import Node
import indykite_sdk.utils.logger as logger
from indykite_sdk.knowledge import KnowledgeClient
from indykite_sdk.indykite.knowledge.v1beta2.model_pb2 import Return as ReturnKnowledge


def test_read_identity_knowledge_success():
    client = KnowledgeClient()
    assert client is not None
    input_params = {"external_id": os.getenv('ORGANIZATION_EXTERNAL_ID')}
    query = "MATCH (n:Individual)-[:BELONGS_TO]->(n:Organization) WHERE n.external_id = $external_id"
    returns = [ReturnKnowledge(variable="n")]
    response = client.identity_knowledge_read(query, input_params, returns)
    assert response is not None


def test_read_identity_knowledge_empty():
    client = KnowledgeClient()
    assert client is not None
    input_params = {"external_id": "VJnoVVgnVVVViMg"}
    query = "MATCH (n:Resource) WHERE n.external_id = $external_id"
    returns = [ReturnKnowledge(variable="n")]
    response = client.identity_knowledge_read(query, input_params, returns)
    assert len(response.nodes) == 0


def test_read_identity_knowledge_exception(capsys):
    client = KnowledgeClient()
    assert client is not None
    input_params = []
    query = 3
    returns = [ReturnKnowledge(variable="n")]
    responses = client.identity_knowledge_read(query, input_params, returns)
    captured = capsys.readouterr()
    assert "ERROR 'list' object has no attribute" in captured.err


def test_get_identity_by_id_success():
    client = KnowledgeClient()
    assert client is not None
    returns = [ReturnKnowledge(variable="n")]
    response = client.get_identity_by_id(os.getenv('INDIVIDUAL_ID'), returns)
    assert response.id == os.getenv('INDIVIDUAL_ID')


def test_get_identity_by_id_empty():
    client = KnowledgeClient()
    assert client is not None
    returns = [ReturnKnowledge(variable="n")]
    response = client.get_identity_by_id("gid:AAAAFRv0C-BcFVoVqfl623K8vvv", returns)
    assert response is None


def test_get_identity_by_id_exception(capsys):
    client = KnowledgeClient()
    assert client is not None
    response = client.get_identity_by_id([], [])
    captured = capsys.readouterr()
    assert "invalid IdentityKnowledgeReadRequest.Returns" in captured.err


def test_get_node_by_id_exception(capsys):
    client = KnowledgeClient()
    assert client is not None
    response = client.get_node_by_id([], [])
    captured = capsys.readouterr()
    assert "invalid format for input param 'id'" in captured.err


def test_get_node_by_id_success():
    client = KnowledgeClient()
    assert client is not None
    returns = [ReturnKnowledge(variable="n")]
    response = client.get_node_by_id(os.getenv('ORGANIZATION_ID'), returns)
    assert response.id == os.getenv('ORGANIZATION_ID')


def test_get_node_by_id_empty():
    client = KnowledgeClient()
    assert client is not None
    returns = [ReturnKnowledge(variable="n")]
    response = client.get_node_by_id("gid:AAAAFRv0C-BcFVoVqfl623K8vvv", returns)
    assert response is None


def test_get_node_by_id_exception(capsys):
    client = KnowledgeClient()
    assert client is not None
    response = client.get_node_by_id([], [], False)
    captured = capsys.readouterr()
    assert "invalid IdentityKnowledgeReadRequest.Returns" in captured.err


def test_get_identity_by_identifier_success():
    client = KnowledgeClient()
    assert client is not None
    returns = [ReturnKnowledge(variable="n")]
    response = client.get_identity_by_identifier(os.getenv('INDIVIDUAL_EXTERNAL_ID'), "Whatever", returns)
    assert response[0].external_id == os.getenv('INDIVIDUAL_EXTERNAL_ID')
    assert response[0].type == "Individual" or "Whatever"


def test_get_identity_by_identifier_empty():
    client = KnowledgeClient()
    assert client is not None
    returns = [ReturnKnowledge(variable="n")]
    response = client.get_identity_by_identifier(os.getenv('ORGANIZATION_EXTERNAL_ID'), "Individual", returns)
    assert response is None


def test_get_node_by_identifier_empty():
    client = KnowledgeClient()
    assert client is not None
    returns = [ReturnKnowledge(variable="n")]
    response = client.get_node_by_identifier(os.getenv('ORGANIZATION_EXTERNAL_ID'), "Individual", returns, True)
    assert not response


def test_get_identity_by_identifier_exception(capsys):
    client = KnowledgeClient()
    assert client is not None

    def mocked_get_identity_by_identifier(request: pb2.IdentityKnowledgeReadRequest):
        return logger.logger_error("missing 1 required positional argument: 'returns'")

    client.stub.IdentityKnowledgeRead = mocked_get_identity_by_identifier
    returns = [ReturnKnowledge(variable="n")]
    response = client.get_identity_by_identifier(os.getenv('INDIVIDUAL_EXTERNAL_ID'), "Individual", returns)
    captured = capsys.readouterr()
    assert "missing 1 required positional argument: 'returns'" in captured.err


def test_get_node_by_identifier_success():
    client = KnowledgeClient()
    assert client is not None
    returns = [ReturnKnowledge(variable="n")]
    response = client.get_node_by_identifier(os.getenv('ORGANIZATION_EXTERNAL_ID'), "Organization", returns)
    assert response[0].external_id == os.getenv('ORGANIZATION_EXTERNAL_ID')
    assert response[0].type == "Organization"


def test_get_node_by_identifier_empty():
    client = KnowledgeClient()
    assert client is not None
    returns = [ReturnKnowledge(variable="n")]
    response = client.get_node_by_identifier("pVmaIfVVVglVVfx", "Organization", returns)
    assert len(response) == 0


def test_get_node_by_identifier_exception(capsys):
    client = KnowledgeClient()
    assert client is not None

    def mocked_get_node_by_identifier(request: pb2.IdentityKnowledgeReadRequest):
        return logger.logger_error("invalid IdentityKnowledgeReadRequest.Returns")

    client.stub.IdentityKnowledge = mocked_get_node_by_identifier
    response = client.get_node_by_identifier(os.getenv('ORGANIZATION_EXTERNAL_ID'), "Organization", [])
    captured = capsys.readouterr()
    assert "invalid IdentityKnowledgeReadRequest.Returns" in captured.err


def test_list_nodes_by_property_success():
    client = KnowledgeClient()
    assert client is not None
    returns = [ReturnKnowledge(variable="n")]
    response = client.list_nodes_by_property({"colour": "white"}, returns)
    assert response[0].external_id == os.getenv('ASSET_EXTERNAL_ID')
    assert response[0].type == "Asset"


def test_list_nodes_by_property_empty():
    client = KnowledgeClient()
    assert client is not None
    property = {"colour": "unknown"}
    returns = [ReturnKnowledge(variable="n")]
    response = client.list_nodes_by_property(property, returns)
    assert len(response) == 0


def test_list_nodes_by_property_exception(capsys):
    client = KnowledgeClient()
    assert client is not None

    def mocked_list_nodes_by_property(request: pb2.IdentityKnowledgeReadRequest):
        return logger.logger_error("invalid IdentityKnowledgeReadRequest.Returns")

    client.stub.IdentityKnowledge = mocked_list_nodes_by_property
    response = client.list_nodes_by_property({"colour": "gray"}, [])
    captured = capsys.readouterr()
    assert "invalid IdentityKnowledgeReadRequest.Returns" in captured.err


def test_list_identities_by_property_success():
    client = KnowledgeClient()
    assert client is not None
    returns = [ReturnKnowledge(variable="n")]
    response = client.list_identities_by_property({"first_name": "jackson"}, returns)
    assert response[0].external_id == os.getenv('INDIVIDUAL_EXTERNAL_ID')
    assert response[0].type == "Individual" or "Whatever"


def test_list_identities_by_property_empty():
    client = KnowledgeClient()
    assert client is not None
    returns = [ReturnKnowledge(variable="n")]
    response = client.list_identities_by_property({"last_name": "unknown"}, returns)
    assert response is None


def test_list_identities_by_property_exception(capsys):
    client = KnowledgeClient()
    assert client is not None

    def mocked_list_identities_by_property(request: pb2.IdentityKnowledgeReadRequest):
        return logger.logger_error("invalid IdentityKnowledgeReadRequest.Returns")

    client.stub.IdentityKnowledgeRead = mocked_list_identities_by_property
    response = client.list_identities_by_property({"last_name": "mushu"}, [])
    captured = capsys.readouterr()
    assert "invalid IdentityKnowledgeReadRequest.Returns" in captured.err


def test_list_nodes_success():
    client = KnowledgeClient()
    assert client is not None
    returns = [ReturnKnowledge(variable="n")]
    response = client.list_nodes(returns)
    assert response[0].type == "Asset" or "Organization"


def test_list_nodes_empty():
    client = KnowledgeClient()
    assert client is not None

    def mocked_list_resources(request: pb2.IdentityKnowledgeReadRequest):
        return None

    client.stub.IdentityKnowledgeRead = mocked_list_resources
    returns = [ReturnKnowledge(variable="n")]
    response = client.list_nodes(returns)
    assert response is None


def test_list_nodes_exception(capsys):
    client = KnowledgeClient()
    assert client is not None

    def mocked_list_resources(request: pb2.IdentityKnowledgeReadRequest):
        return logger.logger_error("invalid IdentityKnowledgeReadRequest.Returns")

    client.stub.IdentityKnowledgeRead = mocked_list_resources
    response = client.list_nodes([])
    captured = capsys.readouterr()
    assert "invalid IdentityKnowledgeReadRequest.Returns" in captured.err


def test_list_identities_success():
    client = KnowledgeClient()
    assert client is not None
    returns = [ReturnKnowledge(variable="n")]
    response = client.list_identities(returns)
    assert response[0].type == "Individual" or "Carowner" or "Whatever"


def test_list_identities_empty():
    client = KnowledgeClient()
    assert client is not None

    def mocked_list_digital_twin(request: pb2.IdentityKnowledgeReadRequest):
        return None

    client.stub.IdentityKnowledgeRead = mocked_list_digital_twin
    returns = [ReturnKnowledge(variable="n")]
    response = client.list_identities(returns)
    assert response is None


def test_list_identities_exception(capsys):
    client = KnowledgeClient()
    assert client is not None

    def mocked_list_digital_twin(request: pb2.IdentityKnowledgeReadRequest):
        return logger.logger_error("invalid IdentityKnowledgeReadRequest.Returns")

    client.stub.IdentityKnowledgeRead = mocked_list_digital_twin
    response = client.list_identities([])
    captured = capsys.readouterr()
    assert "invalid IdentityKnowledgeReadRequest.Returns" in captured.err


def test_get_property_success():
    node1 = Node(
        id="gid:AAAAFVCygmDZtk8KtTtw9CBopC8",
        external_id="PEpkjOvUJQvqTFw",
        type="individual",
        tags=[],
        properties=[
        {
            "key": "last_name",
            "value": {
                "stringValue": "mushu"
            }
        }
        ])
    property = node1.get_property(node1, "last_name")
    assert property == "mushu"


def test_get_property_no_prop():
    node1 = Node(
        id="gid:AAAAFVCygmDZtk8KtTtw9CBopC8",
        external_id="PEpkjOvUJQvqTFw",
        type="individual")
    property = node1.get_property(node1,"unknown")
    assert property is None


def test_get_property_non_valid():
    node1 = Node(
        id="gid:AAAAFVCygmDZtk8KtTtw9CBopC8",
        external_id="PEpkjOvUJQvqTFw",
        type="individual",
        tags=[],
        properties=[
        {
            "key": "last_name",
            "value": {
                "stringValue": "mushu"
            }
        }
        ])
    property = node1.get_property(node1, "unknown")
    assert property is None


def test_delete_empty():
    client = KnowledgeClient()
    assert client is not None
    responses = client.delete_all_with_node_type("whenever")
    assert responses is None


def test_delete_fail(capsys):
    client = KnowledgeClient()
    assert client is not None
    responses = client.delete_all_with_node_type("")
    captured = capsys.readouterr()
    assert "ERROR" in captured.err
