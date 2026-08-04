"""Shared Config API model shapes.

Every Config API resource follows the same lifecycle: create returns
``{id, create_time, created_by}`` plus an ``ETag`` response header; read
returns the full resource plus its ``ETag``; update and delete are guarded by
``If-Match`` and a stale etag fails with HTTP 412
(:class:`indykite_sdk.ETagMismatchError`).
"""

from __future__ import annotations

from typing import Any

from indykite_sdk._core.models import IKResponseModel

__all__ = ["ConfigResource", "CreateResult", "UpdateResult"]


class _ETagged(IKResponseModel):
    """A response paired with the ``ETag`` header needed for later update/delete."""

    #: Concurrency-control version from the ``ETag`` response header.
    #: Pass it as ``etag=`` to the matching ``update_*``/``delete_*`` call.
    etag: str | None = None


class CreateResult(_ETagged):
    """Confirmation of a created configuration."""

    id: str | None = None
    create_time: str | None = None
    created_by: str | None = None


class UpdateResult(_ETagged):
    """Confirmation of an updated configuration."""

    id: str | None = None
    create_time: str | None = None
    created_by: str | None = None
    update_time: str | None = None
    updated_by: str | None = None


class ConfigResource(_ETagged):
    """A configuration resource whose full payload the SDK does not (yet) type.

    The fields common to every Config API resource are typed; everything else
    the API returns is kept verbatim (``resource.model_extra`` or attribute
    access) so no data is lost.
    """

    id: str | None = None
    name: str | None = None
    display_name: str | None = None
    description: str | None = None
    project_id: str | None = None
    organization_id: str | None = None
    create_time: str | None = None
    created_by: str | None = None
    update_time: str | None = None
    updated_by: str | None = None

    def field(self, name: str, default: Any = None) -> Any:
        """Read any resource field, typed or not.

        Example: ``sink.field("provider")``.
        """
        if name in dict(type(self).model_fields):
            return getattr(self, name)
        return (self.model_extra or {}).get(name, default)
