"""Live test for a ``2.0-ciq`` write query whose upsert values are ``@`` references.

The platform reads the referenced values from the graph the policy matched and
writes them on the matched node, so the response carries values the request
never sent. The test builds its policy, knowledge query and graph data in the
test project and cleans up after itself.
"""

from __future__ import annotations

import json
from typing import Any

from indykite_sdk import APIStatusError, CaptureClient, CIQClient, ConfigClient
from tests.integration.conftest import poll_until

POLICY = {
    "meta": {"policy_version": "2.0-ciq"},
    # The _Application subject binds to the caller's own application node, so
    # executing needs only the application-agent credential.
    "subject": {"type": "_Application"},
    "condition": {
        "cypher": "MATCH (subject:_Application) MATCH (owner:Person)-[:OWNS]->(server:Server)",
        "filter": [
            {
                "operator": "AND",
                "operands": [
                    {"operator": "=", "attribute": "@subject.external_id", "value": "$_appId"},
                    {"operator": "=", "attribute": "@server.external_id", "value": "$server_external_id"},
                ],
            }
        ],
    },
    "allowed_reads": {"nodes": ["server.*"]},
    "allowed_upserts": {"nodes": {"existing_nodes": ["server"]}},
}

QUERY = {
    "nodes": ["server.property.owner_id", "server.property.owner_email"],
    "upsert_nodes": [
        {
            "name": "server",
            "properties": [
                {"type": "owner_id", "value": "@owner.external_id"},
                {"type": "owner_email", "value": "@owner.property.email"},
            ],
        }
    ],
}


def test_ciq_upserts_values_referenced_from_the_matched_graph(
    config_client: ConfigClient,
    capture_client: CaptureClient,
    ciq_client: CIQClient,
    project_id: str,
    unique_suffix: str,
) -> None:
    """Ciq upserts values referenced from the matched graph."""
    owner_email = f"sdk-it-ciq2-{unique_suffix}@example.com"
    owner = {"external_id": f"sdk-it-ciq2-owner-{unique_suffix}", "type": "Person"}
    # No region property, so knowledge queries filtering servers by region never see this transient one.
    server = {"external_id": f"sdk-it-ciq2-server-{unique_suffix}", "type": "Server"}
    owns = {"type": "OWNS", "source": owner, "target": server}

    policy = config_client.create_authorization_policy(
        f"sdk-it-ciq2-ref-{unique_suffix}", project_id, json.dumps(POLICY), "ACTIVE"
    )
    assert policy.id
    try:
        query = config_client.create_knowledge_query(
            f"sdk-it-ciq2-ref-kq-{unique_suffix}", project_id, json.dumps(QUERY), "ACTIVE", policy.id
        )
        assert query.id
        try:
            try:
                capture_client.upsert_nodes(
                    [
                        dict(owner, is_identity=True, properties=[{"type": "email", "value": owner_email}]),
                        server,
                    ]
                )
                capture_client.upsert_relationships([owns])

                def referenced_values() -> dict[str, Any] | None:
                    response = ciq_client.execute(query.id, input_params={"server_external_id": server["external_id"]})
                    if len(response.data) != 1:
                        return None
                    nodes = response.data[0].nodes
                    return nodes if nodes.get("server.property.owner_email") == owner_email else None

                # The write is idempotent, so poll until policy, query and data
                # have propagated and the referenced values come back.
                nodes = poll_until(referenced_values, retry_on=(APIStatusError,), timeout=60.0, interval=5.0)
                assert nodes["server.property.owner_id"] == owner["external_id"]
                assert nodes["server.property.owner_email"] == owner_email
            finally:
                capture_client.delete_relationships([owns])
                capture_client.delete_nodes([owner, server])
        finally:
            # The query references the policy, so it goes first.
            current_query = config_client.read_knowledge_query(query.id)
            config_client.delete_knowledge_query(query.id, etag=current_query.etag)
    finally:
        current_policy = config_client.read_authorization_policy(policy.id)
        config_client.delete_authorization_policy(policy.id, etag=current_policy.etag)
