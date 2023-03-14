import time
from indykite_sdk.config import ConfigClient
from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.model.create_config_node import CreateConfigNode
from indykite_sdk.model.update_config_node import UpdateConfigNode
from helpers import data


def test_read_config_node_success(capsys):
    client = ConfigClient()
    assert client is not None

    config_node_id = data.get_email_service_config_node_id()
    config_node = client.read_config_node(config_node_id)
    captured = capsys.readouterr()

    assert config_node is not None
    assert "invalid or expired access_token" not in captured.out


def test_read_config_node_empty():
    client = ConfigClient()
    assert client is not None

    config_node_id = data.get_email_service_config_node_id()

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


def test_create_email_service_config_node_success(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    customer_id = data.get_customer_id()
    email_service_config = data.get_email_service()

    config_node = client.create_email_service_config_node(customer_id,
                                                          "automation-"+right_now,
                                                          "Automation "+right_now,
                                                          "description",
                                                          email_service_config,
                                                          [])
    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)


def test_create_email_service_config_node_empty(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    customer_id = data.get_customer_id()
    email_service_config = data.get_email_service()

    def mocked_create_config_node(request: pb2.CreateConfigNodeRequest):
        return None

    client.stub.CreateConfigNode = mocked_create_config_node
    config_node = client.create_email_service_config_node(customer_id,
                                                          "automation-"+right_now,
                                                          "Automation "+right_now,
                                                          "description",
                                                          email_service_config,
                                                          [])

    assert config_node is None


def test_create_email_service_config_node_exception(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    customer_id = data.get_customer_id()
    config_node = client.create_email_service_config_node(customer_id,
                                                          "automation-"+right_now,
                                                          "Automation "+right_now,
                                                          "description",
                                                          "description",
                                                          [])

    captured = capsys.readouterr()
    assert "Message must be initialized with a dict: indykite.config.v1beta1.CreateConfigNodeRequest" in captured.err


def test_update_email_service_config_node_success(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    config_node_id = data.get_email_service_config_node_id()
    response = client.read_config_node(config_node_id)
    assert response is not None

    email_service_config = data.get_email_service()
    config_node_response = client.update_email_service_config_node(response.id,
                                                                   response.etag,
                                                                   "Automation "+right_now,
                                                                   "description "+right_now,
                                                                   email_service_config,
                                                                   [])

    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert config_node_response is not None
    assert isinstance(config_node_response, UpdateConfigNode)


def test_update_email_service_config_node_empty(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    config_node_id = data.get_email_service_config_node_id()
    response = client.read_config_node(config_node_id)
    assert response is not None

    email_service_config = data.get_email_service()

    def mocked_update_config_node(request: pb2.UpdateConfigNodeRequest):
        return None

    client.stub.UpdateConfigNode = mocked_update_config_node
    config_node_response = client.update_email_service_config_node(response.id,
                                                                   response.etag,
                                                                   "Automation "+right_now,
                                                                   "description "+right_now,
                                                                   email_service_config,
                                                                   [])

    assert config_node_response is None


def test_update_email_service_config_node_exception(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    config_node_id = data.get_email_service_config_node_id()
    response = client.read_config_node(config_node_id)
    assert response is not None

    config_node_response = client.update_email_service_config_node(response.id,
                                                                   response.etag,
                                                                   "Automation "+right_now,
                                                                   "description "+right_now,
                                                                   "description",
                                                                   [])

    captured = capsys.readouterr()
    assert "must be initialized with a dict: indykite.config.v1beta1.UpdateConfigNodeRequest" in captured.err


def test_del_config_node_success(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    customer_id = data.get_customer_id()
    email_service_config = data.get_email_service()

    config_node = client.create_email_service_config_node(customer_id,
                                                          "automation-" + right_now,
                                                          "Automation " + right_now,
                                                          "description",
                                                          email_service_config,
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


def test_create_auth_flow_config_node_success(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    app_space_id = data.get_app_space_id()
    auth_flow_config = data.get_auth_flow()

    config_node = client.create_auth_flow_config_node(app_space_id,
                                                      "automation-"+right_now,
                                                      "Automation "+right_now,
                                                      "description",
                                                      auth_flow_config,
                                                      [])
    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)


def test_create_auth_flow_config_node_empty(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    app_space_id = data.get_app_space_id()
    auth_flow_config = data.get_auth_flow()

    def mocked_create_config_node(request: pb2.CreateConfigNodeRequest):
        return None

    client.stub.CreateConfigNode = mocked_create_config_node
    config_node = client.create_auth_flow_config_node(app_space_id,
                                                      "automation-"+right_now,
                                                      "Automation "+right_now,
                                                      "description",
                                                      auth_flow_config,
                                                      [])

    assert config_node is None


def test_create_auth_flow_config_node_exception(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    app_space_id = data.get_app_space_id()
    config_node = client.create_auth_flow_config_node(app_space_id,
                                                      "automation-"+right_now,
                                                      "Automation "+right_now,
                                                      "description",
                                                      "description",
                                                      [])

    captured = capsys.readouterr()
    assert "Message must be initialized with a dict: indykite.config.v1beta1.CreateConfigNodeRequest" in captured.err


def test_update_auth_flow_config_node_success(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    config_node_id = data.get_auth_flow_config_node_id()
    response = client.read_config_node(config_node_id)
    assert response is not None

    auth_flow_config = data.get_auth_flow()
    config_node_response = client.update_auth_flow_config_node(response.id,
                                                               response.etag,
                                                               "Automation "+right_now,
                                                               "description "+right_now,
                                                               auth_flow_config,
                                                               [])

    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert config_node_response is not None
    assert isinstance(config_node_response, UpdateConfigNode)


def test_update_auth_flow_config_node_empty(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    config_node_id = data.get_auth_flow_config_node_id()
    response = client.read_config_node(config_node_id)
    assert response is not None

    auth_flow_config = data.get_auth_flow()

    def mocked_update_config_node(request: pb2.UpdateConfigNodeRequest):
        return None

    client.stub.UpdateConfigNode = mocked_update_config_node
    config_node_response = client.update_auth_flow_config_node(response.id,
                                                               response.etag,
                                                               "Automation " + right_now,
                                                               "description " + right_now,
                                                               auth_flow_config,
                                                               [])

    assert config_node_response is None


def test_update_auth_flow_config_node_exception(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    config_node_id = data.get_auth_flow_config_node_id()
    response = client.read_config_node(config_node_id)
    assert response is not None

    config_node_response = client.update_auth_flow_config_node(response.id,
                                                               response.etag,
                                                               "Automation "+right_now,
                                                               "description "+right_now,
                                                               "description",
                                                               [])

    captured = capsys.readouterr()
    assert "must be initialized with a dict: indykite.config.v1beta1.UpdateConfigNodeRequest" in captured.err


def test_create_oauth2_client_config_node_success(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    app_space_id = data.get_app_space_id()
    oauth2_client_config = data.get_oauth2_client()

    config_node = client.create_oauth2_client_config_node(app_space_id,
                                                          "automation-"+right_now,
                                                          "Automation "+right_now,
                                                          "description",
                                                          oauth2_client_config,
                                                          [])
    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)


def test_create_oauth2_client_config_node_empty(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    app_space_id = data.get_app_space_id()
    oauth2_client_config = data.get_oauth2_client()

    def mocked_create_config_node(request: pb2.CreateConfigNodeRequest):
        return None

    client.stub.CreateConfigNode = mocked_create_config_node
    config_node = client.create_oauth2_client_config_node(app_space_id,
                                                          "automation-"+right_now,
                                                          "Automation "+right_now,
                                                          "description",
                                                          oauth2_client_config,
                                                          [])

    assert config_node is None


def test_create_oauth2_client_config_node_exception(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    app_space_id = data.get_app_space_id()
    config_node = client.create_oauth2_client_config_node(app_space_id,
                                                          "automation-"+right_now,
                                                          "Automation "+right_now,
                                                          "description",
                                                          "description",
                                                          [])

    captured = capsys.readouterr()
    assert "Message must be initialized with a dict: indykite.config.v1beta1.CreateConfigNodeRequest" in captured.err


def test_update_oauth2_client_config_node_success(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    config_node_id = data.get_oauth2_client_config_node_id()
    response = client.read_config_node(config_node_id)
    assert response is not None

    oauth2_client_config = data.get_oauth2_client()
    config_node_response = client.update_oauth2_client_config_node(response.id,
                                                                   response.etag,
                                                                   "Automation "+right_now,
                                                                   "description "+right_now,
                                                                   oauth2_client_config,
                                                                   [])

    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert config_node_response is not None
    assert isinstance(config_node_response, UpdateConfigNode)


def test_update_oauth2_client_config_node_empty(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    config_node_id = data.get_oauth2_client_config_node_id()
    response = client.read_config_node(config_node_id)
    assert response is not None

    oauth2_client_config = data.get_oauth2_client()

    def mocked_update_config_node(request: pb2.UpdateConfigNodeRequest):
        return None

    client.stub.UpdateConfigNode = mocked_update_config_node
    config_node_response = client.update_oauth2_client_config_node(response.id,
                                                                   response.etag,
                                                                   "Automation " + right_now,
                                                                   "description " + right_now,
                                                                   oauth2_client_config,
                                                                   [])

    assert config_node_response is None


def test_update_oauth2_client_config_node_exception(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    config_node_id = data.get_oauth2_client_config_node_id()
    response = client.read_config_node(config_node_id)
    assert response is not None

    config_node_response = client.update_oauth2_client_config_node(response.id,
                                                                   response.etag,
                                                                   "Automation "+right_now,
                                                                   "description "+right_now,
                                                                   "description",
                                                                   [])

    captured = capsys.readouterr()
    assert "must be initialized with a dict: indykite.config.v1beta1.UpdateConfigNodeRequest" in captured.err


def test_create_ingest_mapping_config_node_success(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    app_space_id = data.get_app_space_id()
    ingest_mapping_config = data.get_ingest_mapping()

    config_node = client.create_ingest_mapping_config_node(app_space_id,
                                                           "automation-"+right_now,
                                                           "Automation "+right_now,
                                                           "description",
                                                           ingest_mapping_config,
                                                           [])
    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)


def test_create_ingest_mapping_config_node_empty(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    app_space_id = data.get_app_space_id()
    ingest_mapping_config = data.get_ingest_mapping()

    def mocked_create_config_node(request: pb2.CreateConfigNodeRequest):
        return None

    client.stub.CreateConfigNode = mocked_create_config_node
    config_node = client.create_ingest_mapping_config_node(app_space_id,
                                                           "automation-"+right_now,
                                                           "Automation "+right_now,
                                                           "description",
                                                           ingest_mapping_config,
                                                           [])

    assert config_node is None


def test_create_ingest_mapping_config_node_exception(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    app_space_id = data.get_app_space_id()
    config_node = client.create_ingest_mapping_config_node(app_space_id,
                                                           "automation-"+right_now,
                                                           "Automation "+right_now,
                                                           "description",
                                                           "description",
                                                           [])

    captured = capsys.readouterr()
    assert "Message must be initialized with a dict: indykite.config.v1beta1.CreateConfigNodeRequest" in captured.err


def test_update_ingest_mapping_config_node_success(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    config_node_id = data.get_ingest_mapping_config_node_id()
    response = client.read_config_node(config_node_id)
    assert response is not None

    ingest_mapping_config = data.get_ingest_mapping()
    config_node_response = client.update_ingest_mapping_config_node(response.id,
                                                                    response.etag,
                                                                    "Automation "+right_now,
                                                                    "description "+right_now,
                                                                    ingest_mapping_config,
                                                                    [])

    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert config_node_response is not None
    assert isinstance(config_node_response, UpdateConfigNode)


def test_update_ingest_mapping_config_node_empty(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    config_node_id = data.get_ingest_mapping_config_node_id()
    response = client.read_config_node(config_node_id)
    assert response is not None

    ingest_mapping_config = data.get_ingest_mapping()

    def mocked_update_config_node(request: pb2.UpdateConfigNodeRequest):
        return None

    client.stub.UpdateConfigNode = mocked_update_config_node
    config_node_response = client.update_ingest_mapping_config_node(response.id,
                                                                    response.etag,
                                                                    "Automation " + right_now,
                                                                    "description " + right_now,
                                                                    ingest_mapping_config,
                                                                    [])

    assert config_node_response is None


def test_update_ingest_mapping_config_node_exception(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    config_node_id = data.get_ingest_mapping_config_node_id()
    response = client.read_config_node(config_node_id)
    assert response is not None

    config_node_response = client.update_ingest_mapping_config_node(response.id,
                                                                    response.etag,
                                                                    "Automation "+right_now,
                                                                    "description "+right_now,
                                                                    "description",
                                                                    [])

    captured = capsys.readouterr()
    assert "must be initialized with a dict: indykite.config.v1beta1.UpdateConfigNodeRequest" in captured.err


def test_create_webauthn_provider_config_node_success(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    app_space_id = data.get_app_space_id()
    webauthn_provider_config = data.get_webauthn_provider()

    config_node = client.create_webauthn_provider_config_node(app_space_id,
                                                              "automation-"+right_now,
                                                              "Automation "+right_now,
                                                              "description",
                                                              webauthn_provider_config,
                                                              [])
    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)


def test_create_webauthn_provider_config_node_empty(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    app_space_id = data.get_app_space_id()
    webauthn_provider_config = data.get_webauthn_provider()

    def mocked_create_config_node(request: pb2.CreateConfigNodeRequest):
        return None

    client.stub.CreateConfigNode = mocked_create_config_node
    config_node = client.create_webauthn_provider_config_node(app_space_id,
                                                              "automation-"+right_now,
                                                              "Automation "+right_now,
                                                              "description",
                                                              webauthn_provider_config,
                                                              [])

    assert config_node is None


def test_create_webauthn_provider_config_node_exception(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    app_space_id = data.get_app_space_id()
    webauthn_provider_config = data.get_webauthn_provider_exception()
    config_node = client.create_webauthn_provider_config_node(app_space_id,
                                                              "automation-"+right_now,
                                                              "Automation "+right_now,
                                                              "description",
                                                              webauthn_provider_config,
                                                              [])

    captured = capsys.readouterr()
    assert "StatusCode.INVALID_ARGUMENT" in captured.err


def test_update_webauthn_provider_config_node_success(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    config_node_id = data.get_webauthn_provider_config_node_id()
    response = client.read_config_node(config_node_id)
    assert response is not None

    webauthn_provider_config = data.get_webauthn_provider()
    config_node_response = client.update_webauthn_provider_config_node(response.id,
                                                                       response.etag,
                                                                       "Automation "+right_now,
                                                                       "description "+right_now,
                                                                       webauthn_provider_config,
                                                                       [])

    captured = capsys.readouterr()

    assert "invalid or expired access_token" not in captured.out
    assert config_node_response is not None
    assert isinstance(config_node_response, UpdateConfigNode)


def test_update_webauthn_provider_config_node_empty(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    config_node_id = data.get_webauthn_provider_config_node_id()
    response = client.read_config_node(config_node_id)
    assert response is not None

    webauthn_provider_config = data.get_webauthn_provider()

    def mocked_update_config_node(request: pb2.UpdateConfigNodeRequest):
        return None

    client.stub.UpdateConfigNode = mocked_update_config_node
    config_node_response = client.update_webauthn_provider_config_node(response.id,
                                                                       response.etag,
                                                                       "Automation " + right_now,
                                                                       "description " + right_now,
                                                                       webauthn_provider_config,
                                                                       [])

    assert config_node_response is None


def test_update_webauthn_provider_config_node_exception(capsys):
    client = ConfigClient()
    assert client is not None

    right_now = str(int(time.time()))
    config_node_id = data.get_webauthn_provider_config_node_id()
    webauthn_provider_config = data.get_webauthn_provider_exception()
    response = client.read_config_node(config_node_id)
    assert response is not None

    config_node_response = client.update_webauthn_provider_config_node(response.id,
                                                                       response.etag,
                                                                       "Automation "+right_now,
                                                                       "description "+right_now,
                                                                       webauthn_provider_config,
                                                                       [])

    captured = capsys.readouterr()
    assert "StatusCode.INVALID_ARGUMENT" in captured.err
