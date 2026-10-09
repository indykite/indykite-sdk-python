"""Sans-IO CRUD plumbing shared by all Config API resources."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

import httpx

from indykite_sdk._core.ops import RequestSpec
from indykite_sdk.config.models.common import _ETagged


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


def read_spec(path: str, resource_id: str, *, version: int | None = None, project_id: str | None = None) -> RequestSpec:
    """Build a read request for an ID, or for a name scoped by ``project_id``."""
    params: dict[str, Any] = {}
    if version is not None:
        params["version"] = version
    if project_id is not None:
        params["project_id"] = project_id
    return RequestSpec("GET", f"{path}/{quote(resource_id, safe=':')}", params=params)


def update_spec(path: str, resource_id: str, body: dict[str, Any], etag: str | None) -> RequestSpec:
    """Build an update request, sent with ``If-Match`` when an etag is given."""
    return RequestSpec(
        "PUT", f"{path}/{quote(resource_id, safe=':')}", json_body=clean_body(body), headers=_if_match(etag)
    )


def delete_spec(path: str, resource_id: str, etag: str | None) -> RequestSpec:
    """Build a delete request, sent with ``If-Match`` when an etag is given."""
    return RequestSpec("DELETE", f"{path}/{quote(resource_id, safe=':')}", headers=_if_match(etag))


def unguarded_delete_spec(path: str, resource_id: str) -> RequestSpec:
    """Build a delete request without ``If-Match``, for resources whose delete takes no etag."""
    return RequestSpec("DELETE", f"{path}/{quote(resource_id, safe=':')}")


def _if_match(etag: str | None) -> dict[str, str]:
    """``If-Match`` makes the API reject the change when the resource changed since ``etag`` was read."""
    return {"If-Match": etag} if etag else {}


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
