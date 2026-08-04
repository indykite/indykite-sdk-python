"""Models for the Entity Matching API (``/entity-matching/v1``).

Spec: https://openapi.indykite.com/v1/entitymatching.yaml (the run/status
endpoints are live but not yet published in the spec).
"""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from indykite_sdk._core.models import IKModel, IKResponseModel

__all__ = [
    "CustomPropertyMapping",
    "PipelineRun",
    "PipelineStatus",
    "PropertyMappings",
    "SuggestedPropertyMapping",
]


class CustomPropertyMapping(IKModel):
    """A rule matching one source-node property against one target-node property."""

    source_node_property: str
    target_node_property: str


class SuggestedPropertyMapping(IKResponseModel):
    """A system-suggested mapping with its similarity score."""

    source_node_type: str | None = None
    source_node_property: str | None = None
    target_node_type: str | None = None
    target_node_property: str | None = None
    similarity_score_cutoff: float | None = None


class PropertyMappings(IKResponseModel):
    """Suggested property mappings for a pipeline."""

    id: str | None = None
    suggested_property_mappings: list[SuggestedPropertyMapping] = []


class PipelineRun(IKResponseModel):
    """Confirmation of a triggered pipeline run."""

    id: str | None = None
    etag: str | None = None
    last_run_time: str | None = None


class PipelineStatus(IKResponseModel):
    """Statuses of the pipeline's two steps.

    Values are ``INVALID``, ``PENDING``, ``IN_PROGRESS``, ``SUCCESS``, or ``ERROR``.
    """

    id: str | None = None
    property_mapping_status: str | None = None
    entity_matching_status: str | None = None


SimilarityScoreCutoff = Annotated[float, Field(ge=0.0, le=1.0)]
