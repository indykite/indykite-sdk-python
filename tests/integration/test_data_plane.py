"""Live AuthZEN, CIQ, Data Schema, and Entity Matching smoke tests."""

from __future__ import annotations

from indykite_sdk import (
    AuthZENClient,
    CIQClient,
    DataSchemaClient,
    EntityMatchingClient,
)
from tests.integration.conftest import require_env


def test_authzen_evaluation_returns_boolean(authzen_client: AuthZENClient) -> None:
    """Authzen evaluation returns boolean."""
    result = authzen_client.evaluation(
        ("Person", "sdk-it-nonexistent-subject"),
        "SDK_IT_ACTION",
        ("Asset", "sdk-it-nonexistent-resource"),
    )
    assert isinstance(result.decision, bool)


def test_authzen_search_action(authzen_client: AuthZENClient) -> None:
    """Authzen search action."""
    result = authzen_client.search_action(
        ("Person", "sdk-it-nonexistent-subject"),
        ("Asset", "sdk-it-nonexistent-resource"),
    )
    assert isinstance(result.action_names, list)


def test_ciq_execute(ciq_client: CIQClient) -> None:
    """Ciq execute."""
    query_id = require_env("INDYKITE_TEST_KNOWLEDGE_QUERY_ID")
    response = ciq_client.execute(query_id, page_size=10)
    assert isinstance(response.data, list)


def test_ciq_pagination(ciq_client: CIQClient) -> None:
    """Ciq pagination."""
    query_id = require_env("INDYKITE_TEST_KNOWLEDGE_QUERY_ID")
    records = list(ciq_client.execute_iter(query_id, page_size=2))
    assert isinstance(records, list)


def test_data_schema_read(data_schema_client: DataSchemaClient) -> None:
    """Data schema read."""
    schema = data_schema_client.read()
    assert isinstance(schema.graph, dict)


def test_entity_matching_status(entity_matching_client: EntityMatchingClient) -> None:
    """Entity matching status."""
    pipeline_id = require_env("INDYKITE_TEST_ENTITY_MATCHING_PIPELINE_ID")
    status = entity_matching_client.read_status(pipeline_id)
    assert status.id or status.entity_matching_status or status.property_mapping_status


def test_entity_matching_property_mappings(entity_matching_client: EntityMatchingClient) -> None:
    """Entity matching property mappings."""
    pipeline_id = require_env("INDYKITE_TEST_ENTITY_MATCHING_PIPELINE_ID")
    mappings = entity_matching_client.read_property_mappings(pipeline_id)
    assert isinstance(mappings.suggested_property_mappings, list)
