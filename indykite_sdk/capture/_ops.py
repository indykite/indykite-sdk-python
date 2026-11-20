"""Sans-IO request building shared by the sync and async Capture clients."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import httpx
from pydantic import ValidationError

from indykite_sdk._core.models import IKModel
from indykite_sdk._core.ops import RequestSpec
from indykite_sdk.capture.models import (
    LOCATION_DEFAULT,
    LOCATION_GLOBAL,
    MAX_BATCH_SIZE,
    BatchResult,
    BatchResults,
)
from indykite_sdk.errors import RequestValidationError


def coerce_items[ModelT: IKModel](
    items: Sequence[ModelT | dict[str, Any]], model_cls: type[ModelT], what: str
) -> list[ModelT]:
    """Validate a batch of models/dicts, mapping validation failures to :class:`RequestValidationError`."""
    if not items:
        raise RequestValidationError(f"At least one {what} is required.")
    coerced: list[ModelT] = []
    for index, item in enumerate(items):
        try:
            coerced.append(item if isinstance(item, model_cls) else model_cls.model_validate(item))
        except ValidationError as exc:
            raise RequestValidationError(f"Invalid {what} at index {index}: {exc}") from exc
    return coerced


def request_locations(items: Sequence[IKModel]) -> frozenset[str]:
    """Collect the locations named by the nodes of a batch.

    A node entry carries its own location; a relationship entry is routed by
    the locations of its source and target nodes.
    """
    locations: set[str] = set()
    for item in items:
        nodes = (item.source, item.target) if hasattr(item, "source") else (item,)
        locations.update(node.location for node in nodes if node.location)
    return frozenset(locations)


def batch_specs[ModelT: IKModel](
    path: str,
    field_name: str,
    items: list[ModelT],
    *,
    auto_chunk: bool,
) -> list[tuple[int, RequestSpec, frozenset[str]]]:
    """Split ``items`` into request specs of at most 250 items each.

    Returns ``(start_index, spec, locations)`` triples: the start index lets
    callers report where a chunk failed, and the locations of the chunk select
    the shape its response is parsed in.
    """
    if len(items) > MAX_BATCH_SIZE and not auto_chunk:
        raise RequestValidationError(
            f"The Capture API accepts at most {MAX_BATCH_SIZE} items per request, got {len(items)}. "
            f"Pass auto_chunk=True to split the batch automatically."
        )
    specs: list[tuple[int, RequestSpec, frozenset[str]]] = []
    for start in range(0, len(items), MAX_BATCH_SIZE):
        chunk = items[start : start + MAX_BATCH_SIZE]
        body: dict[str, Any] = {field_name: [item.to_wire() for item in chunk]}
        specs.append((start, RequestSpec("POST", path, json_body=body), request_locations(chunk)))
    return specs


def parse_batch_results(response: httpx.Response, locations: frozenset[str]) -> BatchResults:
    """Parse a batch response in the shape the request selects.

    The API answers ``{"results": [...]}`` when no node of the request has a
    location, and ``{"<location>": [gid, ...]}`` otherwise. In the second shape
    only the request's locations, plus the default and global keys the API can
    add on its own, are read as locations.
    """
    data = response.json() if response.content else {}
    if not isinstance(data, dict):
        data = {}
    if not locations:
        return BatchResults(results=[BatchResult.model_validate(result) for result in data.get("results") or []])
    known = locations | {LOCATION_DEFAULT, LOCATION_GLOBAL}
    return BatchResults(by_location={key: list(gids or []) for key, gids in data.items() if key in known})
