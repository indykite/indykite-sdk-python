"""Asynchronous Capture API client."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import httpx

from indykite_sdk._core.http import BaseAsyncClient
from indykite_sdk._core.ops import RequestSpec
from indykite_sdk.capture import _ops
from indykite_sdk.capture.models import (
    BatchResult,
    DeleteNodeProperties,
    DeleteNodePropertyMetadata,
    DeleteRelationshipProperties,
    NodeRef,
    Relationship,
    UpsertNode,
)
from indykite_sdk.errors import ChunkedCaptureError, IndyKiteError

__all__ = ["AsyncCaptureClient"]


class AsyncCaptureClient(BaseAsyncClient):
    """Async variant of :class:`indykite_sdk.CaptureClient` - same methods, ``await``-able.

    Example::

        from indykite_sdk import AsyncCaptureClient

        async with AsyncCaptureClient() as client:
            await client.upsert_nodes([{"external_id": "millicent", "type": "Person"}])
    """

    _api_prefix = "/capture/v1"
    _auth_kind = "app_agent"

    async def _send_batches(
        self,
        specs: list[tuple[int, RequestSpec]],
        *,
        timeout: httpx.Timeout | float | None,
    ) -> list[BatchResult]:
        results: list[BatchResult] = []
        for start, spec in specs:
            try:
                response = await self._send(spec, timeout=timeout)
            except IndyKiteError as exc:
                if len(specs) > 1:
                    raise ChunkedCaptureError(
                        f"Chunked capture call failed at item {start} after {len(results)} successful items.",
                        completed=results,
                        failed_at=start,
                    ) from exc
                raise
            results.extend(_ops.parse_batch_results(response))
        return results

    async def upsert_nodes(
        self,
        nodes: Sequence[UpsertNode | dict[str, Any]],
        *,
        auto_chunk: bool = False,
        timeout: httpx.Timeout | float | None = None,
    ) -> list[BatchResult]:
        """Create or update nodes (``POST /nodes``)."""
        items = _ops.coerce_items(nodes, UpsertNode, "node")
        return await self._send_batches(
            _ops.batch_specs("/nodes", "nodes", items, auto_chunk=auto_chunk), timeout=timeout
        )

    async def upsert_node(
        self,
        node: UpsertNode | dict[str, Any],
        *,
        timeout: httpx.Timeout | float | None = None,
    ) -> BatchResult:
        """Create or update a single node (``PUT /nodes/{type}:{external_id}``). **Experimental.**"""
        item = _ops.coerce_items([node], UpsertNode, "node")[0]
        body = item.to_wire()
        path = f"/nodes/{body.pop('type')}:{body.pop('external_id')}"
        response = await self._send(RequestSpec("PUT", path, json_body=body), timeout=timeout)
        data = response.json() if response.content else {}
        return BatchResult.model_validate(data if isinstance(data, dict) else {})

    async def delete_nodes(
        self,
        nodes: Sequence[NodeRef | dict[str, Any]],
        *,
        auto_chunk: bool = False,
        timeout: httpx.Timeout | float | None = None,
    ) -> list[BatchResult]:
        """Delete whole nodes (``POST /nodes/delete``)."""
        items = _ops.coerce_items(nodes, NodeRef, "node reference")
        return await self._send_batches(
            _ops.batch_specs("/nodes/delete", "nodes", items, auto_chunk=auto_chunk), timeout=timeout
        )

    async def delete_node_properties(
        self,
        nodes: Sequence[DeleteNodeProperties | dict[str, Any]],
        *,
        auto_chunk: bool = False,
        timeout: httpx.Timeout | float | None = None,
    ) -> list[BatchResult]:
        """Strip named properties from nodes (``POST /nodes/properties/delete``)."""
        items = _ops.coerce_items(nodes, DeleteNodeProperties, "node property delete")
        return await self._send_batches(
            _ops.batch_specs("/nodes/properties/delete", "nodes", items, auto_chunk=auto_chunk), timeout=timeout
        )

    async def delete_node_property_metadata(
        self,
        nodes: Sequence[DeleteNodePropertyMetadata | dict[str, Any]],
        *,
        auto_chunk: bool = False,
        timeout: httpx.Timeout | float | None = None,
    ) -> list[BatchResult]:
        """Strip metadata fields from one property per node (``POST /nodes/properties/metadata/delete``)."""
        items = _ops.coerce_items(nodes, DeleteNodePropertyMetadata, "property metadata delete")
        return await self._send_batches(
            _ops.batch_specs("/nodes/properties/metadata/delete", "nodes", items, auto_chunk=auto_chunk),
            timeout=timeout,
        )

    async def upsert_relationships(
        self,
        relationships: Sequence[Relationship | dict[str, Any]],
        *,
        use_global_db: bool = False,
        auto_chunk: bool = False,
        timeout: httpx.Timeout | float | None = None,
    ) -> list[BatchResult]:
        """Create or update relationships (``POST /relationships``)."""
        items = _ops.coerce_items(relationships, Relationship, "relationship")
        extra = {"use_global_db": True} if use_global_db else None
        return await self._send_batches(
            _ops.batch_specs("/relationships", "relationships", items, auto_chunk=auto_chunk, extra_body=extra),
            timeout=timeout,
        )

    async def delete_relationships(
        self,
        relationships: Sequence[Relationship | dict[str, Any]],
        *,
        use_global_db: bool = False,
        auto_chunk: bool = False,
        timeout: httpx.Timeout | float | None = None,
    ) -> list[BatchResult]:
        """Delete relationships (``POST /relationships/delete``)."""
        items = _ops.coerce_items(relationships, Relationship, "relationship")
        extra = {"use_global_db": True} if use_global_db else None
        return await self._send_batches(
            _ops.batch_specs("/relationships/delete", "relationships", items, auto_chunk=auto_chunk, extra_body=extra),
            timeout=timeout,
        )

    async def delete_relationship_properties(
        self,
        relationships: Sequence[DeleteRelationshipProperties | dict[str, Any]],
        *,
        use_global_db: bool = False,
        auto_chunk: bool = False,
        timeout: httpx.Timeout | float | None = None,
    ) -> list[BatchResult]:
        """Strip named properties from relationships (``POST /relationships/properties/delete``)."""
        items = _ops.coerce_items(relationships, DeleteRelationshipProperties, "relationship property delete")
        extra = {"use_global_db": True} if use_global_db else None
        return await self._send_batches(
            _ops.batch_specs(
                "/relationships/properties/delete", "relationships", items, auto_chunk=auto_chunk, extra_body=extra
            ),
            timeout=timeout,
        )
