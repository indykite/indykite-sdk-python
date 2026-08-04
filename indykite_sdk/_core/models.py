"""Shared Pydantic base models."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class IKModel(BaseModel):
    """Base for request models: unknown fields are rejected to catch typos early."""

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    def to_wire(self) -> dict[str, Any]:
        """Serialize for the wire: aliases on, ``None`` fields omitted."""
        return self.model_dump(by_alias=True, exclude_none=True)


class IKResponseModel(BaseModel):
    """Base for response models: unknown fields are kept, never rejected.

    The API may add fields at any time; response models must not break on them.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")
