"""Audit Log client: query parameters, envelope parsing, cursor paging, JWKS."""

from __future__ import annotations

import pytest

from indykite_sdk import AsyncAuditClient, AuditClient, IndyKiteError, RequestValidationError
from indykite_sdk.audit import Checkpoint, KeySet, LogEntry, Manifest, Page

PROJECT = "gid:AAAAAmluZHlraURlgAABDwAAAAA"

BATCH = {
    "batch_id": "batch-1",
    "project_id": PROJECT,
    "sequence": 1,
    "data": [{"type": "indykite.audit.capture.upsert", "actor": "agent-1"}, {"type": "indykite.audit.authz"}],
    "hash": "abc",
    "signature": "c2ln",
    "kid": "platform-key-1",
    "alg": "ES256",
    "chain_hash": "head-1",
    "manifest_id": "manifest-1",
}

MANIFEST = {
    "manifest_id": "manifest-1",
    "batch_id": "batch-1",
    "batch_uri": "gs://bucket/gid.AAAA/batches/1.json",
    "project_id": PROJECT,
    "sequence": 1,
    "prev_hash": "",
    "data_hash": "abc",
    "head_hash": "head-1",
    "signature": "c2ln",
    "kid": "platform-key-1",
    "alg": "ES256",
    "created_at": "2026-09-21T12:00:00Z",
}

CHECKPOINT = {
    "checkpoint_id": "checkpoint-1",
    "project_id": PROJECT,
    "sequence": 1,
    "head_hash": "head-1",
    "created_at": "2026-09-21T13:00:00.000000001Z",
    "signature": "c2ln",
    "kid": "platform-key-1",
    "alg": "ES256",
}

JWKS = {"keys": [{"kty": "EC", "crv": "P-256", "x": "eA", "y": "eQ", "use": "sig", "kid": "platform-key-1"}]}

EMPTY_PAGE = {"next_cursor": "", "has_more": False, "items": []}


def test_list_logs_request_and_parsing(make_client, mock_api) -> None:
    """List logs request and parsing."""
    mock_api.respond({"next_cursor": "MTAx", "has_more": True, "items": [BATCH]})
    client = make_client(AuditClient)
    page = client.list_logs(PROJECT, cursor="MTAw", page_size=10)
    assert mock_api.last.method == "GET"
    assert mock_api.last.url.path == "/audit/v1/logs"
    assert dict(mock_api.last.url.params) == {"project_id": PROJECT, "cursor": "MTAw", "pagesize": "10"}
    assert mock_api.last.headers["X-IK-ClientKey"] == "app-agent-token-value"
    assert isinstance(page, Page)
    assert page.has_more is True
    assert page.next_cursor == "MTAx"
    batch = page.items[0]
    assert isinstance(batch, LogEntry)
    assert batch.sequence == 1
    assert batch.kid == "platform-key-1"
    assert batch.chain_hash == "head-1"
    assert len(batch.data) == 2
    assert batch.data[0]["actor"] == "agent-1"


def test_list_logs_first_page_sends_only_project_id(make_client, mock_api) -> None:
    """List logs first page sends only project id."""
    mock_api.respond(EMPTY_PAGE)
    client = make_client(AuditClient)
    page = client.list_logs(PROJECT)
    assert dict(mock_api.last.url.params) == {"project_id": PROJECT}
    assert page.items == []
    assert page.has_more is False


def test_list_manifests(make_client, mock_api) -> None:
    """List manifests."""
    mock_api.respond({"next_cursor": "", "has_more": False, "items": [MANIFEST]})
    client = make_client(AuditClient)
    page = client.list_manifests(PROJECT)
    assert mock_api.last.url.path == "/audit/v1/manifests"
    manifest = page.items[0]
    assert isinstance(manifest, Manifest)
    assert manifest.prev_hash == ""
    assert manifest.head_hash == "head-1"
    assert manifest.data_hash == "abc"
    assert manifest.created_at.startswith("2026-09-21")


def test_list_checkpoints(make_client, mock_api) -> None:
    """List checkpoints."""
    mock_api.respond({"next_cursor": "", "has_more": False, "items": [CHECKPOINT]})
    client = make_client(AuditClient)
    page = client.list_checkpoints(PROJECT, page_size=1)
    assert mock_api.last.url.path == "/audit/v1/checkpoints"
    assert mock_api.last.url.params["pagesize"] == "1"
    checkpoint = page.items[0]
    assert isinstance(checkpoint, Checkpoint)
    assert checkpoint.checkpoint_id == "checkpoint-1"
    assert checkpoint.head_hash == "head-1"


def test_null_wire_fields_parse(make_client, mock_api) -> None:
    """Null wire fields parse."""
    mock_api.respond({"next_cursor": None, "has_more": False, "items": [{**MANIFEST, "prev_hash": None}]})
    mock_api.respond({"next_cursor": None, "has_more": False, "items": None})
    mock_api.respond({"next_cursor": None, "has_more": False, "items": [{**BATCH, "data": None, "kid": None}]})
    mock_api.respond({"keys": None})
    client = make_client(AuditClient)
    manifests = client.list_manifests(PROJECT)
    assert manifests.next_cursor is None
    assert manifests.items[0].prev_hash is None
    assert client.list_checkpoints(PROJECT).items == []
    batch = client.list_logs(PROJECT).items[0]
    assert batch.data == []
    assert batch.kid is None
    assert client.jwks(PROJECT).keys == []


def test_iter_handles_null_next_cursor_on_last_page(make_client, mock_api) -> None:
    """Iter handles null next cursor on last page."""
    mock_api.respond({"next_cursor": "c1", "has_more": True, "items": [BATCH]})
    mock_api.respond({"next_cursor": None, "has_more": False, "items": [{**BATCH, "sequence": 2}]})
    client = make_client(AuditClient)
    assert [batch.sequence for batch in client.iter_logs(PROJECT)] == [1, 2]


def test_page_tolerates_unknown_fields(make_client, mock_api) -> None:
    """Page tolerates unknown fields."""
    mock_api.respond({"next_cursor": "", "has_more": False, "items": [{**BATCH, "new_field": 1}], "total": 1})
    client = make_client(AuditClient)
    page = client.list_logs(PROJECT)
    assert page.items[0].batch_id == "batch-1"


def test_iter_logs_follows_cursor_until_has_more_is_false(make_client, mock_api) -> None:
    """Iter logs follows cursor until has more is false."""
    mock_api.respond({"next_cursor": "c1", "has_more": True, "items": [BATCH, {**BATCH, "sequence": 2}]})
    mock_api.respond({"next_cursor": "c2", "has_more": True, "items": [{**BATCH, "sequence": 3}]})
    mock_api.respond({"next_cursor": "", "has_more": False, "items": [{**BATCH, "sequence": 4}]})
    client = make_client(AuditClient)
    batches = list(client.iter_logs(PROJECT, page_size=2))
    assert [batch.sequence for batch in batches] == [1, 2, 3, 4]
    assert [request.url.params.get("cursor") for request in mock_api.requests] == [None, "c1", "c2"]
    assert all(request.url.params["pagesize"] == "2" for request in mock_api.requests)


def test_iter_manifests_single_page(make_client, mock_api) -> None:
    """Iter manifests single page."""
    mock_api.respond({"next_cursor": "", "has_more": False, "items": [MANIFEST]})
    client = make_client(AuditClient)
    assert [manifest.manifest_id for manifest in client.iter_manifests(PROJECT)] == ["manifest-1"]
    assert len(mock_api.requests) == 1


def test_iter_checkpoints_empty_chain(make_client, mock_api) -> None:
    """Iter checkpoints empty chain."""
    mock_api.respond(EMPTY_PAGE)
    client = make_client(AuditClient)
    assert list(client.iter_checkpoints(PROJECT)) == []


def test_iter_stops_when_cursor_does_not_advance(make_client, mock_api) -> None:
    """Iter stops when cursor does not advance."""
    mock_api.respond({"next_cursor": "same", "has_more": True, "items": [BATCH]})
    mock_api.respond({"next_cursor": "same", "has_more": True, "items": [{**BATCH, "sequence": 2}]})
    client = make_client(AuditClient)
    seen: list[int] = []
    # The first page advances (None -> "same"); the second hands the same cursor back.
    with pytest.raises(IndyKiteError, match="does not advance"):
        for batch in client.iter_logs(PROJECT):
            seen.append(batch.sequence)
    assert seen == [1, 2]
    assert len(mock_api.requests) == 2


def test_iter_stops_when_has_more_without_cursor(make_client, mock_api) -> None:
    """Iter stops when has more without cursor."""
    mock_api.respond({"next_cursor": "", "has_more": True, "items": [BATCH]})
    client = make_client(AuditClient)
    with pytest.raises(IndyKiteError, match="does not advance"):
        list(client.iter_logs(PROJECT))


@pytest.mark.parametrize("project_id", ["", "   "])
def test_project_id_required(make_client, mock_api, project_id) -> None:
    """Project id required."""
    client = make_client(AuditClient)
    with pytest.raises(RequestValidationError, match="project_id"):
        client.list_logs(project_id)
    with pytest.raises(RequestValidationError, match="project_id"):
        client.jwks(project_id)
    assert mock_api.requests == []


def test_project_id_is_stripped(make_client, mock_api) -> None:
    """Project id is stripped."""
    mock_api.respond(EMPTY_PAGE)
    client = make_client(AuditClient)
    client.list_manifests(f" {PROJECT} ")
    assert mock_api.last.url.params["project_id"] == PROJECT


@pytest.mark.parametrize("page_size", [0, -5])
def test_page_size_must_be_positive(make_client, mock_api, page_size) -> None:
    """Page size must be positive."""
    client = make_client(AuditClient)
    with pytest.raises(RequestValidationError, match="page_size"):
        client.list_checkpoints(PROJECT, page_size=page_size)
    assert mock_api.requests == []


def test_jwks_request_and_find(make_client, mock_api) -> None:
    """Jwks request and find."""
    mock_api.respond(JWKS)
    client = make_client(AuditClient)
    keys = client.jwks(PROJECT)
    assert mock_api.last.method == "GET"
    assert mock_api.last.url.path == "/audit/.well-known/jwks.json"
    assert dict(mock_api.last.url.params) == {"project_id": PROJECT}
    assert isinstance(keys, KeySet)
    key = keys.find("platform-key-1")
    assert key is not None
    assert (key.kty, key.crv, key.use) == ("EC", "P-256", "sig")
    assert keys.find("rotated-out") is None


def test_jwks_empty_set(make_client, mock_api) -> None:
    """Jwks empty set."""
    mock_api.respond({})
    client = make_client(AuditClient)
    assert client.jwks(PROJECT).keys == []


def test_base_url_has_audit_prefix(make_client) -> None:
    """Base url has audit prefix."""
    client = make_client(AuditClient)
    assert client.base_url.endswith("/audit")


async def test_async_list_and_iter(make_async_client, mock_api) -> None:
    """Async list and iter."""
    mock_api.respond({"next_cursor": "c1", "has_more": True, "items": [BATCH]})
    mock_api.respond({"next_cursor": "", "has_more": False, "items": [{**BATCH, "sequence": 2}]})
    mock_api.respond({"next_cursor": "", "has_more": False, "items": [MANIFEST]})
    mock_api.respond({"next_cursor": "", "has_more": False, "items": [CHECKPOINT]})
    mock_api.respond(EMPTY_PAGE)
    mock_api.respond(EMPTY_PAGE)
    mock_api.respond(JWKS)
    async with make_async_client(AsyncAuditClient) as client:
        batches = [batch async for batch in client.iter_logs(PROJECT)]
        manifests = (await client.list_manifests(PROJECT)).items
        checkpoints = (await client.list_checkpoints(PROJECT)).items
        assert [manifest async for manifest in client.iter_manifests(PROJECT)] == []
        assert [checkpoint async for checkpoint in client.iter_checkpoints(PROJECT)] == []
        keys = await client.jwks(PROJECT)
    assert [batch.sequence for batch in batches] == [1, 2]
    assert mock_api.requests[1].url.params["cursor"] == "c1"
    assert manifests[0].head_hash == "head-1"
    assert checkpoints[0].sequence == 1
    assert keys.find("platform-key-1") is not None


async def test_async_iter_guards_against_stuck_cursor(make_async_client, mock_api) -> None:
    """Async iter guards against stuck cursor."""
    mock_api.respond({"next_cursor": "same", "has_more": True, "items": []})
    mock_api.respond({"next_cursor": "same", "has_more": True, "items": []})
    async with make_async_client(AsyncAuditClient) as client:
        with pytest.raises(IndyKiteError, match="does not advance"):
            _ = [batch async for batch in client.iter_logs(PROJECT)]


@pytest.mark.parametrize(("page_size", "valid"), [(50, True), (51, False), (0, False)])
def test_page_size_is_1_to_50(make_client, mock_api, page_size: int, valid: bool) -> None:
    """Page size is 1 to 50."""
    client = make_client(AuditClient)
    if valid:
        client.list_logs("gid:project-1", page_size=page_size)
        assert mock_api.last.url.params["pagesize"] == "50"
    else:
        with pytest.raises(RequestValidationError, match="1 to 50"):
            client.list_logs("gid:project-1", page_size=page_size)


def test_log_entry_data_object_becomes_one_event_list() -> None:
    """Log entry data object becomes one event list."""
    assert LogEntry.model_validate({"data": {"eventType": "x", "actor": "y"}}).data == [
        {"eventType": "x", "actor": "y"}
    ]
    assert LogEntry.model_validate({"data": [{"eventType": "x"}]}).data == [{"eventType": "x"}]
    assert LogEntry.model_validate({"data": None}).data == []


@pytest.mark.parametrize("page_size", [True, 1.5, "10"])
def test_page_size_must_be_an_integer(make_client, mock_api, page_size) -> None:
    """Page size must be an integer."""
    with pytest.raises(RequestValidationError, match="integer from 1 to 50"):
        make_client(AuditClient).list_logs("gid:project-1", page_size=page_size)
    assert mock_api.requests == []
