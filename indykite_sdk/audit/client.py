"""Synchronous Audit Log client."""

from __future__ import annotations

from collections.abc import Callable, Iterator

import httpx

from indykite_sdk._core.http import (
    DEFAULT_TIMEOUT,
    BaseSyncClient,
    new_sync_client,
    send_sync,
)
from indykite_sdk._core.retry import DEFAULT_RETRY, RetryConfig
from indykite_sdk.audit import _ops
from indykite_sdk.audit.models import Checkpoint, KeySet, LogEntry, Manifest, Page

__all__ = ["AuditClient", "fetch_jwks"]

type Timeout = httpx.Timeout | float | None


class AuditClient(BaseSyncClient):
    """Read a project's tamper-proof audit trail via the Audit Log API (``/audit``).

    Authenticates with the raw **application-agent credential token**
    (``INDYKITE_APPLICATION_CREDENTIALS[_FILE]``) sent as ``X-IK-ClientKey``.
    The agent needs the ``Audit`` API permission, and ``project_id`` must be
    the project the agent belongs to: another project answers 403, a missing
    permission 401.

    Every listing returns one :class:`~indykite_sdk.audit.Page`; the ``iter_*``
    methods follow ``next_cursor`` through every page. Logs and manifests page
    in sequence order from the start of the chain, checkpoints newest first.
    ``page_size`` is 1 to 50.

    Example::

        from indykite_sdk import AuditClient

        with AuditClient() as client:
            for batch in client.iter_logs("gid:project"):
                for event in batch.data:
                    print(batch.sequence, event)
            keys = client.jwks("gid:project")  # the public keys behind every signature
    """

    _api_prefix = _ops.API_PREFIX
    _auth_kind = "app_agent"

    def _list[ItemT](
        self,
        path: str,
        item_cls: type[ItemT],
        project_id: str,
        cursor: str | None,
        page_size: int | None,
        timeout: Timeout,
    ) -> Page[ItemT]:
        spec = _ops.list_spec(path, project_id, cursor, page_size)
        return Page[item_cls].model_validate(self._send(spec, timeout=timeout).json())  # type: ignore[valid-type]

    @staticmethod
    def _iter_pages[ItemT](
        list_page: Callable[[str | None], Page[ItemT]],
    ) -> Iterator[ItemT]:
        """Yield the items of every page, following ``next_cursor`` while ``has_more``."""
        cursor: str | None = None
        while True:
            page = list_page(cursor)
            yield from page.items
            cursor = _ops.next_cursor(cursor, page.next_cursor, page.has_more)
            if cursor is None:
                return

    # -- logs ------------------------------------------------------------------

    def list_logs(
        self, project_id: str, *, cursor: str | None = None, page_size: int | None = None, timeout: Timeout = None
    ) -> Page[LogEntry]:
        """One page of the project's signed chain batches, the audit events (``GET /v1/logs``).

        Args:
            project_id: The project GID the application agent belongs to.
            cursor: ``next_cursor`` of the previous page; omit for the first page.
            page_size: Items per page, 1 to 50 (the platform default and maximum).
        """
        return self._list(_ops.LOGS_PATH, LogEntry, project_id, cursor, page_size, timeout)

    def iter_logs(
        self, project_id: str, *, page_size: int | None = None, timeout: Timeout = None
    ) -> Iterator[LogEntry]:
        """Every chain batch of the project, in sequence order, across all pages."""
        return self._iter_pages(
            lambda cursor: self.list_logs(project_id, cursor=cursor, page_size=page_size, timeout=timeout)
        )

    # -- manifests ---------------------------------------------------------------

    def list_manifests(
        self, project_id: str, *, cursor: str | None = None, page_size: int | None = None, timeout: Timeout = None
    ) -> Page[Manifest]:
        """One page of the project's signed chain manifests (``GET /v1/manifests``).

        Manifests carry the chain linkage (``prev_hash`` / ``head_hash``) without
        the batch payloads and page in lockstep with :meth:`list_logs`: the same
        cursor covers the same sequences on both endpoints.
        """
        return self._list(_ops.MANIFESTS_PATH, Manifest, project_id, cursor, page_size, timeout)

    def iter_manifests(
        self, project_id: str, *, page_size: int | None = None, timeout: Timeout = None
    ) -> Iterator[Manifest]:
        """Every chain manifest of the project, in sequence order, across all pages."""
        return self._iter_pages(
            lambda cursor: self.list_manifests(project_id, cursor=cursor, page_size=page_size, timeout=timeout)
        )

    # -- checkpoints -------------------------------------------------------------

    def list_checkpoints(
        self, project_id: str, *, cursor: str | None = None, page_size: int | None = None, timeout: Timeout = None
    ) -> Page[Checkpoint]:
        """One page of the project's signed checkpoints, newest first (``GET /v1/checkpoints``)."""
        return self._list(_ops.CHECKPOINTS_PATH, Checkpoint, project_id, cursor, page_size, timeout)

    def iter_checkpoints(
        self, project_id: str, *, page_size: int | None = None, timeout: Timeout = None
    ) -> Iterator[Checkpoint]:
        """Every checkpoint of the project, newest first, across all pages."""
        return self._iter_pages(
            lambda cursor: self.list_checkpoints(project_id, cursor=cursor, page_size=page_size, timeout=timeout)
        )

    # -- keys --------------------------------------------------------------------

    def jwks(self, project_id: str, *, timeout: Timeout = None) -> KeySet:
        """The public keys behind the batch, manifest and checkpoint signatures (``GET /.well-known/jwks.json``).

        The endpoint is public: the request carries no credential, and
        :func:`fetch_jwks` reads the same keys without a client.
        ``project_id`` is required but does not select a key today.
        Keep the set next to an exported trail: it names the keys the export
        was signed with, and a ``kid`` missing from a later set was rotated out.
        """
        return KeySet.model_validate(self._send(_ops.jwks_spec(project_id), timeout=timeout).json())


def fetch_jwks(
    project_id: str,
    *,
    base_url: str | None = None,
    region: str | None = None,
    timeout: Timeout = None,
    retries: RetryConfig | None = DEFAULT_RETRY,
    http_client: httpx.Client | None = None,
) -> KeySet:
    """Read the audit signing keys without credentials (``GET /audit/.well-known/jwks.json``).

    The endpoint is public, so a system that verifies an exported trail needs
    no application agent. The host resolves like the clients' base URL:
    ``base_url``, then ``INDYKITE_BASE_URL``, then ``region`` or
    ``INDYKITE_REGION``, then the default region. A passed ``http_client`` is
    used as-is - its base URL, auth, headers and timeout are left unchanged -
    and left open; credential headers it carries are not sent.

    Example::

        from indykite_sdk.audit import fetch_jwks

        keys = fetch_jwks("gid:project", region="eu")
    """
    spec, api_url = _ops.public_jwks_spec(project_id, base_url, region)
    client = new_sync_client(http_client)
    try:
        response = send_sync(
            client,
            spec,
            base_url=api_url,
            retries=retries,
            auth_kind="public",
            timeout=timeout if timeout is not None else DEFAULT_TIMEOUT,
        )
    finally:
        if http_client is None:
            client.close()
    return KeySet.model_validate(response.json())
