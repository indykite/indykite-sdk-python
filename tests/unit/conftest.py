"""Helpers for unit-testing clients against an httpx MockTransport."""

from __future__ import annotations

from collections.abc import Callable

import httpx
import pytest

from indykite_sdk import Credentials

Handler = Callable[[httpx.Request], httpx.Response]


class MockAPI:
    """Records requests and serves canned responses for a client under test."""

    def __init__(self) -> None:
        self.requests: list[httpx.Request] = []
        self._responses: list[httpx.Response] = []
        self._default = httpx.Response(200, json={})

    def respond(self, *responses: httpx.Response | dict | list | tuple[int, dict]) -> None:
        """Queue responses; a dict/list means 200 with that JSON body."""
        for response in responses:
            if isinstance(response, (dict, list)):
                response = httpx.Response(200, json=response)
            elif isinstance(response, tuple):
                status, body = response
                response = httpx.Response(status, json=body)
            self._responses.append(response)

    def handler(self, request: httpx.Request) -> httpx.Response:
        """Record the request and serve the next canned response."""
        self.requests.append(request)
        return self._responses.pop(0) if self._responses else self._default

    @property
    def last(self) -> httpx.Request:
        """The most recently recorded request."""
        return self.requests[-1]


@pytest.fixture
def mock_api() -> MockAPI:
    """Mock api."""
    return MockAPI()


@pytest.fixture
def make_client(mock_api: MockAPI, app_agent_credentials: Credentials, service_account_credentials: Credentials):
    """Build any sync SDK client wired to the mock transport."""

    def factory(client_cls, **kwargs):
        credentials = (
            service_account_credentials if client_cls._auth_kind == "service_account" else app_agent_credentials
        )
        http_client = httpx.Client(transport=httpx.MockTransport(mock_api.handler))
        return client_cls(credentials, http_client=http_client, **kwargs)

    return factory


@pytest.fixture
def make_async_client(mock_api: MockAPI, app_agent_credentials: Credentials, service_account_credentials: Credentials):
    """Build any async SDK client wired to the mock transport."""

    def factory(client_cls, **kwargs):
        credentials = (
            service_account_credentials if client_cls._auth_kind == "service_account" else app_agent_credentials
        )
        http_client = httpx.AsyncClient(transport=httpx.MockTransport(mock_api.handler))
        return client_cls(credentials, http_client=http_client, **kwargs)

    return factory


def sent_json(request: httpx.Request):
    """Decode the JSON body a request sent."""
    import json

    return json.loads(request.content)
