"""Capture client: payload shapes, batch limits, chunking, single-node upsert."""

from __future__ import annotations

import pytest

from indykite_sdk import (
    AsyncCaptureClient,
    CaptureClient,
    ChunkedCaptureError,
    NotFoundError,
    RequestValidationError,
)
from indykite_sdk.capture import Property, UpsertNode
from tests.unit.conftest import sent_json

NODE = {
    "external_id": "captureRest_knightrider",
    "type": "Person",
    "is_identity": True,
    "properties": [{"type": "email", "value": "michael@knightrider.com"}],
}
RELATIONSHIP = {
    "type": "OWNS",
    "source": {"external_id": "captureRest_knightrider", "type": "Person"},
    "target": {"external_id": "kitt", "type": "Car"},
}


def test_upsert_nodes_sends_expected_body_and_parses_results(make_client, mock_api) -> None:
    """Upsert nodes sends expected body and parses results."""
    mock_api.respond({"results": [{"id": "gid:node-1"}]})
    client = make_client(CaptureClient)
    results = client.upsert_nodes([NODE])
    assert mock_api.last.method == "POST"
    assert mock_api.last.url.path == "/capture/v1/nodes"
    assert sent_json(mock_api.last) == {"nodes": [NODE]}
    assert results[0].id == "gid:node-1"


def test_upsert_nodes_accepts_models(make_client, mock_api) -> None:
    """Upsert nodes accepts models."""
    client = make_client(CaptureClient)
    node = UpsertNode(external_id="ada", type="Person", properties=[Property(type="name", value="Ada")])
    client.upsert_nodes([node])
    body = sent_json(mock_api.last)
    assert body["nodes"][0]["properties"] == [{"type": "name", "value": "Ada"}]


def test_upsert_nodes_invalid_node_raises_validation_error(make_client) -> None:
    """Upsert nodes invalid node raises validation error."""
    client = make_client(CaptureClient)
    with pytest.raises(RequestValidationError, match="index 0"):
        client.upsert_nodes([{"type": "Person"}])  # missing external_id


def test_upsert_nodes_empty_batch_raises(make_client) -> None:
    """Upsert nodes empty batch raises."""
    client = make_client(CaptureClient)
    with pytest.raises(RequestValidationError, match="At least one"):
        client.upsert_nodes([])


def test_upsert_nodes_over_250_without_auto_chunk_raises(make_client) -> None:
    """Upsert nodes over 250 without auto chunk raises."""
    client = make_client(CaptureClient)
    nodes = [{"external_id": f"n{i}", "type": "Person"} for i in range(251)]
    with pytest.raises(RequestValidationError, match="auto_chunk"):
        client.upsert_nodes(nodes)


def test_upsert_nodes_auto_chunk_splits_and_concatenates(make_client, mock_api) -> None:
    """Upsert nodes auto chunk splits and concatenates."""
    nodes = [{"external_id": f"n{i}", "type": "Person"} for i in range(600)]
    for chunk_size in (250, 250, 100):
        mock_api.respond({"results": [{"id": f"gid:{i}"} for i in range(chunk_size)]})
    client = make_client(CaptureClient)
    results = client.upsert_nodes(nodes, auto_chunk=True)
    assert len(mock_api.requests) == 3
    assert [len(sent_json(r)["nodes"]) for r in mock_api.requests] == [250, 250, 100]
    assert len(results) == 600


def test_upsert_nodes_auto_chunk_partial_failure(make_client, mock_api) -> None:
    """Upsert nodes auto chunk partial failure."""
    nodes = [{"external_id": f"n{i}", "type": "Person"} for i in range(300)]
    mock_api.respond({"results": [{"id": f"gid:{i}"} for i in range(250)]})
    mock_api.respond((404, {"message": "Not Found"}))
    client = make_client(CaptureClient)
    with pytest.raises(ChunkedCaptureError) as exc_info:
        client.upsert_nodes(nodes, auto_chunk=True)
    error = exc_info.value
    assert len(error.completed) == 250
    assert error.failed_at == 250
    assert isinstance(error.__cause__, NotFoundError)


def test_upsert_single_node_put_path_and_body(make_client, mock_api) -> None:
    """Upsert single node put path and body."""
    mock_api.respond({"id": "gid:node-1"})
    client = make_client(CaptureClient)
    result = client.upsert_node(NODE)
    assert mock_api.last.method == "PUT"
    assert mock_api.last.url.path == "/capture/v1/nodes/Person:captureRest_knightrider"
    body = sent_json(mock_api.last)
    assert "external_id" not in body
    assert "type" not in body
    assert body["is_identity"] is True
    assert result.id == "gid:node-1"


def test_deletes_delete_nodes_path(make_client, mock_api) -> None:
    """Deletes delete nodes path."""
    client = make_client(CaptureClient)
    client.delete_nodes([{"external_id": "ada", "type": "Person"}])
    assert mock_api.last.url.path == "/capture/v1/nodes/delete"
    assert sent_json(mock_api.last) == {"nodes": [{"external_id": "ada", "type": "Person"}]}


def test_deletes_delete_node_properties(make_client, mock_api) -> None:
    """Deletes delete node properties."""
    client = make_client(CaptureClient)
    client.delete_node_properties([{"external_id": "ada", "type": "Person", "property_types": ["email"]}])
    assert mock_api.last.url.path == "/capture/v1/nodes/properties/delete"


def test_deletes_delete_node_property_metadata(make_client, mock_api) -> None:
    """Deletes delete node property metadata."""
    client = make_client(CaptureClient)
    client.delete_node_property_metadata(
        [{"external_id": "ada", "type": "Person", "property_type": "email", "metadata_fields": ["source"]}]
    )
    assert mock_api.last.url.path == "/capture/v1/nodes/properties/metadata/delete"


def test_deletes_delete_relationship_properties(make_client, mock_api) -> None:
    """Deletes delete relationship properties."""
    client = make_client(CaptureClient)
    client.delete_relationship_properties([dict(RELATIONSHIP, property_types=["since"])])
    assert mock_api.last.url.path == "/capture/v1/relationships/properties/delete"


def test_relationships_upsert_relationships_body(make_client, mock_api) -> None:
    """Relationships upsert relationships body."""
    client = make_client(CaptureClient)
    client.upsert_relationships([RELATIONSHIP])
    assert mock_api.last.url.path == "/capture/v1/relationships"
    assert sent_json(mock_api.last) == {"relationships": [RELATIONSHIP]}


def test_relationships_use_global_db_flag(make_client, mock_api) -> None:
    """Relationships use global db flag."""
    client = make_client(CaptureClient)
    client.delete_relationships([RELATIONSHIP], use_global_db=True)
    assert mock_api.last.url.path == "/capture/v1/relationships/delete"
    assert sent_json(mock_api.last)["use_global_db"] is True


def test_relationships_use_global_db_omitted_when_false(make_client, mock_api) -> None:
    """Relationships use global db omitted when false."""
    client = make_client(CaptureClient)
    client.upsert_relationships([RELATIONSHIP])
    assert "use_global_db" not in sent_json(mock_api.last)


async def test_async_capture_upsert_nodes(make_async_client, mock_api) -> None:
    """Async capture upsert nodes."""
    mock_api.respond({"results": [{"id": "gid:node-1"}]})
    async with make_async_client(AsyncCaptureClient) as client:
        results = await client.upsert_nodes([NODE])
    assert results[0].id == "gid:node-1"
    assert mock_api.last.headers["X-IK-ClientKey"] == "app-agent-token-value"


async def test_async_capture_auto_chunk_partial_failure(make_async_client, mock_api) -> None:
    """Async capture auto chunk partial failure."""
    nodes = [{"external_id": f"n{i}", "type": "Person"} for i in range(300)]
    mock_api.respond({"results": []})
    mock_api.respond((404, {"message": "Not Found"}))
    async with make_async_client(AsyncCaptureClient) as client:
        with pytest.raises(ChunkedCaptureError):
            await client.upsert_nodes(nodes, auto_chunk=True)


async def test_async_capture_all_endpoints_round_trip(make_async_client, mock_api) -> None:
    """Async capture all endpoints round trip."""
    async with make_async_client(AsyncCaptureClient) as client:
        await client.upsert_node(NODE)
        await client.delete_nodes([{"external_id": "ada", "type": "Person"}])
        await client.delete_node_properties([{"external_id": "ada", "type": "Person", "property_types": ["email"]}])
        await client.delete_node_property_metadata(
            [{"external_id": "ada", "type": "Person", "property_type": "email", "metadata_fields": ["source"]}]
        )
        await client.upsert_relationships([RELATIONSHIP])
        await client.delete_relationships([RELATIONSHIP], use_global_db=True)
        await client.delete_relationship_properties([dict(RELATIONSHIP, property_types=["since"])])
    paths = [request.url.path.removeprefix("/capture/v1") for request in mock_api.requests]
    assert paths == [
        "/nodes/Person:captureRest_knightrider",
        "/nodes/delete",
        "/nodes/properties/delete",
        "/nodes/properties/metadata/delete",
        "/relationships",
        "/relationships/delete",
        "/relationships/properties/delete",
    ]
