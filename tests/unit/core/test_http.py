"""Base client behavior: auth mounting, error mapping, retries, sync + async."""

from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any

import httpx
import pytest

from indykite_sdk import (
    AuthenticationError,
    Credentials,
    ETagMismatchError,
    IndyKiteConnectionError,
    NotFoundError,
    RateLimitError,
    RetryConfig,
)
from indykite_sdk._core import http as http_module
from indykite_sdk._core.http import USER_AGENT, BaseAsyncClient, BaseSyncClient
from indykite_sdk._core.ops import RequestSpec


class DemoClient(BaseSyncClient):
    """Democlient."""

    _api_prefix = "/capture/v1"
    _auth_kind = "app_agent"


class AsyncDemoClient(BaseAsyncClient):
    """Asyncdemoclient."""

    _api_prefix = "/capture/v1"
    _auth_kind = "app_agent"


def _sync_client(handler, credentials: Credentials, **kwargs: Any) -> DemoClient:
    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    return DemoClient(credentials, http_client=http_client, **kwargs)


def _next_status(statuses: Iterator[int]) -> int:
    """The next scripted status; fails the test if the client sent an unscripted extra request."""
    try:
        return next(statuses)
    except StopIteration as exc:
        raise AssertionError("client sent more requests than the test scripted statuses for") from exc


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(http_module.time, "sleep", lambda _s: None)


def test_request_building_sends_auth_base_url_and_user_agent(app_agent_credentials: Credentials) -> None:
    """Request building sends auth base url and user agent."""
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"ok": True})

    client = _sync_client(handler, app_agent_credentials)
    response = client._send(RequestSpec("POST", "/nodes", json_body={"nodes": []}))
    assert response.json() == {"ok": True}
    request = seen[0]
    assert str(request.url) == "https://eu.api.indykite.com/capture/v1/nodes"
    assert request.headers["X-IK-ClientKey"] == "app-agent-token-value"
    assert request.headers["User-Agent"] == USER_AGENT
    assert json.loads(request.content) == {"nodes": []}


def test_request_building_extra_headers_and_params(app_agent_credentials: Credentials) -> None:
    """Request building extra headers and params."""
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={})

    client = _sync_client(handler, app_agent_credentials)
    client._send(RequestSpec("GET", "/nodes", params={"a": "1"}, headers={"If-Match": "abc"}))
    assert seen[0].url.params["a"] == "1"
    assert seen[0].headers["If-Match"] == "abc"


def test_request_building_base_url_override(app_agent_credentials: Credentials) -> None:
    """Request building base url override."""
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={})

    client = _sync_client(handler, app_agent_credentials, base_url="https://api.dev.indykite.xyz")
    client._send(RequestSpec("GET", "/nodes"))
    assert str(seen[0].url) == "https://api.dev.indykite.xyz/capture/v1/nodes"


def test_error_mapping_404_raises_not_found_with_platform_body(app_agent_credentials: Credentials) -> None:
    """Error mapping 404 raises not found with platform body."""

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"message": "Not Found", "errors": ["node does not exist"]})

    client = _sync_client(handler, app_agent_credentials)
    with pytest.raises(NotFoundError) as exc_info:
        client._send(RequestSpec("GET", "/nodes"))
    error = exc_info.value
    assert error.status_code == 404
    assert error.message == "Not Found"
    assert error.errors == ["node does not exist"]
    assert "GET https://eu.api.indykite.com/capture/v1/nodes" in str(error)
    assert error.hint is not None


def test_error_mapping_401_hint_mentions_app_agent_env_var(app_agent_credentials: Credentials) -> None:
    """Error mapping 401 hint mentions app agent env var."""

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"message": "Unauthenticated"})

    client = _sync_client(handler, app_agent_credentials)
    with pytest.raises(AuthenticationError, match="INDYKITE_APPLICATION_CREDENTIALS"):
        client._send(RequestSpec("POST", "/nodes"))


def test_error_mapping_412_raises_etag_mismatch(app_agent_credentials: Credentials) -> None:
    """Error mapping 412 raises etag mismatch."""

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(412, json={"message": "Precondition Failed", "errors": ["precondition failed"]})

    client = _sync_client(handler, app_agent_credentials)
    with pytest.raises(ETagMismatchError, match="etag is stale"):
        client._send(RequestSpec("PUT", "/x", headers={"If-Match": "old"}, json_body={}))


def test_error_mapping_non_json_error_body_uses_reason_phrase(app_agent_credentials: Credentials) -> None:
    """Error mapping non json error body uses reason phrase."""

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, text="<html>gone</html>")

    client = _sync_client(handler, app_agent_credentials)
    with pytest.raises(NotFoundError, match="Not Found"):
        client._send(RequestSpec("GET", "/nodes"))


def test_error_mapping_transport_error_raises_connection_error(app_agent_credentials: Credentials) -> None:
    """Error mapping transport error raises connection error."""

    def handler(_request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("dns failure")

    client = _sync_client(handler, app_agent_credentials)
    with pytest.raises(IndyKiteConnectionError, match="eu.api.indykite.com"):
        client._send(RequestSpec("GET", "/nodes"))


def test_retries_get_retried_on_503_until_success(app_agent_credentials: Credentials) -> None:
    """Retries get retried on 503 until success."""
    statuses = iter([503, 503, 200])
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(_next_status(statuses), json={})

    client = _sync_client(handler, app_agent_credentials)
    response = client._send(RequestSpec("GET", "/nodes"))
    assert response.status_code == 200
    assert len(calls) == 3


def test_retries_post_not_retried_by_default(app_agent_credentials: Credentials) -> None:
    """Retries post not retried by default."""
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(429, json={"message": "Too Many Requests"})

    client = _sync_client(handler, app_agent_credentials)
    with pytest.raises(RateLimitError):
        client._send(RequestSpec("POST", "/nodes", json_body={}))
    assert len(calls) == 1


def test_retries_post_retried_when_opted_in(app_agent_credentials: Credentials) -> None:
    """Retries post retried when opted in."""
    statuses = iter([429, 200])
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(_next_status(statuses), json={})

    client = _sync_client(handler, app_agent_credentials, retries=RetryConfig(retry_posts=True))
    assert client._send(RequestSpec("POST", "/nodes", json_body={})).status_code == 200
    assert len(calls) == 2


def test_retries_disabled(app_agent_credentials: Credentials) -> None:
    """Retries disabled."""
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(503, json={})

    client = _sync_client(handler, app_agent_credentials, retries=None)
    with pytest.raises(Exception, match="503|Service"):
        client._send(RequestSpec("GET", "/nodes"))
    assert len(calls) == 1


def test_context_managers_sync_context_manager_closes(app_agent_credentials: Credentials) -> None:
    """Context managers sync context manager closes."""
    client = _sync_client(lambda _r: httpx.Response(200), app_agent_credentials)
    with client:
        pass
    assert client._client.is_closed


async def test_context_managers_async_send_and_close(app_agent_credentials: Credentials) -> None:
    """Context managers async send and close."""

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["X-IK-ClientKey"] == "app-agent-token-value"
        return httpx.Response(200, json={"ok": True})

    http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    async with AsyncDemoClient(app_agent_credentials, http_client=http_client) as client:
        response = await client._send(RequestSpec("POST", "/nodes", json_body={}))
        assert response.json() == {"ok": True}
    assert client._client.is_closed


async def test_context_managers_async_retry_on_503(app_agent_credentials: Credentials) -> None:
    """Context managers async retry on 503."""
    statuses = iter([503, 200])

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(_next_status(statuses), json={})

    http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    async with AsyncDemoClient(app_agent_credentials, http_client=http_client) as client:
        response = await client._send(RequestSpec("GET", "/nodes"))
        assert response.status_code == 200


def test_context_managers_wrong_http_client_type_raises(app_agent_credentials: Credentials) -> None:
    """Context managers wrong http client type raises."""
    with pytest.raises(TypeError, match="httpx.Client"):
        DemoClient(app_agent_credentials, http_client=httpx.AsyncClient())


def test_env_credentials_used_when_not_passed(monkeypatch: pytest.MonkeyPatch) -> None:
    """Env credentials used when not passed."""
    monkeypatch.setenv("INDYKITE_APPLICATION_CREDENTIALS", "app-agent-token-value")
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={})

    client = DemoClient(http_client=httpx.Client(transport=httpx.MockTransport(handler)))
    client._send(RequestSpec("GET", "/nodes"))
    assert seen[0].headers["X-IK-ClientKey"] == "app-agent-token-value"


def test_raw_token_string_accepted_by_app_agent_clients(app_agent_credentials: Credentials) -> None:
    """Raw token string accepted by app agent clients."""
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={})

    client = DemoClient("raw-token-string", http_client=httpx.Client(transport=httpx.MockTransport(handler)))
    client._send(RequestSpec("GET", "/nodes"))
    assert seen[0].headers["X-IK-ClientKey"] == "raw-token-string"
