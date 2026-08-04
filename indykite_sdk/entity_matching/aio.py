"""Asynchronous Entity Matching client."""

from __future__ import annotations

import asyncio
import time
from collections.abc import Sequence
from typing import Any

import httpx

from indykite_sdk._core.http import BaseAsyncClient
from indykite_sdk._core.ops import RequestSpec
from indykite_sdk.entity_matching.client import _is_complete, _run_body
from indykite_sdk.entity_matching.models import (
    CustomPropertyMapping,
    PipelineRun,
    PipelineStatus,
    PropertyMappings,
)
from indykite_sdk.errors import PipelineTimeoutError

__all__ = ["AsyncEntityMatchingClient"]


class AsyncEntityMatchingClient(BaseAsyncClient):
    """Async variant of :class:`indykite_sdk.EntityMatchingClient`."""

    _api_prefix = "/entity-matching/v1"
    _auth_kind = "app_agent"

    async def read_property_mappings(
        self, pipeline_id: str, *, timeout: httpx.Timeout | float | None = None
    ) -> PropertyMappings:
        """Read system-suggested property mappings (``GET /pipelines/{id}/property-mappings``)."""
        response = await self._send(RequestSpec("GET", f"/pipelines/{pipeline_id}/property-mappings"), timeout=timeout)
        return PropertyMappings.model_validate(response.json())

    async def run_pipeline(
        self,
        pipeline_id: str,
        *,
        similarity_score_cutoff: float,
        custom_property_mappings: Sequence[CustomPropertyMapping | dict[str, Any]] | None = None,
        timeout: httpx.Timeout | float | None = None,
    ) -> PipelineRun:
        """Trigger a pipeline run (``POST /pipelines/{id}/runs``). **Experimental** (not in public spec)."""
        spec = RequestSpec(
            "POST",
            f"/pipelines/{pipeline_id}/runs",
            json_body=_run_body(similarity_score_cutoff, custom_property_mappings),
        )
        return PipelineRun.model_validate((await self._send(spec, timeout=timeout)).json())

    async def read_status(self, pipeline_id: str, *, timeout: httpx.Timeout | float | None = None) -> PipelineStatus:
        """Read the pipeline's step statuses (``GET /pipelines/{id}/status``). **Experimental** (not in public spec)."""
        response = await self._send(RequestSpec("GET", f"/pipelines/{pipeline_id}/status"), timeout=timeout)
        return PipelineStatus.model_validate(response.json())

    async def wait_for_completion(
        self,
        pipeline_id: str,
        *,
        timeout: float = 600.0,
        poll_interval: float = 10.0,
    ) -> PipelineStatus:
        """Poll :meth:`read_status` until the matching step reaches a final status.

        Raises:
            PipelineTimeoutError: no final status within ``timeout`` seconds.
        """
        deadline = time.monotonic() + timeout
        while True:
            status = await self.read_status(pipeline_id)
            if _is_complete(status):
                return status
            if time.monotonic() + poll_interval > deadline:
                raise PipelineTimeoutError(
                    f"Entity-matching pipeline {pipeline_id} did not complete within {timeout:.0f}s "
                    f"(last status: {status.entity_matching_status})."
                )
            await asyncio.sleep(poll_interval)
