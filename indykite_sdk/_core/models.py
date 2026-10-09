"""Shared Pydantic base models."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator


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

    @model_validator(mode="before")
    @classmethod
    def _null_collections_take_defaults(cls, data: Any) -> Any:
        """A ``null`` sent for a list or dict field means "empty", not an error."""
        if not isinstance(data, dict):
            return data
        nulls = {
            field.alias or name
            for name, field in cls.model_fields.items()
            if isinstance(field.default, list | dict) and data.get(field.alias or name, ...) is None
        }
        return {key: value for key, value in data.items() if key not in nulls} if nulls else data
