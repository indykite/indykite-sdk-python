from datetime import datetime
import os
import pytest

from indykite_sdk.indykite.knowledge.v1beta2 import identity_knowledge_api_pb2 as pb2
from indykite_sdk.model.identity_knowledge import Metadata, Node
import indykite_sdk.utils.logger as logger
from indykite_sdk.knowledge import KnowledgeClient
from indykite_sdk.indykite.knowledge.v1beta2.model_pb2 import Return as ReturnKnowledge
from indykite_sdk.indykite.objects.v1beta2 import value_pb2


@pytest.fixture
def client():
    return KnowledgeClient()


def test_read_identity_knowledge_success(client):
    input_params = {"external_id": os.getenv('ORGANIZATION_EXTERNAL_ID')}
    query = "MATCH (n:Individual)-[:BELONGS_TO]->(n:Organization) WHERE n.external_id = $external_id"
    returns = [ReturnKnowledge(variable="n")]
    response = client.identity_knowledge_read(query, input_params, returns)
    assert response is not None


def test_read_identity_knowledge_empty(client):
    input_params = {"external_id": "VJnoVVgnVVVViMg"}
    query = "MATCH (n:Resource) WHERE n.external_id = $external_id"
    returns = [ReturnKnowledge(variable="n")]
    response = client.identity_knowledge_read(query, input_params, returns)
    assert len(response.nodes) == 0


def test_read_identity_knowledge_exception(client, capsys):
    input_params = []
    query = 3
    returns = [ReturnKnowledge(variable="n")]
    responses = client.identity_knowledge_read(query, input_params, returns)
    captured = capsys.readouterr()
    assert "ERROR 'list' object has no attribute" in captured.err


def test_get_identity_by_id_success(client):
    response = client.get_identity_by_id(os.getenv('INDIVIDUAL_ID'))
    assert response.id == os.getenv('INDIVIDUAL_ID')


def test_get_identity_by_id_empty(client):
    response = client.get_identity_by_id("gid:AAAAFRv0C-BcFVoVqfl623K8vvv")
    assert response is None


def test_get_identity_by_id_exception(client, capsys):
    response = client.get_identity_by_id("")
    captured = capsys.readouterr()
    assert "id is missing" in captured.err


def test_get_node_by_id_exception(client, capsys):
    response = client.get_node_by_id("")
    captured = capsys.readouterr()
    assert "id is missing" in captured.err


def test_get_node_by_id_success(client):
    response = client.get_node_by_id(os.getenv('ORGANIZATION_ID'))
    assert response.id == os.getenv('ORGANIZATION_ID')


def test_get_node_by_id_empty(client):
    response = client.get_node_by_id("gid:AAAAFRv0C-BcFVoVqfl623K8vvv")
    assert response is None


def test_get_identity_by_identifier_success(client):
    response = client.get_identity_by_identifier(os.getenv('INDIVIDUAL_EXTERNAL_ID'), "Person")
    assert response[0].external_id == os.getenv('INDIVIDUAL_EXTERNAL_ID')
    assert response[0].type == "Person" or "Whatever"


def test_get_identity_by_identifier_empty(client):
    response = client.get_identity_by_identifier(os.getenv('ORGANIZATION_EXTERNAL_ID'), "Individual")
    assert response is None


def test_get_node_by_identifier_empty(client):
    response = client.get_node_by_identifier(os.getenv('ORGANIZATION_EXTERNAL_ID'), "Individual", True)
    assert not response


def test_get_identity_by_identifier_exception(client, capsys):

    def mocked_get_identity_by_identifier(request: pb2.IdentityKnowledgeReadRequest):
        return logger.logger_error("missing 1 required positional argument: 'returns'")

    client.stub.IdentityKnowledgeRead = mocked_get_identity_by_identifier
    response = client.get_identity_by_identifier(os.getenv('INDIVIDUAL_EXTERNAL_ID'), "Individual")
    captured = capsys.readouterr()
    assert "missing 1 required positional argument: 'returns'" in captured.err


def test_get_node_by_identifier_success(client):
    response = client.get_node_by_identifier(os.getenv('ORGANIZATION_EXTERNAL_ID'), "Organization")
    assert response[0].external_id == os.getenv('ORGANIZATION_EXTERNAL_ID')
    assert response[0].type == "Organization"


def test_get_node_by_identifier_empty(client):
    response = client.get_node_by_identifier("pVmaIfVVVglVVfx", "Organization")
    assert len(response) == 0


def test_list_nodes_by_property_success(client):
    response = client.list_nodes_by_property({"colour": "grey"})
    assert response[0].external_id == os.getenv('ASSET_EXTERNAL_ID')
    assert response[0].type == "Asset"


def test_list_nodes_by_property_empty(client):
    property = {"colour": "unknown"}
    response = client.list_nodes_by_property(property)
    assert len(response) == 0


def test_list_nodes_by_property_exception(client, capsys):

    def mocked_list_nodes_by_property(request: pb2.IdentityKnowledgeReadRequest):
        return logger.logger_error("Logging error")

    client.stub.IdentityKnowledge = mocked_list_nodes_by_property
    response = client.list_nodes_by_property({}, "Error")
    captured = capsys.readouterr()
    assert "Logging error" in captured.err


def test_list_identities_by_property_success(client):
    response = client.list_identities_by_property({"first_name": "darna"})
    assert response[0].external_id == os.getenv('INDIVIDUAL_EXTERNAL_ID')
    assert response[0].type == "Person"


def test_list_identities_by_property_empty(client):
    response = client.list_identities_by_property({"last_name": "unknown"})
    assert response is None


def test_list_identities_by_property_exception(client, capsys):

    def mocked_list_identities_by_property(request: pb2.IdentityKnowledgeReadRequest):
        return logger.logger_error("invalid IdentityKnowledgeReadRequest.Returns")

    client.stub.IdentityKnowledgeRead = mocked_list_identities_by_property
    response = client.list_identities_by_property({"last_name": "mushu"})
    captured = capsys.readouterr()
    assert "invalid IdentityKnowledgeReadRequest.Returns" in captured.err


def test_list_nodes_empty(client):

    def mocked_list_resources(request: pb2.IdentityKnowledgeReadRequest):
        return None

    client.stub.IdentityKnowledgeRead = mocked_list_resources
    response = client.list_nodes()
    assert response is None


def test_list_nodes_exception(client, capsys):

    def mocked_list_resources(request: pb2.IdentityKnowledgeReadRequest):
        return logger.logger_error("invalid IdentityKnowledgeReadRequest.Returns")

    client.stub.IdentityKnowledgeRead = mocked_list_resources
    response = client.list_nodes([])
    captured = capsys.readouterr()
    assert "invalid IdentityKnowledgeReadRequest.Returns" in captured.err


def test_list_identities_empty(client):

    def mocked_list_identity_node(request: pb2.IdentityKnowledgeReadRequest):
        return None

    client.stub.IdentityKnowledgeRead = mocked_list_identity_node
    response = client.list_identities()
    assert response is None


def test_list_identities_exception(client, capsys):

    def mocked_list_identity_node(request: pb2.IdentityKnowledgeReadRequest):
        return logger.logger_error("list_identities() takes 1 positional argument but 2 were given")

    client.stub.IdentityKnowledgeRead = mocked_list_identity_node
    response = client.list_identities()
    captured = capsys.readouterr()
    assert "list_identities() takes 1 positional argument but 2 were given" in captured.err


def test_get_metadata_success():
    metadata1 = Metadata(
        assurance_level=1,
        verification_time=datetime.now().timestamp(),
        source="Myself",
        custom_metadata={
            "customData": value_pb2.Value(string_value="customValue")
        }
    )
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
                },
                "metadata": metadata1
            }
        ])
    metadata = node1.get_metadata(node1, "last_name")
    assert metadata.source == "Myself"


def test_get_metadata_no_data():
    node1 = Node(
        id="gid:AAAAFVCygmDZtk8KtTtw9CBopC8",
        external_id="PEpkjOvUJQvqTFw",
        type="individual")
    metadata = node1.get_metadata(node1, "unknown")
    assert metadata is None

def test_get_external_value_no_data():
    node1 = Node(
        id="gid:AAAAFVCygmDZtk8KtTtw9CBopC8",
        external_id="PEpkjOvUJQvqTFw",
        type="individual")
    external_value = node1.get_external_value(node1, "unknown")
    assert external_value is None


def test_get_metadata_non_valid():
    metadata1 = Metadata(
        assurance_level=1,
        verification_time=datetime.now().timestamp(),
        source="Myself",
        custom_metadata={
            "customData": value_pb2.Value(string_value="customValue")
        }
    )
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
            },
            "metadata": metadata1
        }
        ]
    )
    metadata = node1.get_metadata(node1, "unknown")
    assert metadata is None


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
            },
            "metadata": {}
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


def test_delete_empty(client):
    responses = client.delete_all_with_node_type("whenever")
    assert responses is None


def test_delete_fail(client, capsys):
    responses = client.delete_all_with_node_type("")
    captured = capsys.readouterr()
    assert "ERROR" in captured.err
