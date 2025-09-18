import time

import pytest
from helpers import data

from indykite_sdk.config import ConfigClient
from indykite_sdk.indykite.config.v1beta1 import \
    config_management_api_pb2 as pb2
from indykite_sdk.model.application_agent import ApplicationAgent
from indykite_sdk.model.create_application_agent import CreateApplicationAgent
from indykite_sdk.model.update_application_agent import UpdateApplicationAgent


@pytest.fixture
def client():
    return ConfigClient()


@pytest.fixture
def application_id():
    return data.get_application_id()


@pytest.fixture
def application_agent_id():
    return data.get_application_agent_id()


@pytest.fixture
def app_space_id():
    return data.get_app_space_id()


def test_read_application_agent_by_id_wrong_id(client, capsys):
    application_agent_id = "aaaaaaaaaaaaaaa"
    response = client.read_application_agent_by_id(application_agent_id)
    captured = capsys.readouterr()
    assert (
        "invalid ReadApplicationAgentRequest.Id: value length must be between 22 and 254 runes, inclusive"
        in captured.err
    )


def test_read_application_agent_id_success(client, application_agent_id, capsys):
    application_agent = client.read_application_agent_by_id(application_agent_id)
    captured = capsys.readouterr()
    assert application_agent is not None
    assert "invalid or expired access_token" not in captured.out
    # assert isinstance(application_agent, ApplicationAgent)


def test_read_application_agent_by_id_empty(client, application_agent_id):
    def mocked_read_application_agent_by_id(request: pb2.ReadApplicationAgentRequest):
        return None

    client.stub.ReadApplicationAgent = mocked_read_application_agent_by_id
    application_agent = client.read_application_agent_by_id(application_agent_id)
    assert application_agent is None


def test_read_application_agent_by_name_wrong_name(client, app_space_id, capsys):
    application_agent_name = "aaaaaaaaaaaaaaa"
    response = client.read_application_agent_by_name(app_space_id, application_agent_name)
    captured = capsys.readouterr()
    assert "NOT_FOUND" in captured.err


def test_read_application_agent_by_name_wrong_app_space_id(client, capsys):
    application_agent_name = data.get_application_agent_name()
    app_space_id = "gid:AAAAAlrNh6beFUSNk6tTtka8dwg"
    response = client.read_application_agent_by_name(app_space_id, application_agent_name)
    captured = capsys.readouterr()
    assert "NOT_FOUND" in captured.err


def test_read_application_agent_by_name_wrong_app_space_size(client, capsys):
    application_agent_name = data.get_application_agent_name()
    app_space_id = "12546"
    response = client.read_application_agent_by_name(app_space_id, application_agent_name)
    captured = capsys.readouterr()
    assert "invalid ReadApplicationAgentRequest.Name" in captured.err


def test_read_application_agent_name_success(client, app_space_id, capsys):
    application_agent_name = data.get_application_agent_name()
    application_agent = client.read_application_agent_by_name(app_space_id, application_agent_name)
    captured = capsys.readouterr()
    assert application_agent is not None
    assert "invalid or expired access_token" not in captured.out
    assert isinstance(application_agent, ApplicationAgent)


def test_read_application_agent_by_name_empty(client, app_space_id):
    application_agent_name = data.get_application_agent_name()

    def mocked_read_application_agent_by_name(request: pb2.ReadApplicationAgentRequest):
        return None

    client.stub.ReadApplicationAgent = mocked_read_application_agent_by_name
    application_agent = client.read_application_agent_by_name(app_space_id, application_agent_name)
    assert application_agent is None


def test_create_application_agent_success(client, application_id, capsys):
    right_now = str(int(time.time()))
    application_agent = client.create_application_agent(
        application_id,
        "automation-" + right_now,
        "Automation " + right_now,
        "description",
        ["Authorization", "Capture"],
    )
    captured = capsys.readouterr()
    assert "invalid or expired access_token" not in captured.out
    assert application_agent is not None
    assert isinstance(application_agent, CreateApplicationAgent)
    response = client.delete_application_agent(application_agent.id, application_agent.etag)


def test_create_application_agent_empty(client, application_id):
    right_now = str(int(time.time()))

    def mocked_create_application_agent(request: pb2.CreateApplicationAgentRequest):
        return None

    client.stub.CreateApplicationAgent = mocked_create_application_agent
    application_agent = client.create_application_agent(
        application_id,
        "automation-" + right_now,
        "Automation " + right_now,
        "description",
        ["Authorization", "Capture"],
    )
    assert application_agent is None


def test_create_application_agent_already_exists(client, application_id, capsys):
    application_agent = client.create_application_agent(
        application_id, "appagentpython", "ApplicationAgent test sdk", "description", ["Authorization", "Capture"],
    )
    captured = capsys.readouterr()
    assert "config entity with given name already exist" in captured.err


def test_create_application_agent_fail_invalid_application_id(client, capsys):
    application_id = "gid:AAAAAdM5d45g4j5lIW1Ma1nFAA"
    application_agent = client.create_application_agent(
        application_id, "agent-sdk", "ApplicationAgent test", "description", ["Authorization", "Capture"],
    )
    captured = capsys.readouterr()
    assert "invalid id value was provided for application_id" in captured.err


def test_create_application_agent_name_fail_type_parameter(client, application_id, capsys):
    application_agent = client.create_application_agent(
        application_id, ["test"], "test create", "description", ["Authorization", "Capture"],
    )
    captured = capsys.readouterr()
    assert "bad argument type for built-in operation" in captured.err


def test_create_application_agent_no_permissions(client, application_id):
    right_now = str(int(time.time()))
    application_agent = client.create_application_agent(
        application_id, "automation-" + right_now, "Automation " + right_now, "description", [],
    )
    assert application_agent is None


def test_update_application_agent_success(client, app_space_id, capsys):
    application_agent_name = data.get_application_agent_name()
    response = client.read_application_agent_by_name(app_space_id, application_agent_name)
    assert response is not None
    application_agent = client.update_application_agent(
        response.id, response.etag, response.display_name, "description", ["Authorization", "Capture"],
    )
    captured = capsys.readouterr()
    assert "invalid or expired access_token" not in captured.out
    assert application_agent is not None
    assert isinstance(application_agent, UpdateApplicationAgent)


def test_update_application_agent_empty(client, app_space_id):
    application_agent_name = data.get_application_agent_name()
    response = client.read_application_agent_by_name(app_space_id, application_agent_name)
    assert response is not None

    def mocked_update_application_agent(request: pb2.UpdateApplicationAgentRequest):
        return None

    client.stub.UpdateApplicationAgent = mocked_update_application_agent
    application_agent = client.update_application_agent(
        response.id, response.etag, response.display_name, "description", ["Authorization", "Capture"],
    )
    assert application_agent is None


def test_update_application_agent_fail_invalid_application_agent(client, app_space_id, capsys):
    application_agent_name = data.get_application_agent_name()
    response = client.read_application_agent_by_name(app_space_id, application_agent_name)
    assert response is not None
    application_agent_id = "gid:AAAAAdM5dfh564j5lIW1Ma1nFAA"
    application_agent = client.update_application_agent(
        application_agent_id, response.etag, response.display_name, "description update", ["Authorization", "Capture"],
    )
    captured = capsys.readouterr()
    assert "invalid id value was provided for id" in captured.err


def test_update_application_agent_name_fail_type_parameter(client, application_agent_id, app_space_id, capsys):
    application_agent_name = data.get_application_agent_name()
    response = client.read_application_agent_by_name(app_space_id, application_agent_name)
    assert response is not None
    application_agent = client.update_application_agent(
        application_agent_id, [response.etag], response.display_name, "description", ["Authorization", "Capture"],
    )
    captured = capsys.readouterr()
    assert "bad argument type for built-in operation" in captured.err


def test_update_application_agent_no_permissions(client, app_space_id):
    application_agent_name = data.get_application_agent_name()
    response = client.read_application_agent_by_name(app_space_id, application_agent_name)
    assert response is not None
    application_agent = client.update_application_agent(
        response.id, response.etag, response.display_name, "description", [],
    )
    assert application_agent is None


def test_get_application_agent_list_success(client, app_space_id, capsys):
    application_agent_name = data.get_application_agent_name()
    match = []
    match.append(application_agent_name)
    application_agent = client.list_application_agents(app_space_id, match)
    captured = capsys.readouterr()
    assert application_agent is not None
    assert "invalid or expired access_token" not in captured.out


def test_get_application_agent_list_wrong_app_space(client, capsys):
    app_space_id = "gid:AAAAAXX66V2_Jk3kjCCPThMQGaw"
    application_agent_name = data.get_application_agent_name()
    match = []
    match.append(application_agent_name)
    application_agent = client.list_application_agents(app_space_id, match)
    captured = capsys.readouterr()
    assert "invalid id value was provided for app_space_id" in captured.err


def test_get_application_agent_list_wrong_type(client, app_space_id, capsys):
    match = "test-create"
    application_agent = client.list_application_agents(app_space_id, match)
    captured = capsys.readouterr()
    assert "value length must be between 2 and 254 runes" in captured.err


def test_get_application_agent_list_empty_match(client, app_space_id, capsys):
    match = []
    application_agent = client.list_application_agents(app_space_id, match)
    captured = capsys.readouterr()
    assert "value must contain at least 1 item" in captured.err


def test_get_application_agent_list_no_answer_match(client, app_space_id, capsys):
    application_agent_name = "test-creation"
    match = []
    match.append(application_agent_name)
    application_agent = client.list_application_agents(app_space_id, match)
    captured = capsys.readouterr()
    assert application_agent is not None
    assert application_agent == []


def test_get_application_agent_list_raise_exception(client, app_space_id, capsys):
    match = ""
    application_agent = client.list_application_agents(app_space_id, match)
    captured = capsys.readouterr()
    assert "value must contain at least 1 item" in captured.err


def test_get_application_agent_list_empty(client, app_space_id):
    application_agent_name = data.get_application_agent_name()
    match = []
    match.append(application_agent_name)

    def mocked_get_application_agent_list(request: pb2.ListApplicationAgentsRequest):
        return None

    client.stub.ListApplicationAgents = mocked_get_application_agent_list
    application_agent = client.list_application_agents(app_space_id, match)
    assert application_agent is None


def test_del_application_agent_success(client, application_id):
    right_now = str(int(time.time()))
    application_agent = client.create_application_agent(
        application_id,
        "automation-" + right_now,
        "Automation " + right_now,
        "description",
        ["Authorization", "Capture"],
    )
    assert application_agent is not None

    def mocked_delete_application_agent(request: pb2.DeleteApplicationAgentRequest):
        return ""

    client.stub.DeleteApplicationAgent = mocked_delete_application_agent
    response = client.delete_application_agent(application_agent.id, application_agent.etag)


def test_del_application_agent_wrong_application_agent_id(client, application_agent_id, capsys):
    response = client.delete_application_agent(application_agent_id, "oeprbUOYHUIYI75U")
    captured = capsys.readouterr()
    assert "invalid eTag value" in captured.err


def test_del_application_agent_empty(client):
    id = "gid:AAAAAjLRnbbaJE53rrjm_NJXyO"
    etag = "HcQ77D8CUWV"

    def mocked_delete_application_agent(request: pb2.DeleteApplicationAgentRequest):
        return None

    client.stub.DeleteApplicationAgent = mocked_delete_application_agent
    response = client.delete_application_agent(id, etag)
    assert response is None
