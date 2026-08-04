"""Sans-IO CRUD plumbing shared by all Config API resources."""

from __future__ import annotations

from typing import Any

import httpx

from indykite_sdk._core.ops import RequestSpec
from indykite_sdk.config.models.common import _ETagged
from indykite_sdk.errors import RequestValidationError


def clean_body(body: dict[str, Any]) -> dict[str, Any]:
    """Drop ``None`` values so optional kwargs never reach the wire."""
    return {key: value for key, value in body.items() if value is not None}


def list_spec(path: str, params: dict[str, Any]) -> RequestSpec:
    """Build a list request, dropping unset/false filters."""
    query = {key: value for key, value in params.items() if value is not None and value is not False}
    return RequestSpec("GET", path, params=query)


def create_spec(path: str, body: dict[str, Any]) -> RequestSpec:
    """Build a create request."""
    return RequestSpec("POST", path, json_body=clean_body(body))


def read_spec(path: str, resource_id: str, *, version: int | None = None, location: str | None = None) -> RequestSpec:
    """Build a read-by-id request."""
    params: dict[str, Any] = {}
    if version is not None:
        params["version"] = version
    if location is not None:
        params["location"] = location
    return RequestSpec("GET", f"{path}/{resource_id}", params=params)


def update_spec(path: str, resource_id: str, body: dict[str, Any], etag: str) -> RequestSpec:
    """Build an ``If-Match``-guarded update request."""
    _require_etag(etag)
    return RequestSpec("PUT", f"{path}/{resource_id}", json_body=clean_body(body), headers={"If-Match": etag})


def delete_spec(path: str, resource_id: str, etag: str) -> RequestSpec:
    """Build an ``If-Match``-guarded delete request."""
    _require_etag(etag)
    return RequestSpec("DELETE", f"{path}/{resource_id}", headers={"If-Match": etag})


def _require_etag(etag: str) -> None:
    if not etag or not isinstance(etag, str):
        raise RequestValidationError(
            "An etag is required for updates and deletes. Read the resource first and pass its "
            "`.etag` (from the ETag response header) so concurrent changes are detected."
        )


def parse_one[ModelT: _ETagged](model: type[ModelT], response: httpx.Response) -> ModelT:
    """Parse a single-resource response, attaching the ``ETag`` header."""
    data = response.json() if response.content else {}
    parsed = model.model_validate(data if isinstance(data, dict) else {})
    if etag := response.headers.get("ETag"):
        parsed.etag = etag
    return parsed


def parse_list[ModelT: _ETagged](model: type[ModelT], response: httpx.Response) -> list[ModelT]:
    """Parse a ``{"data": [...]}`` list envelope."""
    data = response.json() if response.content else {}
    items = data.get("data") or [] if isinstance(data, dict) else []
    return [model.model_validate(item) for item in items]
