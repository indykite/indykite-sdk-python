import numpy as np
import pytest
import time

from indykite_sdk.config import ConfigClient
from indykite_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from indykite_sdk.indykite.config.v1beta1 import model_pb2
from indykite_sdk.model.create_config_node import CreateConfigNode
from indykite_sdk.model.update_config_node import UpdateConfigNode
from helpers import data


@pytest.fixture
def client():
    return ConfigClient()


@pytest.fixture
def right_now():
    return str(int(time.time()) + 2)


@pytest.fixture
def app_space_id():
    return data.get_app_space_id()


def test_read_config_node_success(client, capsys):
    config_node_id = data.get_authz_policy()
    config_node = client.read_config_node(config_node_id)
    captured = capsys.readouterr()
    assert config_node is not None
    assert "invalid or expired access_token" not in captured.out


def test_read_config_node_empty(client):
    config_node_id = data.get_authz_policy()

    def mocked_read_config_node(request: pb2.ReadConfigNodeRequest):
        return None

    client.stub.ReadConfigNode = mocked_read_config_node
    config_node = client.read_config_node(config_node_id)
    assert config_node is None


def test_read_config_node_wrong_id(client, capsys):
    config_node_id = "aaaaaaaaaaaaaaa"
    response = client.read_config_node(config_node_id)
    captured = capsys.readouterr()
    assert("invalid ReadConfigNodeRequest.Id: value length must be between 22 and 254 runes, inclusive" in captured.err)


def test_read_config_node_version_not_authz(client, capsys):
    config_node_id = data.get_authz_policy()
    config_node = client.read_config_node(config_node_id, 0)
    captured = capsys.readouterr()
    assert config_node is not None
    assert "invalid or expired access_token" not in captured.out


def test_del_config_node_success(client, right_now, app_space_id, capsys):
    authorization_policy_config = data.get_authz_policy()
    config_node = client.create_authorization_policy_config_node(app_space_id,
                                                                 "automation-" + right_now,
                                                                 "Automation " + right_now,
                                                                 "description",
                                                                 authorization_policy_config)

    assert config_node is not None
    response = client.delete_config_node(config_node.id, config_node.etag)
    captured = capsys.readouterr()
    assert response is not None


def test_del_config_node_empty(client, capsys):
    id = "gid:AAAAAjLRnbbaJE53rrjm_NJXyO"
    etag = "HcQ77D8CUWV"

    def mocked_delete_config_node(request: pb2.DeleteConfigNodeRequest):
        return None

    client.stub.DeleteConfigNode = mocked_delete_config_node
    response = client.delete_config_node(id, etag)
    assert response is None


def test_create_authorization_policy_config_node_success(client, right_now, app_space_id, capsys):
    authorization_policy_config = data.get_authz_policy()
    config_node = client.create_authorization_policy_config_node(app_space_id,
                                                                 "automation-"+right_now,
                                                                 "Automation "+right_now,
                                                                 "description",
                                                                 authorization_policy_config)
    captured = capsys.readouterr()
    assert "invalid or expired access_token" not in captured.out
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)
    response = client.delete_config_node(config_node.id, config_node.etag)


def test_create_authorization_policy_config_node_empty(client, right_now, app_space_id, capsys):
    authorization_policy_config = data.get_authz_policy()

    def mocked_create_config_node(request: pb2.CreateConfigNodeRequest):
        return None

    client.stub.CreateConfigNode = mocked_create_config_node
    config_node = client.create_authorization_policy_config_node(app_space_id,
                                                                 "automation-"+right_now,
                                                                 "Automation "+right_now,
                                                                 "description",
                                                                 authorization_policy_config)

    assert config_node is None


def test_create_authorization_policy_config_node_exception(client, right_now, app_space_id, capsys):
    config_node = client.create_authorization_policy_config_node(app_space_id,
                                                                 "automation-"+right_now,
                                                                 "Automation "+right_now,
                                                                 "description",
                                                                 "description")

    captured = capsys.readouterr()
    assert "'str' object has no attribute 'status'" in captured.err


def test_update_authorization_policy_config_node_success(client, right_now, capsys):
    config_node_id = data.get_authz_policy_config_node_id()
    response = client.read_config_node(config_node_id)
    assert response is not None
    authorization_policy_config = data.get_authz_policy()
    config_node_response = client.update_authorization_policy_config_node(response.id,
                                                                          response.etag,
                                                                          "Automation "+right_now,
                                                                          "description "+right_now,
                                                                          authorization_policy_config)

    captured = capsys.readouterr()
    assert "invalid or expired access_token" not in captured.out
    assert config_node_response is not None
    assert isinstance(config_node_response, UpdateConfigNode)


def test_update_authorization_policy_config_node_empty(client, right_now, capsys):
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
                                                                          authorization_policy_config)

    assert config_node_response is None


def test_update_authorization_policy_config_node_exception(client, right_now, capsys):
    config_node_id = data.get_authz_policy_config_node_id()
    response = client.read_config_node(config_node_id)
    assert response is not None
    config_node_response = client.update_authorization_policy_config_node(response.id,
                                                                          response.etag,
                                                                          "Automation "+right_now,
                                                                          "description "+right_now,
                                                                          "description")

    captured = capsys.readouterr()
    assert "'str' object has no attribute 'status'" in captured.err


def test_create_consent_config_node_success(client, right_now, app_space_id, capsys):
    consent_config = data.get_consent_config()
    config_node = client.create_consent_config_node(app_space_id,
                                                    "automation-"+right_now,
                                                    "Automation "+right_now,
                                                    "description",
                                                    consent_config)
    captured = capsys.readouterr()
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)
    response = client.delete_config_node(config_node.id, config_node.etag)
    assert response is not None


def test_create_consent_config_node_empty(client, right_now, app_space_id, capsys):
    consent_config = data.get_consent_config()

    def mocked_create_config_node(request: pb2.CreateConfigNodeRequest):
        return None

    client.stub.CreateConfigNode = mocked_create_config_node
    config_node = client.create_consent_config_node(app_space_id,
                                                    "automation-"+right_now,
                                                    "Automation "+right_now,
                                                    "description",
                                                    consent_config)

    assert config_node is None


def test_create_consent_config_node_exception(client, right_now, app_space_id, capsys):
    config_node = client.create_consent_config_node(app_space_id,
                                                    "automation-"+right_now,
                                                    "Automation "+right_now,
                                                    "description",
                                                    "description")

    captured = capsys.readouterr()
    assert "Message must be initialized with a dict" in captured.err


def test_create_token_introspect_config_node_success(client, app_space_id, capsys):
    right_now = str(int(time.time())+2)
    token_introspect_config = data.get_token_introspect_config()

    config_node = client.create_token_introspect_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                            "description",
                                                             token_introspect_config)
    captured = capsys.readouterr()
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)
    response = client.delete_config_node(config_node.id, config_node.etag)
    assert response is not None


def test_create_token_introspect_config_node_empty(client, app_space_id, capsys):
    right_now = str(int(time.time())+4)
    token_introspect_config = data.get_token_introspect_config()

    def mocked_create_config_node(request: pb2.CreateConfigNodeRequest):
        return None

    client.stub.CreateConfigNode = mocked_create_config_node
    config_node = client.create_token_introspect_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                             "description",
                                                             token_introspect_config)
    assert config_node is None


def test_create_token_introspect_config_node_exception(client, app_space_id, capsys):
    right_now = str(int(time.time())+6)
    config_node = client.create_token_introspect_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                             "description",
                                                             "description")

    captured = capsys.readouterr()
    assert "Message must be initialized with a dict" in captured.err


def test_create_token_introspect_config_node_wrong_app_space(client, capsys):
    right_now = str(int(time.time())+2)
    app_space_id = data.get_identity_node()
    token_introspect_config = data.get_token_introspect_config()

    config_node = client.create_token_introspect_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                             "description",
                                                             token_introspect_config)
    captured = capsys.readouterr()
    assert "StatusCode.NOT_FOUND" in captured.err


def test_create_token_introspect_config_node_app_space_other_customer(client, capsys):
    right_now = str(int(time.time())+2)
    app_space_id = "gid:AAAAAoQaR-cpn0jcmWkW_HV1c6g"
    token_introspect_config = data.get_token_introspect_config()

    config_node = client.create_token_introspect_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                             "description",
                                                             token_introspect_config)
    captured = capsys.readouterr()
    assert "StatusCode.PERMISSION_DENIED" in captured.err


def test_update_token_introspect_config_node_success(client, right_now, app_space_id, ):
    token_introspect_config = data.get_token_introspect_config()
    config_node = client.create_token_introspect_config_node(app_space_id,
                                                             "automation-" + right_now,
                                                             "Automation " + right_now,
                                                             "description",
                                                             token_introspect_config)
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)
    right_now = str(int(time.time()))
    token_introspect_config = data.get_token_introspect_config()
    config_node_response = client.update_token_introspect_config_node(config_node.id,
                                                                      config_node.etag,
                                                                      "Automation "+right_now,
                                                                      "description "+right_now,
                                                                      token_introspect_config)
    assert config_node_response is not None
    assert isinstance(config_node_response, UpdateConfigNode)
    response = client.delete_config_node(config_node.id, config_node.etag)


def test_update_token_introspect_config_node_wrong_etag(client, right_now, capsys):
    token_introspect_config = data.get_token_introspect_config()
    config_node_response = client.update_token_introspect_config_node("gid:AAAAAuCBOLvwzUuWvKB1jWznHSM",
                                                                      "JD5ikook6kjiof",
                                                                      "Automation "+right_now,
                                                                      "description "+right_now,
                                                                      token_introspect_config)
    captured = capsys.readouterr()
    assert "invalid eTag value" in captured.err


def test_create_external_data_resolver_config_node_success(client, app_space_id, capsys):
    right_now = str(int(time.time())+2)
    external_data_resolver_config = data.get_external_data_resolver_config(right_now)

    config_node = client.create_external_data_resolver_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                            "description",
                                                             external_data_resolver_config)
    captured = capsys.readouterr()
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)
    response = client.delete_config_node(config_node.id, config_node.etag)
    assert response is not None


def test_create_external_data_resolver_config_node_empty(client, app_space_id, capsys):
    right_now = str(int(time.time())+4)
    external_data_resolver_config = data.get_external_data_resolver_config(right_now)

    def mocked_create_config_node(request: pb2.CreateConfigNodeRequest):
        return None

    client.stub.CreateConfigNode = mocked_create_config_node
    config_node = client.create_external_data_resolver_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                             "description",
                                                             external_data_resolver_config)
    assert config_node is None


def test_create_external_data_resolver_config_node_exception(client, app_space_id, capsys):
    right_now = str(int(time.time())+6)
    config_node = client.create_external_data_resolver_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                             "description",
                                                             "description")

    captured = capsys.readouterr()
    assert "ExternalDataResolverConfig must be an object" in captured.err


def test_create_external_data_resolver_config_node_wrong_app_space(client, capsys):
    right_now = str(int(time.time())+2)
    app_space_id = data.get_identity_node()
    external_data_resolver_config = data.get_external_data_resolver_config(right_now)

    config_node = client.create_external_data_resolver_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                             "description",
                                                             external_data_resolver_config)
    captured = capsys.readouterr()
    assert "StatusCode.NOT_FOUND" in captured.err


def test_create_external_data_resolver_config_node_app_space_other_customer(client, capsys):
    right_now = str(int(time.time())+2)
    app_space_id = "gid:AAAAAoQaR-cpn0jcmWkW_HV1c6g"
    external_data_resolver_config = data.get_external_data_resolver_config(right_now)

    config_node = client.create_external_data_resolver_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                             "description",
                                                             external_data_resolver_config)
    captured = capsys.readouterr()
    assert "StatusCode.PERMISSION_DENIED" in captured.err


def test_update_external_data_resolver_config_node_success(client, right_now, app_space_id):
    external_data_resolver_config = data.get_external_data_resolver_config(right_now)
    config_node = client.create_external_data_resolver_config_node(app_space_id,
                                                             "automation-" + right_now,
                                                             "Automation " + right_now,
                                                             "description",
                                                             external_data_resolver_config)
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)

    right_now = str(int(time.time()))
    external_data_resolver_config = data.get_external_data_resolver_config(right_now)
    config_node_response = client.update_external_data_resolver_config_node(config_node.id,
                                                                      config_node.etag,
                                                                      "Automation "+right_now,
                                                                      "description "+right_now,
                                                                      external_data_resolver_config)
    assert config_node_response is not None
    assert isinstance(config_node_response, UpdateConfigNode)
    response = client.delete_config_node(config_node.id, config_node.etag)


def test_update_external_data_resolver_config_node_wrong_id(client, right_now, capsys):
    external_data_resolver_config = data.get_external_data_resolver_config(right_now)
    config_node_response = client.update_external_data_resolver_config_node("gid:AAAAAuCBOLvwzUuWvKB1jWznHSM",
                                                                      "eyouyuuinjk",
                                                                      "Automation "+right_now,
                                                                      "description "+right_now,
                                                                      external_data_resolver_config)
    captured = capsys.readouterr()
    assert "invalid eTag value" in captured.err


def test_create_entity_matching_pipeline_config_node_success(client, app_space_id, capsys):
    right_now = str(int(time.time())+2)
    entity_matching_pipeline_config = data.get_entity_matching_pipeline_config(right_now)

    config_node = client.create_entity_matching_pipeline_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                            "description",
                                                             entity_matching_pipeline_config)
    captured = capsys.readouterr()
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)
    response = client.delete_config_node(config_node.id, config_node.etag)
    assert response is not None


def test_create_entity_matching_pipeline_config_node_empty(client, app_space_id, capsys):
    right_now = str(int(time.time())+4)
    entity_matching_pipeline_config = data.get_entity_matching_pipeline_config(right_now)

    def mocked_create_config_node(request: pb2.CreateConfigNodeRequest):
        return None

    client.stub.CreateConfigNode = mocked_create_config_node
    config_node = client.create_entity_matching_pipeline_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                             "description",
                                                             entity_matching_pipeline_config)
    assert config_node is None


def test_create_entity_matching_pipeline_config_node_exception(client, app_space_id, capsys):
    right_now = str(int(time.time())+6)
    config_node = client.create_entity_matching_pipeline_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                             "description",
                                                             "description")

    captured = capsys.readouterr()
    assert "EntityMatchingPipelineConfig must be an object" in captured.err


def test_create_entity_matching_pipeline_config_node_wrong_app_space(client, capsys):
    right_now = str(int(time.time())+2)
    app_space_id = data.get_identity_node()
    entity_matching_pipeline_config = data.get_entity_matching_pipeline_config(right_now)
    config_node = client.create_entity_matching_pipeline_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                             "description",
                                                             entity_matching_pipeline_config)
    captured = capsys.readouterr()
    assert "StatusCode.NOT_FOUND" in captured.err


def test_create_entity_matching_pipeline_config_node_app_space_other_customer(client, capsys):
    right_now = str(int(time.time())+2)
    app_space_id = "gid:AAAAAoQaR-cpn0jcmWkW_HV1c6g"
    entity_matching_pipeline_config = data.get_entity_matching_pipeline_config(right_now)

    config_node = client.create_entity_matching_pipeline_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                             "description",
                                                             entity_matching_pipeline_config)
    captured = capsys.readouterr()
    assert "StatusCode.PERMISSION_DENIED" in captured.err


def test_update_entity_matching_pipeline_config_node_success(client, right_now, app_space_id, ):
    entity_matching_pipeline_config = data.get_entity_matching_pipeline_config(right_now)
    config_node = client.create_entity_matching_pipeline_config_node(app_space_id,
                                                             "automation-" + right_now,
                                                             "Automation " + right_now,
                                                             "description",
                                                             entity_matching_pipeline_config)
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)

    right_now = str(int(time.time()))
    config_node_response = client.update_entity_matching_pipeline_config_node(config_node.id,
                                                                      config_node.etag,
                                                                      "Automation "+right_now,
                                                                      "description "+right_now,
                                                                      model_pb2.EntityMatchingPipelineConfig(
                                                                          similarity_score_cutoff=np.float32(0.9)
                                                                      ))
    assert config_node_response is not None
    assert isinstance(config_node_response, UpdateConfigNode)
    response = client.delete_config_node(config_node.id, config_node.etag)


def test_update_entity_matching_pipeline_config_node_wrong_id(client, right_now, capsys):
    config_node_response = client.update_entity_matching_pipeline_config_node("gid:AAAAAuCBOLvwzUuWvKB1jWznHSM",
                                                                      "eyouyuuinjk",
                                                                      "Automation "+right_now,
                                                                      "description "+right_now,
                                                                      model_pb2.EntityMatchingPipelineConfig(
                                                                          similarity_score_cutoff=np.float32(
                                                                              0.9)
                                                                      ))
    captured = capsys.readouterr()
    assert "invalid eTag value" in captured.err


def test_create_trust_score_profile_config_node_success(client, app_space_id, capsys):
    right_now = str(int(time.time())+2)
    trust_score_profile_config = data.get_trust_score_profile_config(right_now)

    config_node = client.create_trust_score_profile_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                            "description",
                                                             trust_score_profile_config)
    captured = capsys.readouterr()
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)
    response = client.delete_config_node(config_node.id, config_node.etag)
    assert response is not None


def test_create_trust_score_profile_config_node_empty(client, app_space_id, capsys):
    right_now = str(int(time.time())+4)
    trust_score_profile_config = data.get_trust_score_profile_config(right_now)

    def mocked_create_config_node(request: pb2.CreateConfigNodeRequest):
        return None

    client.stub.CreateConfigNode = mocked_create_config_node
    config_node = client.create_trust_score_profile_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                             "description",
                                                             trust_score_profile_config)
    assert config_node is None


def test_create_trust_score_profile_config_node_exception(client, app_space_id, capsys):
    right_now = str(int(time.time())+6)
    config_node = client.create_trust_score_profile_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                             "description",
                                                             "description")

    captured = capsys.readouterr()
    assert "TrustScoreProfileConfig must be an object" in captured.err


def test_create_trust_score_profile_config_node_wrong_app_space(client, capsys):
    right_now = str(int(time.time())+2)
    app_space_id = data.get_identity_node()
    trust_score_profile_config = data.get_trust_score_profile_config(right_now)
    config_node = client.create_trust_score_profile_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                             "description",
                                                             trust_score_profile_config)
    captured = capsys.readouterr()
    assert "StatusCode.NOT_FOUND" in captured.err


def test_create_trust_score_profile_config_node_app_space_other_customer(client, capsys):
    right_now = str(int(time.time())+2)
    app_space_id = "gid:AAAAAoQaR-cpn0jcmWkW_HV1c6g"
    trust_score_profile_config = data.get_trust_score_profile_config(right_now)

    config_node = client.create_trust_score_profile_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                             "description",
                                                             trust_score_profile_config)
    captured = capsys.readouterr()
    assert "StatusCode.PERMISSION_DENIED" in captured.err


def test_update_trust_score_profile_config_node_success(client, right_now, app_space_id, capsys):
    trust_score_profile_config = data.get_trust_score_profile_config(right_now)
    config_node = client.create_trust_score_profile_config_node(app_space_id,
                                                             "automation-" + right_now,
                                                             "Automation " + right_now,
                                                             "description",
                                                             trust_score_profile_config)
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)

    right_now = str(int(time.time()))
    config_node_response = client.update_trust_score_profile_config_node(
        config_node.id,
        config_node.etag,
        "Automation "+right_now,
        "description "+right_now,
           model_pb2.TrustScoreProfileConfig(
               dimensions=[model_pb2.TrustScoreDimension(
                   name=5,
                   weight=0.9
               )],
               schedule=4
           ))
    assert config_node_response is not None
    assert isinstance(config_node_response, UpdateConfigNode)
    response = client.delete_config_node(config_node.id, config_node.etag)


def test_update_trust_score_profile_config_node_wrong_id(client, right_now, capsys):
    config_node_response = client.update_trust_score_profile_config_node(
        "gid:AAAAAuCBOLvwzUuWvKB1jWznHSM",
        "eyouyuuinjk",
        "Automation "+right_now,
        "description "+right_now,
        model_pb2.TrustScoreProfileConfig(
            dimensions=[model_pb2.TrustScoreDimension(
                name=5,
                weight=0.9
            )],
            schedule=4
        ))
    captured = capsys.readouterr()
    assert "invalid eTag value" in captured.err


def test_create_knowledge_query_config_node_success(client, app_space_id, capsys):
    right_now = str(int(time.time())+2)
    knowledge_query_config = data.get_knowledge_query_config(right_now)

    config_node = client.create_knowledge_query_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                            "description",
                                                             knowledge_query_config)
    captured = capsys.readouterr()
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)
    response = client.delete_config_node(config_node.id, config_node.etag)
    assert response is not None


def test_create_knowledge_query_config_node_empty(client, app_space_id, capsys):
    right_now = str(int(time.time())+4)
    knowledge_query_config = data.get_knowledge_query_config(right_now)

    def mocked_create_config_node(request: pb2.CreateConfigNodeRequest):
        return None

    client.stub.CreateConfigNode = mocked_create_config_node
    config_node = client.create_knowledge_query_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                             "description",
                                                             knowledge_query_config)
    assert config_node is None


def test_create_knowledge_query_config_node_exception(client, app_space_id, capsys):
    right_now = str(int(time.time())+6)
    config_node = client.create_knowledge_query_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                             "description",
                                                             "description")

    captured = capsys.readouterr()
    assert "Message must be initialized with a dict" in captured.err


def test_create_knowledge_query_config_node_wrong_app_space(client, capsys):
    right_now = str(int(time.time())+2)
    app_space_id = data.get_identity_node()
    knowledge_query_config = data.get_knowledge_query_config(right_now)
    config_node = client.create_knowledge_query_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                             "description",
                                                             knowledge_query_config)
    captured = capsys.readouterr()
    assert "location must be DOCUMENT_TYPE_APP_SPACE" in captured.err


def test_knowledge_query_config_node_app_space_other_customer(client, capsys):
    right_now = str(int(time.time())+2)
    app_space_id = "gid:AAAAAoQaR-cpn0jcmWkW_HV1c6g"
    knowledge_query_config = data.get_knowledge_query_config(right_now)

    config_node = client.create_knowledge_query_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                             "description",
                                                             knowledge_query_config)
    captured = capsys.readouterr()
    assert "StatusCode.INVALID_ARGUMENT" in captured.err


def test_update_knowledge_query_config_node_success(client, right_now, app_space_id, capsys):
    knowledge_query_config = data.get_knowledge_query_config(right_now)
    config_node = client.create_knowledge_query_config_node(app_space_id,
                                                             "automation-" + right_now,
                                                             "Automation " + right_now,
                                                             "description",
                                                             knowledge_query_config)
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)

    right_now = str(int(time.time()))
    config_node_response = client.update_knowledge_query_config_node(
        config_node.id,
        config_node.etag,
        "Automation "+right_now,
        "description "+right_now,
        data.get_knowledge_query_config_upd(right_now)
    )
    assert config_node_response is not None
    assert isinstance(config_node_response, UpdateConfigNode)
    response = client.delete_config_node(config_node.id, config_node.etag)


def test_update_knowledge_query_config_node_wrong_id(client, right_now, capsys):
    config_node_response = client.update_knowledge_query_config_node(
        "gid:AAAAAuCBOLvwzUuWvKB1jWznHSM",
        "eyouyuuinjk",
        "Automation "+right_now,
        "description "+right_now,
        data.get_knowledge_query_config_upd(right_now)
    )
    captured = capsys.readouterr()
    assert "invalid eTag value" in captured.err


def test_create_event_sink_config_node_success(client, app_space_id, capsys):
    right_now = str(int(time.time())+2)
    event_sink_config = data.get_event_sink_config(right_now)

    config_node = client.create_event_sink_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                            "description",
                                                             event_sink_config)
    captured = capsys.readouterr()
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)
    response = client.delete_config_node(config_node.id, config_node.etag)
    assert response is not None


def test_create_event_sink_config_node_empty(client, app_space_id, capsys):
    right_now = str(int(time.time())+4)
    event_sink_config = data.get_event_sink_config(right_now)

    def mocked_create_config_node(request: pb2.CreateConfigNodeRequest):
        return None

    client.stub.CreateConfigNode = mocked_create_config_node
    config_node = client.create_event_sink_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                             "description",
                                                             event_sink_config)
    assert config_node is None


def test_create_event_sink_config_node_exception(client, app_space_id, capsys):
    right_now = str(int(time.time())+6)
    config_node = client.create_event_sink_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                             "description",
                                                             "description")

    captured = capsys.readouterr()
    assert "Message must be initialized with a dict" in captured.err


def test_create_event_sink_config_node_wrong_app_space(client, capsys):
    right_now = str(int(time.time())+2)
    app_space_id = data.get_identity_node()
    event_sink_config = data.get_event_sink_config(right_now)
    config_node = client.create_event_sink_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                             "description",
                                                             event_sink_config)
    captured = capsys.readouterr()
    assert "StatusCode.NOT_FOUND" in captured.err


def test_event_sink_config_node_app_space_other_customer(client, capsys):
    right_now = str(int(time.time())+2)
    app_space_id = "gid:AAAAAoQaR-cpn0jcmWkW_HV1c6g"
    event_sink_config = data.get_event_sink_config(right_now)

    config_node = client.create_event_sink_config_node(app_space_id,
                                                             "automation-"+right_now,
                                                             "Automation "+right_now,
                                                             "description",
                                                             event_sink_config)
    captured = capsys.readouterr()
    assert "StatusCode.PERMISSION_DENIED" in captured.err


def test_update_event_sink_config_node_success(client, app_space_id, capsys):
    right_now = str(int(time.time()) + 2)
    event_sink_config = data.get_event_sink_config(right_now)
    config_node = client.create_event_sink_config_node(app_space_id,
                                                             "automation-" + right_now,
                                                             "Automation " + right_now,
                                                             "description",
                                                             event_sink_config)
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)

    right_now = str(int(time.time()))
    config_node_response = client.update_event_sink_config_node(
        config_node.id,
        config_node.etag,
        "Automation "+right_now,
        "description "+right_now,
        data.get_event_sink_config(right_now)
    )
    assert config_node_response is not None
    assert isinstance(config_node_response, UpdateConfigNode)
    response = client.delete_config_node(config_node.id, config_node.etag)


def test_update_event_sink_config_node_wrong_id(client, right_now, capsys):
    config_node_response = client.update_event_sink_config_node(
        "gid:AAAAAuCBOLvwzUuWvKB1jWznHSM",
        "eyouyuuinjk",
        "Automation "+right_now,
        "description "+right_now,
        data.get_event_sink_config(right_now)
    )
    captured = capsys.readouterr()
    assert "invalid eTag value" in captured.err


def test_validate_authorization_policy_status(client, capsys):
    response = client.validate_authorization_policy_status("wrong")
    captured = capsys.readouterr()
    assert "status must be a member of AuthorizationPolicyConfig.Status" in captured.err


def test_validate_data_points(client, capsys):
    response = client.validate_data_points(False)
    captured = capsys.readouterr()
    assert "ERROR" in captured.err


def test_validate_entity_matching_status(client, capsys):
    response = client.validate_entity_matching_status("wrong")
    captured = capsys.readouterr()
    assert "status must be a member of EntityMatchingPipelineConfig.Status" in captured.err


def test_validate_trust_score_profile_dimension(client, capsys):
    response = client.validate_trust_score_profile_dimension("wrong")
    captured = capsys.readouterr()
    assert "dimension must be a member of TrustScoreDimension.Name" in captured.err


def test_validate_trust_score_profile_update_frequency(client, capsys):
    response = client.validate_trust_score_profile_update_frequency("wrong")
    captured = capsys.readouterr()
    assert "update_frequency must be a member of TrustScoreProfileConfig.UpdateFrequency" in captured.err


def test_validate_knowledge_query_status(client, capsys):
    response = client.validate_knowledge_query_status("wrong")
    captured = capsys.readouterr()
    assert "status must be a member of KnowledgeQueryStatus" in captured.err


def test_get_list_config_node_success(client, right_now, app_space_id, capsys):
    authorization_policy_config = data.get_authz_policy()
    config_node = client.create_authorization_policy_config_node(app_space_id,
                                                                 "automation-" + right_now,
                                                                 "Automation " + right_now,
                                                                 "description",
                                                                 authorization_policy_config)
    captured = capsys.readouterr()
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)
    config_node_id = config_node.id
    list_config_nodes = client.list_config_node_versions(config_node_id)
    assert list_config_nodes is not None
    assert list_config_nodes[0].id == config_node_id
    # assert list_config_nodes[0].version is not None
    response = client.delete_config_node(config_node.id, config_node.etag)


def test_get_list_config_node_empty(client, app_space_id, capsys):
    right_now = str(int(time.time() + 12))
    authorization_policy_config = data.get_authz_policy()
    config_node = client.create_authorization_policy_config_node(app_space_id,
                                                                 "automation-" + right_now,
                                                                 "Automation " + right_now,
                                                                 "description",
                                                                 authorization_policy_config)
    captured = capsys.readouterr()
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)
    config_node_id = config_node.id
    list_config_nodes = client.list_config_node_versions(config_node_id)
    assert list_config_nodes is not None
    response = client.delete_config_node(config_node.id, config_node.etag)


def test_get_list_config_node_exception(client, app_space_id, capsys):
    right_now = str(int(time.time() + 15))
    authorization_policy_config = data.get_authz_policy()
    config_node = client.create_authorization_policy_config_node(app_space_id,
                                                                 "automation-" + right_now,
                                                                 "Automation " + right_now,
                                                                 "description",
                                                                 authorization_policy_config)
    captured = capsys.readouterr()
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)
    config_node_id = config_node.id
    list_config_nodes = client.list_config_node_versions(app_space_id)
    assert "" in captured.err
    response = client.delete_config_node(config_node.id, config_node.etag)


