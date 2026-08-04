"""Data Schema client: JGF parsing and helpers."""

from __future__ import annotations

from indykite_sdk import AsyncDataSchemaClient, DataSchemaClient

JGF = {
    "graph": {
        "directed": True,
        "nodes": {
            "Person": {"metadata": {"node_count": 2}},
            "Car": {"metadata": {"node_count": 1}},
        },
        "edges": [
            {"source": "Person", "target": "Car", "relation": "OWNS", "directed": True},
            {"source": "Person", "target": "Car", "relation": "CAN_DRIVE", "directed": True},
        ],
    }
}


def test_read_parses_jgf(make_client, mock_api) -> None:
    """Read parses jgf."""
    mock_api.respond(JGF)
    client = make_client(DataSchemaClient)
    schema = client.read()
    assert mock_api.last.method == "GET"
    assert mock_api.last.url.path == "/data-schema/v1"
    assert sorted(schema.node_types) == ["Car", "Person"]
    assert schema.relationship_types == ["CAN_DRIVE", "OWNS"]


def test_empty_schema(make_client, mock_api) -> None:
    """Empty schema."""
    mock_api.respond({})
    client = make_client(DataSchemaClient)
    schema = client.read()
    assert schema.node_types == []
    assert schema.relationship_types == []


async def test_async_read(make_async_client, mock_api) -> None:
    """Async read."""
    mock_api.respond(JGF)
    async with make_async_client(AsyncDataSchemaClient) as client:
        schema = await client.read()
    assert "Person" in schema.node_types
