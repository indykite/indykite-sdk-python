"""Live Capture API test on a composite IKG: nodes and relationships are routed by location.

It needs a project whose IKG is a composite database, so it is opt-in:

- ``INDYKITE_TEST_COMPOSITE_LOCATIONS`` — two location names of that IKG other
  than ``global``, comma-separated, e.g. ``east,west`` (required to run)
- ``INDYKITE_TEST_COMPOSITE_APPLICATION_CREDENTIALS`` — the application-agent
  token of that project; defaults to ``INDYKITE_APPLICATION_CREDENTIALS[_FILE]``
"""

from __future__ import annotations

import os
from collections.abc import Iterator

import pytest

from indykite_sdk import CaptureClient
from indykite_sdk.capture import LOCATION_DEFAULT, LOCATION_GLOBAL, BatchResults
from tests.integration.conftest import require_env


@pytest.fixture
def composite_locations() -> tuple[str, str]:
    """The two regional locations under test, from INDYKITE_TEST_COMPOSITE_LOCATIONS."""
    locations = [name.strip() for name in require_env("INDYKITE_TEST_COMPOSITE_LOCATIONS").split(",")]
    assert len(locations) == 2, "INDYKITE_TEST_COMPOSITE_LOCATIONS must name two locations"
    east, west = locations
    assert east and west and east != west, "INDYKITE_TEST_COMPOSITE_LOCATIONS must name two different locations"
    assert not {east, west} & {LOCATION_GLOBAL, LOCATION_DEFAULT}, (
        "INDYKITE_TEST_COMPOSITE_LOCATIONS must name two regional locations"
    )
    return east, west


@pytest.fixture
def composite_capture_client() -> Iterator[CaptureClient]:
    """A CaptureClient for the project with the composite IKG."""
    token = os.environ.get("INDYKITE_TEST_COMPOSITE_APPLICATION_CREDENTIALS")
    if not token:
        require_env("INDYKITE_APPLICATION_CREDENTIALS", "INDYKITE_APPLICATION_CREDENTIALS_FILE")
    with CaptureClient(token) if token else CaptureClient() as client:
        yield client


def _assert_gids_by_location(results: BatchResults, expected_counts: dict[str, int]) -> None:
    """Every expected location holds the expected number of GIDs, and nothing else is reported."""
    assert results.results == []
    assert results.by_location is not None
    assert {location: len(gids) for location, gids in results.by_location.items()} == expected_counts
    assert all(gid.startswith("gid:") for gids in results.by_location.values() for gid in gids)


def test_capture_routes_nodes_and_relationships_by_location(
    composite_locations: tuple[str, str], composite_capture_client: CaptureClient, unique_suffix: str
) -> None:
    """Capture routes nodes and relationships by location."""
    east, west = composite_locations
    client = composite_capture_client

    def node(name: str, node_type: str, location: str | None) -> dict[str, str]:
        ref = {"external_id": f"sdk-it-cdb-{name}-{unique_suffix}", "type": node_type}
        return dict(ref, location=location) if location else ref

    east_person = node("east-person", "Person", east)
    west_person = node("west-person", "Person", west)
    west_car = node("west-car", "Car", west)
    default_car = node("default-car", "Car", None)
    global_person = node("global-person", "Person", LOCATION_GLOBAL)
    nodes = [east_person, west_person, west_car, default_car, global_person]

    # Both ends in the same location: stored in that location.
    owns = {"type": "OWNS", "source": west_person, "target": west_car}
    # Ends in different locations: stored in the global location.
    knows = {"type": "KNOWS", "source": east_person, "target": global_person}

    # Only the east person asks for a proxy, so the global location holds the
    # global person plus that one proxy.
    nodes_by_location = {east: 1, west: 2, LOCATION_DEFAULT: 1, LOCATION_GLOBAL: 2}
    relationships_by_location = {west: 1, LOCATION_GLOBAL: 1}

    deleted = False
    try:
        upserts = [dict(n, create_proxy=True) if n is east_person else n for n in nodes]
        _assert_gids_by_location(client.upsert_nodes(upserts), nodes_by_location)
        _assert_gids_by_location(client.upsert_relationships([owns, knows]), relationships_by_location)
        _assert_gids_by_location(client.delete_relationships([owns, knows]), relationships_by_location)
        _assert_gids_by_location(client.delete_nodes(nodes), nodes_by_location)
        deleted = True
    finally:
        if not deleted:
            # Always try to clean up, even on failure part-way.
            try:
                client.delete_relationships([owns, knows])
            finally:
                client.delete_nodes(nodes)
