"""Models for the Capture API (``/capture/v1``).

Spec: https://openapi.indykite.com/v1/capture.yaml
"""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import Field

from indykite_sdk._core.models import IKModel, IKResponseModel

__all__ = [
    "BaseProperty",
    "LOCATION_DEFAULT",
    "LOCATION_GLOBAL",
    "BatchResult",
    "BatchResults",
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

#: The :attr:`BatchResults.by_location` key for entries without a location.
#: It is reserved: a node ``location`` must not use it.
LOCATION_DEFAULT = "__default"

#: The location of the global database of a composite IKG. In
#: :attr:`BatchResults.by_location` it holds the global nodes, the node proxies,
#: and the relationships between nodes of different locations.
LOCATION_GLOBAL = "global"


class Metadata(IKModel):
    """Provenance metadata attached to a single property value."""

    assurance_level: Literal[1, 2, 3] | None = None
    verified_time: str | None = None
    source: str | None = None
    custom_metadata: dict[str, Any] | None = None


class BaseProperty(IKModel):
    """A relationship property: a direct ``value`` or an ``external_value`` reference, without metadata."""

    type: _PropertyType
    value: PropertyValue | None = None
    external_value: str | None = None


class Property(IKModel):
    """A typed property with either a direct ``value`` or an ``external_value`` reference."""

    type: _PropertyType
    value: PropertyValue | None = None
    external_value: str | None = None
    metadata: Metadata | None = None


class NodeRef(IKModel):
    """A reference to an existing node by ``external_id`` and ``type``.

    On a composite IKG, ``location`` routes the node to the database of that
    location. A relationship has no location of its own: it lives in the
    database of its source and target nodes when both have the same location,
    and in the global database when they differ.
    """

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

    ``create_proxy`` asks for a proxy of the node (external ID, type and
    location only) in the global database of a composite IKG. It is ignored for
    a node in the global location and in a request where no node has a location.
    """

    external_id: _ExternalId
    type: _NodeType
    is_identity: bool | None = None
    labels: list[str] | None = None
    location: _Location | None = None
    create_proxy: bool | None = None
    properties: list[Property] | None = None


class Relationship(IKModel):
    """A relationship between two existing nodes, optionally with properties."""

    type: _PropertyType
    source: NodeRef
    target: NodeRef
    properties: list[BaseProperty] | None = None


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
    properties: list[BaseProperty] | None = None


class BatchResult(IKResponseModel):
    """Per-item result of a batch capture call."""

    id: str | None = None


class BatchResults(IKResponseModel):
    """The outcome of a batch capture call.

    Exactly one of the two fields is filled, depending on the request:

    - ``results``, when no node of the request has a location.
    - ``by_location``, when at least one node has a location (composite IKG).

    ``by_location`` lists the affected node or relationship GIDs per location,
    in request order. Entries without a location are under
    :data:`LOCATION_DEFAULT`, and a location where nothing was found has an
    empty list. For a node upsert or delete, :data:`LOCATION_GLOBAL` holds the
    global nodes followed by the node proxies; an ``auto_chunk`` call keeps
    that order per chunk only.
    """

    results: list[BatchResult] = []
    by_location: dict[str, list[str]] | None = None

    def merge(self, other: BatchResults) -> None:
        """Append the results of ``other``, keeping the per-location grouping.

        The chunks of one call can mix both shapes. Once any chunk is
        per-location, the plain results move under :data:`LOCATION_DEFAULT`,
        so that still only one of the two fields is filled.
        """
        if self.by_location is None and other.by_location is None:
            self.results.extend(other.results)
            return
        if self.by_location is None:
            self.by_location = {}
        plain = [result.id for result in (*self.results, *other.results) if result.id is not None]
        if plain:
            self.by_location.setdefault(LOCATION_DEFAULT, []).extend(plain)
        self.results = []
        for location, gids in (other.by_location or {}).items():
            self.by_location.setdefault(location, []).extend(gids)
