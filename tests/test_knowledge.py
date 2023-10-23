import os

from indykite_sdk.indykite.knowledge.v1beta1 import identity_knowledge_api_pb2 as pb2
from indykite_sdk.model.identity_knowledge import Node
import indykite_sdk.utils.logger as logger
from indykite_sdk.knowledge import KnowledgeClient
from indykite_sdk.ingest import IngestClient
from indykite_sdk.indykite.ingest.v1beta2 import model_pb2


def test_read_identity_knowledge_success():
    client = KnowledgeClient()
    assert client is not None
    input_params = {"external_id": os.getenv('ORGANIZATION_EXTERNAL_ID')}
    path = "(:Individual)-[:BELONGS_TO]->(n:Organization)"
    conditions = "WHERE n.external_id = $external_id"
    responses = client.read(path, conditions, input_params)
    for response in responses:
        assert response is not None


def test_read_identity_knowledge_empty():
    client = KnowledgeClient()
    assert client is not None
    input_params = {"external_id": os.getenv('ORGANIZATION_EXTERNAL_ID')}
    path = "(:Whatever)-[:BELONGS_TO]->(n:Organization)"
    conditions = "WHERE n.external_id = $external_id"
    responses = client.read(path, conditions, input_params)
    assert not responses


def test_read_identity_knowledge_exception(capsys):
    client = KnowledgeClient()
    assert client is not None
    input_params = []
    path = 3
    conditions = 2
    responses = client.read(path, conditions, input_params)
    captured = capsys.readouterr()
    assert "ERROR 'list' object has no attribute" in captured.err


def test_get_dt_by_id_success():
    client = KnowledgeClient()
    assert client is not None
    response = client.get_digital_twin_by_id(os.getenv('INDIVIDUAL_ID'))
    assert response.id == os.getenv('INDIVIDUAL_ID')


def test_get_dt_by_id_empty():
    client = KnowledgeClient()
    assert client is not None
    response = client.get_digital_twin_by_id(os.getenv('ORGANIZATION_ID'))
    assert response is None


def test_get_dt_by_id_exception(capsys):
    client = KnowledgeClient()
    assert client is not None
    response = client.get_digital_twin_by_id([])
    captured = capsys.readouterr()
    assert "invalid format for input param 'id'" in captured.err


def test_get_node_by_id_exception(capsys):
    client = KnowledgeClient()
    assert client is not None
    response = client.get_node_by_id([], "DigitalTwin")
    captured = capsys.readouterr()
    assert "invalid format for input param 'id'" in captured.err


def test_get_resource_by_id_success():
    client = KnowledgeClient()
    assert client is not None
    response = client.get_resource_by_id(os.getenv('ORGANIZATION_ID'))
    assert response.id == os.getenv('ORGANIZATION_ID')


def test_get_resource_by_id_empty():
    client = KnowledgeClient()
    assert client is not None
    response = client.get_resource_by_id(os.getenv('INDIVIDUAL_ID'))
    assert response is None


def test_get_resource_by_id_exception(capsys):
    client = KnowledgeClient()
    assert client is not None
    response = client.get_resource_by_id([])
    captured = capsys.readouterr()
    assert "invalid format for input param 'id'" in captured.err


def test_get_dt_by_identifier_success():
    client = KnowledgeClient()
    assert client is not None
    response = client.get_digital_twin_by_identifier(os.getenv('INDIVIDUAL_EXTERNAL_ID'), "Individual")
    assert response[0].external_id == os.getenv('INDIVIDUAL_EXTERNAL_ID')
    assert response[0].type == "individual"


def test_get_dt_by_identifier_empty():
    client = KnowledgeClient()
    assert client is not None
    response = client.get_digital_twin_by_identifier(os.getenv('ORGANIZATION_EXTERNAL_ID'), "Individual")
    assert response is None


def test_get_node_by_identifier_empty():
    client = KnowledgeClient()
    assert client is not None
    response = client.get_node_by_identifier("DigitalTwin", os.getenv('ORGANIZATION_EXTERNAL_ID'), "Individual")
    assert not response


def test_get_dt_by_identifier_exception(capsys):
    client = KnowledgeClient()
    assert client is not None

    def mocked_get_digital_twin_by_identifier(request: pb2.IdentityKnowledgeRequest):
        return logger.logger_error("missing 1 required positional argument")

    client.stub.IdentityKnowledge = mocked_get_digital_twin_by_identifier
    response = client.get_digital_twin_by_identifier(os.getenv('INDIVIDUAL_EXTERNAL_ID'), "Individual")
    captured = capsys.readouterr()
    assert "missing 1 required positional argument" in captured.err


def test_get_resource_by_identifier_success():
    client = KnowledgeClient()
    assert client is not None
    response = client.get_resource_by_identifier(os.getenv('ORGANIZATION_EXTERNAL_ID'), "Organization")
    assert response[0].external_id == os.getenv('ORGANIZATION_EXTERNAL_ID')
    assert response[0].type == "organization"


def test_get_resource_by_identifier_empty():
    client = KnowledgeClient()
    assert client is not None
    response = client.get_resource_by_identifier(os.getenv('INDIVIDUAL_EXTERNAL_ID'), "Organization")
    assert response is None


def test_get_resource_by_identifier_exception(capsys):
    client = KnowledgeClient()
    assert client is not None

    def mocked_get_resource_by_identifier(request: pb2.IdentityKnowledgeRequest):
        return logger.logger_error("missing 1 required positional argument")

    client.stub.IdentityKnowledge = mocked_get_resource_by_identifier
    response = client.get_resource_by_identifier(os.getenv('ORGANIZATION_EXTERNAL_ID'), "Organization")
    captured = capsys.readouterr()
    assert "missing 1 required positional argument" in captured.err


def test_list_resources_by_property_success():
    client = KnowledgeClient()
    assert client is not None
    response = client.list_resources_by_property({"colour": "blue"})
    assert response[0].external_id == os.getenv('ASSET_EXTERNAL_ID')
    assert response[0].type == "asset"


def test_list_resources_by_property_empty():
    client = KnowledgeClient()
    assert client is not None
    property = {"colour": "unknown"}
    response = client.list_resources_by_property(property)
    assert response is None


def test_list_resources_by_property_exception(capsys):
    client = KnowledgeClient()
    assert client is not None

    def mocked_list_resources_by_property(request: pb2.IdentityKnowledgeRequest):
        return logger.logger_error("missing 1 required positional argument")

    client.stub.IdentityKnowledge = mocked_list_resources_by_property
    response = client.list_resources_by_property({"colour": "gray"})
    captured = capsys.readouterr()
    assert "missing 1 required positional argument" in captured.err


def test_list_digital_twin_by_property_success():
    client = KnowledgeClient()
    assert client is not None
    response = client.list_digital_twins_by_property({"first_name": "renno"})
    assert response[0].external_id == os.getenv('INDIVIDUAL_EXTERNAL_ID')
    assert response[0].type == "individual"


def test_list_digital_twin_by_property_empty():
    client = KnowledgeClient()
    assert client is not None
    response = client.list_digital_twins_by_property({"last_name": "unknown"})
    assert response is None


def test_list_digital_twin_by_property_exception(capsys):
    client = KnowledgeClient()
    assert client is not None

    def mocked_list_digital_twin_by_property(request: pb2.IdentityKnowledgeRequest):
        return logger.logger_error("missing 1 required positional argument")

    client.stub.IdentityKnowledge = mocked_list_digital_twin_by_property
    response = client.list_digital_twins_by_property({"last_name": "mushu"})
    captured = capsys.readouterr()
    assert "missing 1 required positional argument" in captured.err


def test_list_resources_success():
    client = KnowledgeClient()
    assert client is not None
    response = client.list_resources()
    assert response[0].type == "asset" or "organization"


def test_list_resources_empty():
    client = KnowledgeClient()
    assert client is not None

    def mocked_list_resources(request: pb2.IdentityKnowledgeRequest):
        return None

    client.stub.IdentityKnowledge = mocked_list_resources
    response = client.list_resources()
    assert response is None


def test_list_resources_exception(capsys):
    client = KnowledgeClient()
    assert client is not None

    def mocked_list_resources(request: pb2.IdentityKnowledgeRequest):
        return logger.logger_error("missing 1 required positional argument")

    client.stub.IdentityKnowledge = mocked_list_resources
    response = client.list_resources()
    captured = capsys.readouterr()
    assert "missing 1 required positional argument" in captured.err


def test_list_digital_twin_success():
    client = KnowledgeClient()
    assert client is not None
    response = client.list_digital_twins()
    assert response[0].type == "individual" or "carowner"


def test_list_digital_twin_empty():
    client = KnowledgeClient()
    assert client is not None

    def mocked_list_digital_twin(request: pb2.IdentityKnowledgeRequest):
        return None

    client.stub.IdentityKnowledge = mocked_list_digital_twin
    response = client.list_digital_twins()
    assert response is None


def test_list_digital_twin_exception(capsys):
    client = KnowledgeClient()
    assert client is not None

    def mocked_list_digital_twin(request: pb2.IdentityKnowledgeRequest):
        return logger.logger_error("missing 1 required positional argument")

    client.stub.IdentityKnowledge = mocked_list_digital_twin
    response = client.list_digital_twins()
    captured = capsys.readouterr()
    assert "missing 1 required positional argument" in captured.err


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
    print(node1)
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
    print(node1)
    property = node1.get_property(node1, "unknown")
    assert property is None


def test_delete_empty():
    client = KnowledgeClient()
    assert client is not None
    responses = client.delete_all_with_node_type("whatever")
    assert responses is None


def test_delete_fail(capsys):
    client = KnowledgeClient()
    assert client is not None
    responses = client.delete_all_with_node_type("")
    captured = capsys.readouterr()
    assert "ERROR" in captured.err
