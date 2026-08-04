"""Synchronous ContX IQ client."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import httpx

from indykite_sdk._core.http import BaseSyncClient
from indykite_sdk._core.ops import RequestSpec, user_token_headers
from indykite_sdk.ciq.models import ExecuteRecord, ExecuteResponse

__all__ = ["CIQClient"]


def _execute_body(
    query: str,
    input_params: dict[str, Any] | None,
    preprocess_params: dict[str, str] | None,
    page_size: int | None,
    page_token: int | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {"id": query}
    if input_params:
        body["input_params"] = input_params
    if preprocess_params:
        body["preprocess_params"] = preprocess_params
    if page_size is not None:
        body["page_size"] = page_size
    if page_token is not None:
        body["page_token"] = page_token
    return body


class CIQClient(BaseSyncClient):
    """Execute ContX IQ knowledge queries against the IndyKite Knowledge Graph.

    Authenticates with the raw **application-agent credential token**
    (``INDYKITE_APPLICATION_CREDENTIALS[_FILE]``) sent as ``X-IK-ClientKey``.
    Reads and policy-mediated writes both go through :meth:`execute` — the
    knowledge query (created via the Config API) defines what happens.

    Example::

        from indykite_sdk import CIQClient

        with CIQClient() as client:
            result = client.execute(
                "gid:AAAAI3CpKUguokArp0rY8oQW9eo",
                input_params={"personId": "ada"},
            )
            for record in result.data:
                print(record.nodes)
    """

    _api_prefix = "/contx-iq/v1"
    _auth_kind = "app_agent"

    def execute(
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
        """Execute one page of a knowledge query (``POST /execute``).

        Args:
            query: The knowledge query GID or name.
            input_params: Values for the query's input parameters.
            preprocess_params: CIQ v2 preprocess parameter values.
            page_size: Result-set page size (API default 100).
            page_token: Integer page number; values under 1 return the first page.
            user_token: Optional end-user access token to run in that user's context.
        """
        spec = RequestSpec(
            "POST",
            "/execute",
            json_body=_execute_body(query, input_params, preprocess_params, page_size, page_token),
            headers=user_token_headers(user_token),
        )
        return ExecuteResponse.model_validate(self._send(spec, timeout=timeout).json())

    def execute_iter(
        self,
        query: str,
        *,
        input_params: dict[str, Any] | None = None,
        preprocess_params: dict[str, str] | None = None,
        page_size: int = 100,
        user_token: str | None = None,
        timeout: httpx.Timeout | float | None = None,
    ) -> Iterator[ExecuteRecord]:
        """Iterate over all records of a query, fetching pages transparently.

        Stops when a page comes back with fewer than ``page_size`` records
        (the API exposes no next-page marker).
        """
        page_token = 1
        while True:
            response = self.execute(
                query,
                input_params=input_params,
                preprocess_params=preprocess_params,
                page_size=page_size,
                page_token=page_token,
                user_token=user_token,
                timeout=timeout,
            )
            yield from response.data
            if len(response.data) < page_size:
                return
            page_token += 1
