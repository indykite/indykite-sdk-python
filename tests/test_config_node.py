import time
from indykite_sdk.config import ConfigClient
from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.create_config_node import CreateConfigNode
from indykite_sdk.model.update_config_node import UpdateConfigNode
from helpers import data


def test_read_config_node_success(capsys):
    client = ConfigClient()
    assert client is not None

    config_node_id = data.get_authz_policy()
    config_node = client.read_config_node(config_node_id)
    captured = capsys.readouterr()

    assert config_node is not None
    assert "invalid or expired access_token" not in captured.out


def test_read_config_node_empty():
    client = ConfigClient()
    assert client is not None

    config_node_id = data.get_authz_policy()

    def mocked_read_config_node(request: pb2.ReadConfigNodeRequest):
        return None

    client.stub.ReadConfigNode = mocked_read_config_node
    config_node = client.read_config_node(config_node_id)

    assert config_node is None


def test_read_config_node_wrong_id(capsys):
    config_node_id = "aaaaaaaaaaaaaaa"

    client = ConfigClient()
    assert client is not None

    response = client.read_config_node(config_node_id)
    captured = capsys.readouterr()
    assert("invalid ReadConfigNodeRequest.Id: value length must be between 22 and 254 runes, inclusive" in captured.err)


def test_read_config_node_version_not_authz(capsys):
    client = ConfigClient()
    assert client is not None

    config_node_id = data.get_authz_policy()
    config_node = client.read_config_node(config_node_id, [], 0)
    captured = capsys.readouterr()

    assert config_node is not None
    assert "invalid or expired access_token" not in captured.out


def test_del_config_node_success(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    app_space_id = data.get_app_space_id()
    authorization_policy_config = data.get_authz_policy()

    config_node = client.create_authorization_policy_config_node(app_space_id,
                                                                 "automation-" + right_now,
                                                                 "Automation " + right_now,
                                                                 "description",
                                                                 authorization_policy_config,
                                                                 [])

    assert config_node is not None

    response = client.delete_config_node(config_node.id, config_node.etag, [] )
    captured = capsys.readouterr()
    assert response is not None


def test_del_config_node_empty(capsys):
    client = ConfigClient()
    assert client is not None

    id = "gid:AAAAAjLRnbbaJE53rrjm_NJXyO"
    etag = "HcQ77D8CUWV"

    def mocked_delete_config_node(request: pb2.DeleteConfigNodeRequest):
        return None

    client.stub.DeleteConfigNode = mocked_delete_config_node
    response = client.delete_config_node(id, etag, [])

    assert response is None


def test_create_authorization_policy_config_node_success(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    app_space_id = data.get_app_space_id()
    authorization_policy_config = data.get_authz_policy()

    config_node = client.create_authorization_policy_config_node(app_space_id,
                                                                 "automation-"+right_now,
                                                                 "Automation "+right_now,
                                                                 "description",
                                                                 authorization_policy_config,
                                                                 [])
    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)
    response = client.delete_config_node(config_node.id, config_node.etag, [])
    assert response.bookmark is not None


def test_create_authorization_policy_config_node_empty(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    app_space_id = data.get_app_space_id()
    authorization_policy_config = data.get_authz_policy()

    def mocked_create_config_node(request: pb2.CreateConfigNodeRequest):
        return None

    client.stub.CreateConfigNode = mocked_create_config_node
    config_node = client.create_authorization_policy_config_node(app_space_id,
                                                                 "automation-"+right_now,
                                                                 "Automation "+right_now,
                                                                 "description",
                                                                 authorization_policy_config,
                                                                 [])

    assert config_node is None


def test_create_authorization_policy_config_node_exception(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    app_space_id = data.get_app_space_id()
    config_node = client.create_authorization_policy_config_node(app_space_id,
                                                                 "automation-"+right_now,
                                                                 "Automation "+right_now,
                                                                 "description",
                                                                 "description",
                                                                 [])

    captured = capsys.readouterr()
    assert "'str' object has no attribute 'status'" in captured.err


def test_update_authorization_policy_config_node_success(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    config_node_id = data.get_authz_policy_config_node_id()
    response = client.read_config_node(config_node_id)
    assert response is not None

    authorization_policy_config = data.get_authz_policy()
    config_node_response = client.update_authorization_policy_config_node(response.id,
                                                                          response.etag,
                                                                          "Automation "+right_now,
                                                                          "description "+right_now,
                                                                          authorization_policy_config,
                                                                          [])

    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert config_node_response is not None
    assert isinstance(config_node_response, UpdateConfigNode)


def test_update_authorization_policy_config_node_empty(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    config_node_id = data.get_authz_policy_config_node_id()
    response = client.read_config_node(config_node_id)
    assert response is not None

    authorization_policy_config = data.get_authz_policy()

    def mocked_update_config_node(request: pb2.UpdateConfigNodeRequest):
        return None

    client.stub.UpdateConfigNode = mocked_update_config_node
    config_node_response = client.update_authorization_policy_config_node(response.id,
                                                                          response.etag,
                                                                          "Automation " + right_now,
                                                                          "description " + right_now,
                                                                          authorization_policy_config,
                                                                          [])

    assert config_node_response is None


def test_update_authorization_policy_config_node_exception(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    config_node_id = data.get_authz_policy_config_node_id()
    response = client.read_config_node(config_node_id)
    assert response is not None

    config_node_response = client.update_authorization_policy_config_node(response.id,
                                                                          response.etag,
                                                                          "Automation "+right_now,
                                                                          "description "+right_now,
                                                                          "description",
                                                                          [])

    captured = capsys.readouterr()
    assert "'str' object has no attribute 'status'" in captured.err


def test_create_consent_config_node_success(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    app_space_id = data.get_app_space_id()
    consent_config = data.get_consent_config()

    config_node = client.create_consent_config_node(app_space_id,
                                                    "automation-"+right_now,
                                                    "Automation "+right_now,
                                                    "description",
                                                    consent_config,
                                                    [])
    captured = capsys.readouterr()
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)
    response = client.delete_config_node(config_node.id, config_node.etag, [])
    assert response.bookmark is not None


def test_create_consent_config_node_empty(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    app_space_id = data.get_app_space_id()
    consent_config = data.get_consent_config()

    def mocked_create_config_node(request: pb2.CreateConfigNodeRequest):
        return None

    client.stub.CreateConfigNode = mocked_create_config_node
    config_node = client.create_consent_config_node(app_space_id,
                                                    "automation-"+right_now,
                                                    "Automation "+right_now,
                                                    "description",
                                                    consent_config,
                                                    [])

    assert config_node is None


def test_create_consent_config_node_exception(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    app_space_id = data.get_app_space_id()
    config_node = client.create_consent_config_node(app_space_id,
                                                    "automation-"+right_now,
                                                    "Automation "+right_now,
                                                    "description",
                                                    "description",
                                                    [])

    captured = capsys.readouterr()
    assert "Message must be initialized with a dict" in captured.err


def test_validate_authorization_policy_status(capsys):
    client = ConfigClient()
    assert client is not None
    response = client.validate_authorization_policy_status("wrong")
    captured = capsys.readouterr()
    assert "status must be a member of AuthorizationPolicyConfig.Status" in captured.err


def test_validate_data_points(capsys):
    client = ConfigClient()
    assert client is not None
    response = client.validate_data_points(False)
    captured = capsys.readouterr()
    assert "ERROR" in captured.err


def test_get_list_config_node_success(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    app_space_id = data.get_app_space_id()
    authorization_policy_config = data.get_authz_policy()

    config_node = client.create_authorization_policy_config_node(app_space_id,
                                                                 "automation-" + right_now,
                                                                 "Automation " + right_now,
                                                                 "description",
                                                                 authorization_policy_config,
                                                                 [])
    captured = capsys.readouterr()
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)
    config_node_id = config_node.id
    list_config_nodes = client.list_config_node_versions(config_node_id)
    assert list_config_nodes is not None
    assert list_config_nodes[0].id == config_node_id
    # assert list_config_nodes[0].version is not None
    response = client.delete_config_node(config_node.id, config_node.etag, [])
    assert response.bookmark is not None


def test_get_list_config_node_empty(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time() + 12))
    app_space_id = data.get_app_space_id()
    authorization_policy_config = data.get_authz_policy()

    config_node = client.create_authorization_policy_config_node(app_space_id,
                                                                 "automation-" + right_now,
                                                                 "Automation " + right_now,
                                                                 "description",
                                                                 authorization_policy_config,
                                                                 [])
    captured = capsys.readouterr()
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)
    config_node_id = config_node.id
    list_config_nodes = client.list_config_node_versions(config_node_id)
    assert list_config_nodes is not None
    response = client.delete_config_node(config_node.id, config_node.etag, [])
    assert response.bookmark is not None


def test_get_list_config_node_exception(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time() + 15))
    app_space_id = data.get_app_space_id()
    authorization_policy_config = data.get_authz_policy()
    config_node = client.create_authorization_policy_config_node(app_space_id,
                                                                 "automation-" + right_now,
                                                                 "Automation " + right_now,
                                                                 "description",
                                                                 authorization_policy_config,
                                                                 [])
    captured = capsys.readouterr()
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)
    config_node_id = config_node.id
    list_config_nodes = client.list_config_node_versions(app_space_id)
    assert "" in captured.err
    response = client.delete_config_node(config_node.id, config_node.etag, [])
    assert response.bookmark is not None
