"""Asynchronous Data Schema client."""

from __future__ import annotations

import httpx

from indykite_sdk._core.http import BaseAsyncClient
from indykite_sdk._core.ops import RequestSpec
from indykite_sdk.data_schema.models import DataSchema

__all__ = ["AsyncDataSchemaClient"]


class AsyncDataSchemaClient(BaseAsyncClient):
    """Async variant of :class:`indykite_sdk.DataSchemaClient`."""

    _api_prefix = "/data-schema/v1"
    _auth_kind = "app_agent"

    async def read(self, *, timeout: httpx.Timeout | float | None = None) -> DataSchema:
        """Read the data schema in JGF v2 format (``GET /``)."""
        response = await self._send(RequestSpec("GET", ""), timeout=timeout)
        return DataSchema.model_validate(response.json())
