"""Entity Matching client: run/status/mappings and completion polling."""

from __future__ import annotations

import pytest

from indykite_sdk import AsyncEntityMatchingClient, EntityMatchingClient, PipelineTimeoutError, RequestValidationError
from indykite_sdk.entity_matching import client as em_client_module
from tests.unit.conftest import sent_json

PIPELINE_ID = "gid:pipeline-1"


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(em_client_module.time, "sleep", lambda _s: None)


def test_endpoints_read_property_mappings(make_client, mock_api) -> None:
    """Endpoints read property mappings."""
    mock_api.respond(
        {
            "id": PIPELINE_ID,
            "suggested_property_mappings": [
                {
                    "source_node_type": "Person",
                    "source_node_property": "email",
                    "target_node_type": "User",
                    "target_node_property": "mail",
                    "similarity_score_cutoff": 0.92,
                }
            ],
        }
    )
    client = make_client(EntityMatchingClient)
    mappings = client.read_property_mappings(PIPELINE_ID)
    assert mock_api.last.url.path == f"/entity-matching/v1/pipelines/{PIPELINE_ID}/property-mappings"
    assert mappings.suggested_property_mappings[0].similarity_score_cutoff == 0.92


def test_endpoints_run_pipeline_body(make_client, mock_api) -> None:
    """Endpoints run pipeline body."""
    mock_api.respond({"id": PIPELINE_ID, "etag": "abc", "last_run_time": "2026-08-04T12:00:00Z"})
    client = make_client(EntityMatchingClient)
    run = client.run_pipeline(
        PIPELINE_ID,
        similarity_score_cutoff=0.9,
        custom_property_mappings=[{"source_node_property": "email", "target_node_property": "mail"}],
    )
    assert mock_api.last.url.path == f"/entity-matching/v1/pipelines/{PIPELINE_ID}/runs"
    assert sent_json(mock_api.last) == {
        "similarity_score_cutoff": 0.9,
        "custom_property_mappings": [{"source_node_property": "email", "target_node_property": "mail"}],
    }
    assert run.etag == "abc"


def test_endpoints_read_status(make_client, mock_api) -> None:
    """Endpoints read status."""
    mock_api.respond({"id": PIPELINE_ID, "property_mapping_status": "SUCCESS", "entity_matching_status": "PENDING"})
    client = make_client(EntityMatchingClient)
    status = client.read_status(PIPELINE_ID)
    assert status.entity_matching_status == "PENDING"


def test_wait_for_completion_polls_until_success(make_client, mock_api) -> None:
    """Wait for completion polls until success."""
    mock_api.respond({"entity_matching_status": "PENDING"})
    mock_api.respond({"entity_matching_status": "PENDING"})
    mock_api.respond({"entity_matching_status": "SUCCESS"})
    client = make_client(EntityMatchingClient)
    status = client.wait_for_completion(PIPELINE_ID, timeout=600, poll_interval=1)
    assert status.entity_matching_status == "SUCCESS"
    assert len(mock_api.requests) == 3


def test_wait_for_completion_times_out(make_client, mock_api) -> None:
    """Wait for completion times out."""
    client = make_client(EntityMatchingClient)  # default response has no final status
    with pytest.raises(PipelineTimeoutError, match=PIPELINE_ID):
        client.wait_for_completion(PIPELINE_ID, timeout=0.5, poll_interval=1)


async def test_async_run_and_wait(make_async_client, mock_api, monkeypatch: pytest.MonkeyPatch) -> None:
    """Async run and wait."""

    async def instant_sleep(_s: float) -> None:
        return None

    from indykite_sdk.entity_matching import aio as em_aio_module

    monkeypatch.setattr(em_aio_module.asyncio, "sleep", instant_sleep)
    mock_api.respond({"id": PIPELINE_ID})
    mock_api.respond({"entity_matching_status": "PENDING"})
    mock_api.respond({"entity_matching_status": "SUCCESS"})
    async with make_async_client(AsyncEntityMatchingClient) as client:
        await client.run_pipeline(PIPELINE_ID, similarity_score_cutoff=0.8)
        status = await client.wait_for_completion(PIPELINE_ID, timeout=600, poll_interval=1)
    assert status.entity_matching_status == "SUCCESS"


ACCEPTED = (202, {"message": "Accepted", "details": ["the property mapping process is not yet completed"]})


def test_read_property_mappings_pending_on_202(make_client, mock_api) -> None:
    """Read property mappings pending on 202."""
    mock_api.respond(ACCEPTED)
    mappings = make_client(EntityMatchingClient).read_property_mappings(PIPELINE_ID)
    assert mappings.pending is True
    assert mappings.message == "Accepted"
    assert mappings.details == ["the property mapping process is not yet completed"]
    assert mappings.suggested_property_mappings == []


async def test_async_read_property_mappings_pending_on_202(make_async_client, mock_api) -> None:
    """Async read property mappings pending on 202."""
    mock_api.respond(ACCEPTED)
    async with make_async_client(AsyncEntityMatchingClient) as client:
        assert (await client.read_property_mappings(PIPELINE_ID)).pending is True


def test_read_property_mappings_ready_is_not_pending(make_client, mock_api) -> None:
    """Read property mappings ready is not pending."""
    mock_api.respond({"id": PIPELINE_ID, "suggested_property_mappings": []})
    assert make_client(EntityMatchingClient).read_property_mappings(PIPELINE_ID).pending is False


@pytest.mark.parametrize("cutoff", [-0.1, 1.1, True, "0.5"])
def test_run_pipeline_rejects_cutoff_outside_0_to_1(make_client, mock_api, cutoff: object) -> None:
    """Run pipeline rejects cutoff outside 0 to 1."""
    with pytest.raises(RequestValidationError, match="similarity_score_cutoff"):
        make_client(EntityMatchingClient).run_pipeline(PIPELINE_ID, similarity_score_cutoff=cutoff)
    assert mock_api.requests == []


@pytest.mark.parametrize("cutoff", [0, 1])
def test_run_pipeline_accepts_cutoff_bounds(make_client, mock_api, cutoff: int) -> None:
    """Run pipeline accepts cutoff bounds."""
    make_client(EntityMatchingClient).run_pipeline(PIPELINE_ID, similarity_score_cutoff=cutoff)
    assert sent_json(mock_api.last) == {"similarity_score_cutoff": cutoff}


async def test_pipeline_id_is_encoded_as_one_path_segment(make_client, make_async_client, mock_api) -> None:
    """Pipeline id is encoded as one path segment."""
    mock_api.respond({"id": PIPELINE_ID}, {"id": PIPELINE_ID}, {"id": PIPELINE_ID})
    client = make_client(EntityMatchingClient)
    client.read_property_mappings("gid:a/b")
    client.run_pipeline("gid:a/b", similarity_score_cutoff=0.5)
    async with make_async_client(AsyncEntityMatchingClient) as async_client:
        await async_client.read_status("gid:a?b")
    assert [request.url.raw_path for request in mock_api.requests] == [
        b"/entity-matching/v1/pipelines/gid:a%2Fb/property-mappings",
        b"/entity-matching/v1/pipelines/gid:a%2Fb/runs",
        b"/entity-matching/v1/pipelines/gid:a%3Fb/status",
    ]
