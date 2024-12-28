import logging
from io import StringIO
import numpy as np
import pytest
import time

from indykite_sdk.entitymatching import EntityMatchingClient
from indykite_sdk.config import ConfigClient
from indykite_sdk.model.create_config_node import CreateConfigNode
from indykite_sdk.indykite.entitymatching.v1beta1 import entity_matching_api_pb2 as pb2
from helpers import data


@pytest.fixture
def client():
    return EntityMatchingClient()


@pytest.fixture
def client_config():
    return ConfigClient()


@pytest.fixture
def right_now():
    return str(int(time.time()) + 2)


@pytest.fixture
def app_space_id():
    return data.get_app_space_id()


def test_entity_matching_success(client, client_config, right_now, app_space_id):
    entity_matching_pipeline_config = data.get_entity_matching_pipeline_config(right_now)

    config_node = client_config.create_entity_matching_pipeline_config_node(app_space_id,
                                                                     "automation-" + right_now,
                                                                     "Automation " + right_now,
                                                                     "description",
                                                                     entity_matching_pipeline_config)
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)
    # send the read entity matching report request and get the response
    time.sleep(5)
    read_suggested_property_mapping = client.read_suggested_property_mapping(config_node.id)
    assert read_suggested_property_mapping is not None
    assert read_suggested_property_mapping.id == config_node.id
    time.sleep(6)
    run_entity_matching_pipeline = client.run_entity_matching_pipeline(
        id=config_node.id,
        similarity_score_cutoff=np.float32(0.95)
    )
    assert run_entity_matching_pipeline is not None
    assert run_entity_matching_pipeline.id == config_node.id

    response = client_config.delete_config_node(config_node.id, config_node.etag)
    assert response is not None


def test_entity_matching_error(client, client_config, right_now, app_space_id):
    logger = logging.getLogger()
    log_stream = StringIO()

    # Set up a stream handler to capture logs
    handler = logging.StreamHandler(log_stream)
    logger.addHandler(handler)
    logger.setLevel(logging.ERROR)
    entity_matching_pipeline_config = data.get_entity_matching_pipeline_config(right_now)
    config_node = client_config.create_entity_matching_pipeline_config_node(app_space_id,
                                                                     "automation-" + right_now,
                                                                     "Automation " + right_now,
                                                                     "description",
                                                                     entity_matching_pipeline_config)
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)
    # send the read entity matching report request and get the response
    read_suggested_property_mapping = client.read_suggested_property_mapping("gid:AAAAFl4LKWRchUKbnN54xGIi5Io")
    assert "invalid entity matching pipeline id" in log_stream.getvalue()
    time.sleep(6)
    run_entity_matching_pipeline = client.run_entity_matching_pipeline(
        id="gid:AAAAFl4LKWRchUKbnN54xGIi5Io",
        similarity_score_cutoff=np.float32(0.95)
    )
    assert "invalid entity matching pipeline id" in log_stream.getvalue()

    response = client_config.delete_config_node(config_node.id, config_node.etag)
    assert response is not None
    # Clean up
    logger.removeHandler(handler)


def test_entity_matching_empty(client, client_config, right_now, app_space_id):
    entity_matching_pipeline_config = data.get_entity_matching_pipeline_config(right_now)
    config_node = client_config.create_entity_matching_pipeline_config_node(app_space_id,
                                                                     "automation-" + right_now,
                                                                     "Automation " + right_now,
                                                                     "description",
                                                                     entity_matching_pipeline_config)
    assert config_node is not None
    assert isinstance(config_node, CreateConfigNode)
    time.sleep(5)
    # send the read entity matching report request and get the response

    def mocked_read_suggested_property_mapping(request: pb2.ReadSuggestedPropertyMappingRequest):
        return None

    client.stub.ReadSuggestedPropertyMapping = mocked_read_suggested_property_mapping
    read_suggested_property_mapping = client.read_suggested_property_mapping(config_node.id)
    assert read_suggested_property_mapping is None
    time.sleep(6)
    def mocked_run_entity_matching_pipeline(request: pb2.RunEntityMatchingPipelineRequest):
        return None

    client.stub.RunEntityMatchingPipeline = mocked_run_entity_matching_pipeline
    run_entity_matching_pipeline = client.run_entity_matching_pipeline(
        id=config_node.id,
        similarity_score_cutoff=np.float32(0.95)
    )
    assert run_entity_matching_pipeline is None

    response = client_config.delete_config_node(config_node.id, config_node.etag)
    assert response is not None
