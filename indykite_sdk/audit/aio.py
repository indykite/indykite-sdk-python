"""Asynchronous Audit Log client."""

from __future__ import annotations

from collections.abc import AsyncIterator, Awaitable, Callable

import httpx

from indykite_sdk._core.http import BaseAsyncClient
from indykite_sdk.audit import _ops
from indykite_sdk.audit.models import Checkpoint, KeySet, LogEntry, Manifest, Page

__all__ = ["AsyncAuditClient"]

type Timeout = httpx.Timeout | float | None


class AsyncAuditClient(BaseAsyncClient):
    """Async variant of :class:`indykite_sdk.AuditClient` - same methods, ``await``-able.

    Example::

        from indykite_sdk import AsyncAuditClient

        async with AsyncAuditClient() as client:
            async for manifest in client.iter_manifests("gid:project"):
                print(manifest.sequence, manifest.head_hash)
    """

    _api_prefix = "/audit"
    _auth_kind = "app_agent"

    async def _list[ItemT](
        self,
        path: str,
        item_cls: type[ItemT],
        project_id: str,
        cursor: str | None,
        page_size: int | None,
        timeout: Timeout,
    ) -> Page[ItemT]:
        spec = _ops.list_spec(path, project_id, cursor, page_size)
        response = await self._send(spec, timeout=timeout)
        return Page[item_cls].model_validate(response.json())  # type: ignore[valid-type]

    @staticmethod
    async def _iter_pages[ItemT](
        list_page: Callable[[str | None], Awaitable[Page[ItemT]]],
    ) -> AsyncIterator[ItemT]:
        """Yield the items of every page, following ``next_cursor`` while ``has_more``."""
        cursor: str | None = None
        while True:
            page = await list_page(cursor)
            for item in page.items:
                yield item
            cursor = _ops.next_cursor(cursor, page.next_cursor, page.has_more)
            if cursor is None:
                return

    async def list_logs(
        self, project_id: str, *, cursor: str | None = None, page_size: int | None = None, timeout: Timeout = None
    ) -> Page[LogEntry]:
        """One page of the project's signed chain batches, the audit events (``GET /v1/logs``)."""
        return await self._list(_ops.LOGS_PATH, LogEntry, project_id, cursor, page_size, timeout)

    def iter_logs(
        self, project_id: str, *, page_size: int | None = None, timeout: Timeout = None
    ) -> AsyncIterator[LogEntry]:
        """Every chain batch of the project, in sequence order, across all pages."""
        return self._iter_pages(
            lambda cursor: self.list_logs(project_id, cursor=cursor, page_size=page_size, timeout=timeout)
        )

    async def list_manifests(
        self, project_id: str, *, cursor: str | None = None, page_size: int | None = None, timeout: Timeout = None
    ) -> Page[Manifest]:
        """One page of the project's signed chain manifests (``GET /v1/manifests``)."""
        return await self._list(_ops.MANIFESTS_PATH, Manifest, project_id, cursor, page_size, timeout)

    def iter_manifests(
        self, project_id: str, *, page_size: int | None = None, timeout: Timeout = None
    ) -> AsyncIterator[Manifest]:
        """Every chain manifest of the project, in sequence order, across all pages."""
        return self._iter_pages(
            lambda cursor: self.list_manifests(project_id, cursor=cursor, page_size=page_size, timeout=timeout)
        )

    async def list_checkpoints(
        self, project_id: str, *, cursor: str | None = None, page_size: int | None = None, timeout: Timeout = None
    ) -> Page[Checkpoint]:
        """One page of the project's signed checkpoints, newest first (``GET /v1/checkpoints``)."""
        return await self._list(_ops.CHECKPOINTS_PATH, Checkpoint, project_id, cursor, page_size, timeout)

    def iter_checkpoints(
        self, project_id: str, *, page_size: int | None = None, timeout: Timeout = None
    ) -> AsyncIterator[Checkpoint]:
        """Every checkpoint of the project, newest first, across all pages."""
        return self._iter_pages(
            lambda cursor: self.list_checkpoints(project_id, cursor=cursor, page_size=page_size, timeout=timeout)
        )

    async def jwks(self, project_id: str, *, timeout: Timeout = None) -> KeySet:
        """The public keys behind every signature (``GET /.well-known/jwks.json``)."""
        response = await self._send(_ops.jwks_spec(project_id), timeout=timeout)
        return KeySet.model_validate(response.json())
