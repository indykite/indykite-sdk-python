"""Synchronous Entity Matching client."""

from __future__ import annotations

import time
from collections.abc import Sequence
from typing import Any
from urllib.parse import quote

import httpx

from indykite_sdk._core.http import BaseSyncClient
from indykite_sdk._core.ops import RequestSpec
from indykite_sdk.entity_matching.models import (
    CustomPropertyMapping,
    PipelineRun,
    PipelineStatus,
    PropertyMappings,
)
from indykite_sdk.errors import PipelineTimeoutError, RequestValidationError

__all__ = ["EntityMatchingClient"]

#: Step statuses that mean the step is no longer running. The API reports
#: PENDING, IN_PROGRESS, SUCCESS or ERROR.
FINAL_STATUSES = frozenset({"SUCCESS", "ERROR"})


def _run_body(
    similarity_score_cutoff: float,
    custom_property_mappings: Sequence[CustomPropertyMapping | dict[str, Any]] | None,
) -> dict[str, Any]:
    if (
        isinstance(similarity_score_cutoff, bool)
        or not isinstance(similarity_score_cutoff, int | float)
        or not 0 <= similarity_score_cutoff <= 1
    ):
        raise RequestValidationError(
            f"similarity_score_cutoff must be a number from 0 to 1, got {similarity_score_cutoff!r}."
        )
    body: dict[str, Any] = {"similarity_score_cutoff": similarity_score_cutoff}
    if custom_property_mappings:
        mappings = [
            item if isinstance(item, CustomPropertyMapping) else CustomPropertyMapping.model_validate(item)
            for item in custom_property_mappings
        ]
        body["custom_property_mappings"] = [mapping.to_wire() for mapping in mappings]
    return body


def _parse_property_mappings(pipeline_id: str, response: httpx.Response) -> PropertyMappings:
    """Parse the mappings, or mark them pending when the API answers 202 Accepted."""
    data = response.json() if response.content else {}
    if response.status_code == httpx.codes.ACCEPTED:
        return PropertyMappings(
            id=pipeline_id, pending=True, message=data.get("message"), details=data.get("details") or []
        )
    return PropertyMappings.model_validate(data)


def _is_complete(status: PipelineStatus) -> bool:
    return (status.entity_matching_status or "").upper() in FINAL_STATUSES


class EntityMatchingClient(BaseSyncClient):
    """Trigger and monitor entity-matching pipeline runs (``/entity-matching/v1``).

    Authenticates with the raw **application-agent credential token**
    (``INDYKITE_APPLICATION_CREDENTIALS[_FILE]``) sent as ``X-IK-ClientKey``.
    Pipelines themselves are created via the Config API
    (:meth:`indykite_sdk.ConfigClient.create_entity_matching_pipeline`).

    Example::

        from indykite_sdk import EntityMatchingClient

        with EntityMatchingClient() as client:
            mappings = client.read_property_mappings("gid:pipeline-id")
            client.run_pipeline("gid:pipeline-id", similarity_score_cutoff=0.9)
            status = client.wait_for_completion("gid:pipeline-id")
    """

    _api_prefix = "/entity-matching/v1"
    _auth_kind = "app_agent"

    def read_property_mappings(
        self, pipeline_id: str, *, timeout: httpx.Timeout | float | None = None
    ) -> PropertyMappings:
        """Read system-suggested property mappings (``GET /pipelines/{id}/property-mappings``).

        While the mappings are not ready the API answers 202 Accepted; the
        result then has ``pending=True`` and no suggestions.
        """
        response = self._send(
            RequestSpec("GET", f"/pipelines/{quote(pipeline_id, safe=':')}/property-mappings"), timeout=timeout
        )
        return _parse_property_mappings(pipeline_id, response)

    def run_pipeline(
        self,
        pipeline_id: str,
        *,
        similarity_score_cutoff: float,
        custom_property_mappings: Sequence[CustomPropertyMapping | dict[str, Any]] | None = None,
        timeout: httpx.Timeout | float | None = None,
    ) -> PipelineRun:
        """Trigger a pipeline run (``POST /pipelines/{id}/runs``).

        Args:
            similarity_score_cutoff: Threshold in [0, 1] above which entities
                are matched automatically.
            custom_property_mappings: Optional overrides of the pipeline's
                stored mapping rules.
        """
        spec = RequestSpec(
            "POST",
            f"/pipelines/{quote(pipeline_id, safe=':')}/runs",
            json_body=_run_body(similarity_score_cutoff, custom_property_mappings),
        )
        return PipelineRun.model_validate(self._send(spec, timeout=timeout).json())

    def read_status(self, pipeline_id: str, *, timeout: httpx.Timeout | float | None = None) -> PipelineStatus:
        """Read the pipeline's step statuses (``GET /pipelines/{id}/status``)."""
        response = self._send(RequestSpec("GET", f"/pipelines/{quote(pipeline_id, safe=':')}/status"), timeout=timeout)
        return PipelineStatus.model_validate(response.json())

    def wait_for_completion(
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
            status = self.read_status(pipeline_id)
            if _is_complete(status):
                return status
            if time.monotonic() + poll_interval > deadline:
                raise PipelineTimeoutError(
                    f"Entity-matching pipeline {pipeline_id} did not complete within {timeout:.0f}s "
                    f"(last status: {status.entity_matching_status})."
                )
            time.sleep(poll_interval)
