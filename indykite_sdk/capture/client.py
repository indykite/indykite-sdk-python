"""Synchronous Capture API client."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import httpx

from indykite_sdk._core.http import BaseSyncClient
from indykite_sdk._core.ops import RequestSpec
from indykite_sdk.capture import _ops
from indykite_sdk.capture.models import (
    BatchResults,
    DeleteNodeProperties,
    DeleteNodePropertyMetadata,
    DeleteRelationshipProperties,
    NodeRef,
    Relationship,
    UpsertNode,
)
from indykite_sdk.errors import ChunkedCaptureError, IndyKiteError

__all__ = ["CaptureClient"]


class CaptureClient(BaseSyncClient):
    """Ingest and delete IndyKite Knowledge Graph data via the Capture API.

    Authenticates with the raw **application-agent credential token**
    (``INDYKITE_APPLICATION_CREDENTIALS[_FILE]``) sent as ``X-IK-ClientKey``.

    Every batch method accepts 1–250 items (models or plain dicts) per call;
    pass ``auto_chunk=True`` to let the SDK split larger batches sequentially.

    On a composite IKG, set ``location`` on the nodes: each node is written to
    the database of its location, and a relationship to the database its source
    and target share, or to the global database when their locations differ.
    The GIDs then come back in :attr:`BatchResults.by_location` instead of
    :attr:`BatchResults.results`.

    Example::

        from indykite_sdk import CaptureClient

        with CaptureClient() as client:
            client.upsert_nodes([
                {"external_id": "millicent", "type": "Person", "is_identity": True,
                 "properties": [{"type": "email", "value": "millicent@example.com"}]},
            ])
    """

    _api_prefix = "/capture/v1"
    _auth_kind = "app_agent"

    def _send_batches(
        self,
        specs: list[tuple[int, RequestSpec, frozenset[str]]],
        *,
        timeout: httpx.Timeout | float | None,
    ) -> BatchResults:
        results = BatchResults()
        for start, spec, locations in specs:
            try:
                response = self._send(spec, timeout=timeout)
            except IndyKiteError as exc:
                if len(specs) > 1:
                    raise ChunkedCaptureError(
                        f"Chunked capture call failed at item {start} after {start} successful items.",
                        completed=results,
                        failed_at=start,
                    ) from exc
                raise
            results.merge(_ops.parse_batch_results(response, locations))
        return results

    def upsert_nodes(
        self,
        nodes: Sequence[UpsertNode | dict[str, Any]],
        *,
        auto_chunk: bool = False,
        timeout: httpx.Timeout | float | None = None,
    ) -> BatchResults:
        """Create or update nodes (``POST /nodes``).

        On a composite IKG a node with ``create_proxy`` also gets a proxy in
        the global database.

        Raises:
            RequestValidationError: invalid node payloads, or >250 items
                without ``auto_chunk``.
            ChunkedCaptureError: an ``auto_chunk`` run failed partway.
        """
        items = _ops.coerce_items(nodes, UpsertNode, "node")
        return self._send_batches(_ops.batch_specs("/nodes", "nodes", items, auto_chunk=auto_chunk), timeout=timeout)

    def delete_nodes(
        self,
        nodes: Sequence[NodeRef | dict[str, Any]],
        *,
        auto_chunk: bool = False,
        timeout: httpx.Timeout | float | None = None,
    ) -> BatchResults:
        """Delete whole nodes (``POST /nodes/delete``)."""
        items = _ops.coerce_items(nodes, NodeRef, "node reference")
        return self._send_batches(
            _ops.batch_specs("/nodes/delete", "nodes", items, auto_chunk=auto_chunk), timeout=timeout
        )

    def delete_node_properties(
        self,
        nodes: Sequence[DeleteNodeProperties | dict[str, Any]],
        *,
        auto_chunk: bool = False,
        timeout: httpx.Timeout | float | None = None,
    ) -> BatchResults:
        """Strip named properties from nodes; the nodes survive (``POST /nodes/properties/delete``)."""
        items = _ops.coerce_items(nodes, DeleteNodeProperties, "node property delete")
        return self._send_batches(
            _ops.batch_specs("/nodes/properties/delete", "nodes", items, auto_chunk=auto_chunk), timeout=timeout
        )

    def delete_node_property_metadata(
        self,
        nodes: Sequence[DeleteNodePropertyMetadata | dict[str, Any]],
        *,
        auto_chunk: bool = False,
        timeout: httpx.Timeout | float | None = None,
    ) -> BatchResults:
        """Strip metadata fields from one property per node (``POST /nodes/properties/metadata/delete``)."""
        items = _ops.coerce_items(nodes, DeleteNodePropertyMetadata, "property metadata delete")
        return self._send_batches(
            _ops.batch_specs("/nodes/properties/metadata/delete", "nodes", items, auto_chunk=auto_chunk),
            timeout=timeout,
        )

    def upsert_relationships(
        self,
        relationships: Sequence[Relationship | dict[str, Any]],
        *,
        auto_chunk: bool = False,
        timeout: httpx.Timeout | float | None = None,
    ) -> BatchResults:
        """Create or update relationships between existing nodes (``POST /relationships``).

        On a composite IKG the database is chosen from the ``location`` of the
        source and target nodes: their shared location, or the global database
        when the locations differ. To write to the global database explicitly,
        set the global location on both nodes. A source or target missing from
        that database is created there with only its external ID and type;
        upsert the node with ``create_proxy`` first to have a proxy that
        carries its location.
        """
        items = _ops.coerce_items(relationships, Relationship, "relationship")
        return self._send_batches(
            _ops.batch_specs("/relationships", "relationships", items, auto_chunk=auto_chunk),
            timeout=timeout,
        )

    def delete_relationships(
        self,
        relationships: Sequence[Relationship | dict[str, Any]],
        *,
        auto_chunk: bool = False,
        timeout: httpx.Timeout | float | None = None,
    ) -> BatchResults:
        """Delete relationships; the endpoint nodes survive (``POST /relationships/delete``)."""
        items = _ops.coerce_items(relationships, Relationship, "relationship")
        return self._send_batches(
            _ops.batch_specs("/relationships/delete", "relationships", items, auto_chunk=auto_chunk),
            timeout=timeout,
        )

    def delete_relationship_properties(
        self,
        relationships: Sequence[DeleteRelationshipProperties | dict[str, Any]],
        *,
        auto_chunk: bool = False,
        timeout: httpx.Timeout | float | None = None,
    ) -> BatchResults:
        """Strip named properties from relationships (``POST /relationships/properties/delete``)."""
        items = _ops.coerce_items(relationships, DeleteRelationshipProperties, "relationship property delete")
        return self._send_batches(
            _ops.batch_specs("/relationships/properties/delete", "relationships", items, auto_chunk=auto_chunk),
            timeout=timeout,
        )
