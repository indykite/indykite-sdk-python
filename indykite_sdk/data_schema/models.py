"""Models for the Data Schema API (``/data-schema/v1``).

Spec: https://openapi.indykite.com/v1/dataschema.yaml - the schema comes back
in JGF v2 (JSON Graph Format).
"""

from __future__ import annotations

from typing import Any

from indykite_sdk._core.models import IKResponseModel

__all__ = ["DataSchema"]


class DataSchema(IKResponseModel):
    """The project's IKG data schema as a JGF v2 graph.

    ``graph`` holds the raw JGF content: ``nodes`` (node types with property
    statistics), ``edges`` (relationship types), and ``metadata``.
    """

    graph: dict[str, Any] = {}

    @property
    def node_types(self) -> list[str]:
        """Names of the node types present in the schema."""
        return list((self.graph.get("nodes") or {}).keys())

    @property
    def relationship_types(self) -> list[str]:
        """Relationship type names present in the schema."""
        return sorted({edge.get("relation", "") for edge in self.graph.get("edges") or [] if edge.get("relation")})
