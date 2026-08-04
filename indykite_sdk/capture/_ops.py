"""Sans-IO request building shared by the sync and async Capture clients."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import httpx
from pydantic import ValidationError

from indykite_sdk._core.models import IKModel
from indykite_sdk._core.ops import RequestSpec
from indykite_sdk.capture.models import MAX_BATCH_SIZE, BatchResult
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


def batch_specs[ModelT: IKModel](
    path: str,
    field_name: str,
    items: list[ModelT],
    *,
    auto_chunk: bool,
    extra_body: dict[str, Any] | None = None,
) -> list[tuple[int, RequestSpec]]:
    """Split ``items`` into request specs of at most 250 items each.

    Returns ``(start_index, spec)`` pairs so callers can report where a chunk
    failed. Without ``auto_chunk``, more than 250 items is a client-side error.
    """
    if len(items) > MAX_BATCH_SIZE and not auto_chunk:
        raise RequestValidationError(
            f"The Capture API accepts at most {MAX_BATCH_SIZE} items per request, got {len(items)}. "
            f"Pass auto_chunk=True to split the batch automatically."
        )
    specs: list[tuple[int, RequestSpec]] = []
    for start in range(0, len(items), MAX_BATCH_SIZE):
        chunk = items[start : start + MAX_BATCH_SIZE]
        body: dict[str, Any] = {field_name: [item.to_wire() for item in chunk]}
        if extra_body:
            body.update(extra_body)
        specs.append((start, RequestSpec("POST", path, json_body=body)))
    return specs


def parse_batch_results(response: httpx.Response) -> list[BatchResult]:
    """Parse a ``{"results": [...]}`` batch response envelope."""
    data = response.json() if response.content else {}
    results = data.get("results") or [] if isinstance(data, dict) else []
    return [BatchResult.model_validate(result) for result in results]
