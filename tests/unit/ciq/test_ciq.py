"""CIQ client: execute payloads, pagination iterator, user tokens."""

from __future__ import annotations

import pytest

from indykite_sdk import AsyncCIQClient, CIQClient, RequestValidationError
from tests.unit.conftest import sent_json

RECORD = {"nodes": {"car.external_id": "kitt", "car.property.model": "K.I.T.T."}, "relationships": {}}


def test_execute_minimal_body(make_client, mock_api) -> None:
    """Execute minimal body."""
    mock_api.respond({"data": [RECORD]})
    client = make_client(CIQClient)
    result = client.execute("gid:query-1")
    assert mock_api.last.url.path == "/contx-iq/v1/execute"
    assert sent_json(mock_api.last) == {"id": "gid:query-1"}
    assert result.data[0].nodes["car.external_id"] == "kitt"


def test_execute_full_body(make_client, mock_api) -> None:
    """Execute full body."""
    client = make_client(CIQClient)
    client.execute(
        "gid:query-1",
        input_params={"personId": "ada"},
        preprocess_params={"model": "gpt"},
        page_size=50,
        page_token=2,
        user_token="user-jwt",
    )
    assert sent_json(mock_api.last) == {
        "id": "gid:query-1",
        "input_params": {"personId": "ada"},
        "preprocess_params": {"model": "gpt"},
        "page_size": 50,
        "page_token": 2,
    }
    assert mock_api.last.headers["Authorization"] == "Bearer user-jwt"


def test_execute_empty_result(make_client, mock_api) -> None:
    """Execute empty result."""
    mock_api.respond({})
    client = make_client(CIQClient)
    assert client.execute("gid:query-1").data == []


def test_execute_iter_stops_on_short_page(make_client, mock_api) -> None:
    """Execute iter stops on short page."""
    mock_api.respond({"data": [RECORD, RECORD]})
    mock_api.respond({"data": [RECORD]})
    client = make_client(CIQClient)
    records = list(client.execute_iter("gid:query-1", page_size=2))
    assert len(records) == 3
    assert [sent_json(r)["page_token"] for r in mock_api.requests] == [1, 2]


def test_execute_iter_exact_multiple_fetches_trailing_empty_page(make_client, mock_api) -> None:
    """Execute iter exact multiple fetches trailing empty page."""
    mock_api.respond({"data": [RECORD, RECORD]})
    mock_api.respond({"data": []})
    client = make_client(CIQClient)
    records = list(client.execute_iter("gid:query-1", page_size=2))
    assert len(records) == 2
    assert len(mock_api.requests) == 2


def test_execute_iter_single_short_page(make_client, mock_api) -> None:
    """Execute iter single short page."""
    mock_api.respond({"data": [RECORD]})
    client = make_client(CIQClient)
    assert len(list(client.execute_iter("gid:query-1"))) == 1
    assert len(mock_api.requests) == 1


def test_whoami_sends_user_token(make_client, mock_api) -> None:
    """Whoami sends user token."""
    mock_api.respond({"type": "Person", "id": "knightrider"})
    client = make_client(CIQClient)
    result = client.whoami("user-jwt")
    assert mock_api.last.method == "GET"
    assert mock_api.last.url.path == "/contx-iq/v1/whoami"
    assert mock_api.last.headers["Authorization"] == "Bearer user-jwt"
    assert mock_api.last.headers["X-IK-ClientKey"] == "app-agent-token-value"
    assert result.type == "Person"
    assert result.id == "knightrider"


@pytest.mark.parametrize("user_token", ["", "   "])
def test_whoami_requires_user_token(make_client, mock_api, user_token) -> None:
    """Whoami requires user token."""
    client = make_client(CIQClient)
    with pytest.raises(RequestValidationError, match="user_token"):
        client.whoami(user_token)
    assert mock_api.requests == []


def test_whoami_strips_user_token(make_client, mock_api) -> None:
    """Whoami strips user token."""
    mock_api.respond({"type": "Person", "id": "knightrider"})
    client = make_client(CIQClient)
    client.whoami(" user-jwt ")
    assert mock_api.last.headers["Authorization"] == "Bearer user-jwt"


async def test_async_ciq_whoami(make_async_client, mock_api) -> None:
    """Async ciq whoami."""
    mock_api.respond({"type": "Person", "id": "knightrider"})
    async with make_async_client(AsyncCIQClient) as client:
        result = await client.whoami("user-jwt")
    assert mock_api.last.url.path == "/contx-iq/v1/whoami"
    assert result.id == "knightrider"


async def test_async_ciq_execute(make_async_client, mock_api) -> None:
    """Async ciq execute."""
    mock_api.respond({"data": [RECORD]})
    async with make_async_client(AsyncCIQClient) as client:
        result = await client.execute("gid:query-1")
    assert len(result.data) == 1


async def test_async_ciq_execute_iter(make_async_client, mock_api) -> None:
    """Async ciq execute iter."""
    mock_api.respond({"data": [RECORD, RECORD]})
    mock_api.respond({"data": []})
    async with make_async_client(AsyncCIQClient) as client:
        records = [record async for record in client.execute_iter("gid:query-1", page_size=2)]
    assert len(records) == 2
