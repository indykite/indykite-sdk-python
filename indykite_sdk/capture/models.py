"""Models for the Capture API (``/capture/v1``).

Spec: https://openapi.indykite.com/v1/capture.yaml
"""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import Field

from indykite_sdk._core.models import IKModel, IKResponseModel

__all__ = [
    "BatchResult",
    "DeleteNodeProperties",
    "DeleteNodePropertyMetadata",
    "DeleteRelationshipProperties",
    "Metadata",
    "NodeRef",
    "Property",
    "PropertyValue",
    "Relationship",
    "UpsertNode",
]

#: A capture property value: string, number, boolean, or an array of those.
PropertyValue = str | int | float | bool | list[str | int | float | bool]

_ExternalId = Annotated[str, Field(min_length=1, max_length=256)]
_NodeType = Annotated[str, Field(min_length=2, max_length=64)]
_Location = Annotated[str, Field(min_length=2, max_length=32)]
_PropertyType = Annotated[str, Field(max_length=128)]

#: Every batch endpoint accepts at most this many items per request.
MAX_BATCH_SIZE = 250


class Metadata(IKModel):
    """Provenance metadata attached to a single property value."""

    assurance_level: Literal[1, 2, 3] | None = None
    verified_time: str | None = None
    source: str | None = None
    custom_metadata: dict[str, Any] | None = None


class Property(IKModel):
    """A typed property with either a direct ``value`` or an ``external_value`` reference."""

    type: _PropertyType
    value: PropertyValue | None = None
    external_value: str | None = None
    metadata: Metadata | None = None


class NodeRef(IKModel):
    """A reference to an existing node by ``external_id`` and ``type``."""

    external_id: _ExternalId
    type: _NodeType
    location: _Location | None = None


class UpsertNode(IKModel):
    """A node to create or update in the IndyKite Knowledge Graph.

    Example::

        UpsertNode(
            external_id="millicent",
            type="Person",
            is_identity=True,
            properties=[Property(type="email", value="millicent@example.com")],
        )
    """

    external_id: _ExternalId
    type: _NodeType
    is_identity: bool | None = None
    labels: list[str] | None = None
    location: _Location | None = None
    properties: list[Property] | None = None


class Relationship(IKModel):
    """A relationship between two existing nodes, optionally with properties."""

    type: _PropertyType
    source: NodeRef
    target: NodeRef
    properties: list[Property] | None = None


class DeleteNodeProperties(IKModel):
    """Strip the named properties from a node; the node itself survives."""

    external_id: _ExternalId
    type: _NodeType
    property_types: list[str] = Field(min_length=1, max_length=250)
    location: _Location | None = None


class DeleteNodePropertyMetadata(IKModel):
    """Strip metadata fields from one property; the property and its value survive."""

    external_id: _ExternalId
    type: _NodeType
    property_type: str
    metadata_fields: list[str] = Field(min_length=1, max_length=250)
    location: _Location | None = None


class DeleteRelationshipProperties(IKModel):
    """Strip the named properties from a relationship; the relationship survives."""

    type: _PropertyType
    source: NodeRef
    target: NodeRef
    property_types: list[str] = Field(min_length=1, max_length=250)


class BatchResult(IKResponseModel):
    """Per-item result of a batch capture call."""

    id: str | None = None
