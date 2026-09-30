"""Sans-IO request building shared by the sync and async Audit Log clients."""

from __future__ import annotations

from typing import Any

from indykite_sdk._core.ops import RequestSpec
from indykite_sdk.errors import IndyKiteError, RequestValidationError

LOGS_PATH = "/v1/logs"
MANIFESTS_PATH = "/v1/manifests"
CHECKPOINTS_PATH = "/v1/checkpoints"
JWKS_PATH = "/.well-known/jwks.json"


def _project_id(project_id: str) -> str:
    project_id = (project_id or "").strip()
    if not project_id:
        raise RequestValidationError(
            "project_id is required: the project GID the application agent belongs to (``gid:...``)."
        )
    return project_id


def list_spec(path: str, project_id: str, cursor: str | None, page_size: int | None) -> RequestSpec:
    """Build one page request of a listing endpoint (``project_id``, ``cursor``, ``pagesize``).

    ``page_size`` must be positive; the platform caps values above 50 to 50.
    """
    params: dict[str, Any] = {"project_id": _project_id(project_id)}
    if cursor:
        params["cursor"] = cursor
    if page_size is not None:
        if page_size < 1:
            raise RequestValidationError(f"page_size must be a positive integer, got {page_size}.")
        params["pagesize"] = page_size
    return RequestSpec("GET", path, params=params)


def jwks_spec(project_id: str) -> RequestSpec:
    """Build the JWKS request; ``project_id`` is required but does not select a key today."""
    return RequestSpec("GET", JWKS_PATH, params={"project_id": _project_id(project_id)})


def next_cursor(cursor: str | None, page_next_cursor: str | None, has_more: bool) -> str | None:
    """The cursor of the following page, or ``None`` when this was the last one.

    Guards against a server handing out the cursor it was just given, which
    would otherwise page forever.
    """
    if not has_more:
        return None
    if not page_next_cursor or page_next_cursor == cursor:
        raise IndyKiteError("The Audit Log API returned a page that does not advance the cursor; stopping.")
    return page_next_cursor
