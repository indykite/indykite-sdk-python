"""Synchronous Data Schema client."""

from __future__ import annotations

import httpx

from indykite_sdk._core.http import BaseSyncClient
from indykite_sdk._core.ops import RequestSpec
from indykite_sdk.data_schema.models import DataSchema

__all__ = ["DataSchemaClient"]


class DataSchemaClient(BaseSyncClient):
    """Read the project's IKG data schema (``/data-schema/v1``).

    Authenticates with the raw **application-agent credential token**
    (``INDYKITE_APPLICATION_CREDENTIALS[_FILE]``) sent as ``X-IK-ClientKey``.

    Example::

        from indykite_sdk import DataSchemaClient

        with DataSchemaClient() as client:
            schema = client.read()
            print(schema.node_types)
    """

    _api_prefix = "/data-schema/v1"
    _auth_kind = "app_agent"

    def read(self, *, timeout: httpx.Timeout | float | None = None) -> DataSchema:
        """Read the data schema in JGF v2 format (``GET /``)."""
        response = self._send(RequestSpec("GET", ""), timeout=timeout)
        return DataSchema.model_validate(response.json())
