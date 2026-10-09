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


def test_execute_sends_delegated_token_header(make_client, mock_api) -> None:
    """Execute sends delegated token header."""
    client = make_client(CIQClient)
    client.execute("gid:query-1", user_token="user-jwt", delegated_token="ik-jwt")
    assert mock_api.last.headers["Authorization"] == "Bearer user-jwt"
    assert mock_api.last.headers["X-IK-Token"] == "ik-jwt"
    assert mock_api.last.headers["X-IK-ClientKey"] == "app-agent-token-value"
    # The tokens travel as headers only; the body never carries them.
    assert sent_json(mock_api.last) == {"id": "gid:query-1"}


def test_execute_without_tokens_sends_no_token_headers(make_client, mock_api) -> None:
    """Execute without tokens sends no token headers."""
    client = make_client(CIQClient)
    client.execute("gid:query-1", delegated_token="")
    assert "Authorization" not in mock_api.last.headers
    assert "X-IK-Token" not in mock_api.last.headers


def test_execute_iter_forwards_delegated_token(make_client, mock_api) -> None:
    """Execute iter forwards delegated token."""
    mock_api.respond({"data": [RECORD, RECORD]})
    mock_api.respond({"data": []})
    client = make_client(CIQClient)
    list(client.execute_iter("gid:query-1", page_size=2, user_token="u", delegated_token="ik-jwt"))
    assert all(request.headers["X-IK-Token"] == "ik-jwt" for request in mock_api.requests)


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
        records = [
            record
            async for record in client.execute_iter("gid:query-1", page_size=2, user_token="u", delegated_token="ik")
        ]
    assert len(records) == 2
    assert all(request.headers["X-IK-Token"] == "ik" for request in mock_api.requests)


@pytest.mark.parametrize("value", ["", "v" * 257])
def test_execute_rejects_input_param_strings_outside_1_to_256(make_client, mock_api, value: str) -> None:
    """Execute rejects input param strings outside 1 to 256."""
    with pytest.raises(RequestValidationError, match="input_params"):
        make_client(CIQClient).execute("gid:kq-1", input_params={"name": value})
    assert mock_api.requests == []


def test_execute_accepts_non_string_input_params(make_client, mock_api) -> None:
    """Execute accepts non string input params."""
    make_client(CIQClient).execute("gid:kq-1", input_params={"limit": 5, "name": "v" * 256})
    assert sent_json(mock_api.last)["input_params"] == {"limit": 5, "name": "v" * 256}


def test_whoami_fields_are_optional(make_client, mock_api) -> None:
    """Whoami fields are optional."""
    mock_api.respond({})
    result = make_client(CIQClient).whoami("user-jwt")
    assert result.type is None
    assert result.id is None


@pytest.mark.parametrize("page_size", [0, -1])
async def test_execute_iter_rejects_page_size_below_1(make_client, make_async_client, mock_api, page_size: int) -> None:
    """Execute iter rejects page size below 1."""
    with pytest.raises(RequestValidationError, match="page_size"):
        list(make_client(CIQClient).execute_iter("gid:kq-1", page_size=page_size))
    async with make_async_client(AsyncCIQClient) as client:
        with pytest.raises(RequestValidationError, match="page_size"):
            [record async for record in client.execute_iter("gid:kq-1", page_size=page_size)]
    assert mock_api.requests == []


def test_null_collections_in_response_are_empty(make_client, mock_api) -> None:
    """Null collections in response are empty."""
    mock_api.respond({"data": [{"nodes": None, "relationships": None}]}, {"data": None})
    client = make_client(CIQClient)
    record = client.execute("gid:kq-1").data[0]
    assert (record.nodes, record.relationships) == ({}, {})
    assert client.execute("gid:kq-1").data == []
