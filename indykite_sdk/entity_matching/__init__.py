"""Entity Matching API — trigger and monitor entity-matching pipeline runs."""

from indykite_sdk.entity_matching.aio import AsyncEntityMatchingClient
from indykite_sdk.entity_matching.client import EntityMatchingClient
from indykite_sdk.entity_matching.models import (
    CustomPropertyMapping,
    PipelineRun,
    PipelineStatus,
    PropertyMappings,
    SuggestedPropertyMapping,
)

__all__ = [
    "AsyncEntityMatchingClient",
    "CustomPropertyMapping",
    "EntityMatchingClient",
    "PipelineRun",
    "PipelineStatus",
    "PropertyMappings",
    "SuggestedPropertyMapping",
]
