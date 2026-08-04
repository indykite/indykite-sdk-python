"""Asynchronous ContX IQ client."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

import httpx

from indykite_sdk._core.http import BaseAsyncClient
from indykite_sdk._core.ops import RequestSpec, user_token_headers
from indykite_sdk.ciq.client import _execute_body
from indykite_sdk.ciq.models import ExecuteRecord, ExecuteResponse

__all__ = ["AsyncCIQClient"]


class AsyncCIQClient(BaseAsyncClient):
    """Async variant of :class:`indykite_sdk.CIQClient` - same methods, ``await``-able.

    Example::

        from indykite_sdk import AsyncCIQClient

        async with AsyncCIQClient() as client:
            result = await client.execute("gid:AAAAI3CpKUguokArp0rY8oQW9eo")
    """

    _api_prefix = "/contx-iq/v1"
    _auth_kind = "app_agent"

    async def execute(
        self,
        query: str,
        *,
        input_params: dict[str, Any] | None = None,
        preprocess_params: dict[str, str] | None = None,
        page_size: int | None = None,
        page_token: int | None = None,
        user_token: str | None = None,
        timeout: httpx.Timeout | float | None = None,
    ) -> ExecuteResponse:
        """Execute one page of a knowledge query (``POST /execute``)."""
        spec = RequestSpec(
            "POST",
            "/execute",
            json_body=_execute_body(query, input_params, preprocess_params, page_size, page_token),
            headers=user_token_headers(user_token),
        )
        return ExecuteResponse.model_validate((await self._send(spec, timeout=timeout)).json())

    async def execute_iter(
        self,
        query: str,
        *,
        input_params: dict[str, Any] | None = None,
        preprocess_params: dict[str, str] | None = None,
        page_size: int = 100,
        user_token: str | None = None,
        timeout: httpx.Timeout | float | None = None,
    ) -> AsyncIterator[ExecuteRecord]:
        """Iterate over all records of a query, fetching pages transparently."""
        page_token = 1
        while True:
            response = await self.execute(
                query,
                input_params=input_params,
                preprocess_params=preprocess_params,
                page_size=page_size,
                page_token=page_token,
                user_token=user_token,
                timeout=timeout,
            )
            for record in response.data:
                yield record
            if len(response.data) < page_size:
                return
            page_token += 1
