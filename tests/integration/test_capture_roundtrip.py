"""Live Capture API roundtrip: upsert nodes + relationship, then delete everything."""

from __future__ import annotations

from indykite_sdk import CaptureClient


def test_capture_roundtrip(capture_client: CaptureClient, unique_suffix: str) -> None:
    """Capture roundtrip."""
    person = {"external_id": f"sdk-it-person-{unique_suffix}", "type": "Person", "is_identity": True}
    car = {"external_id": f"sdk-it-car-{unique_suffix}", "type": "Car"}
    relationship = {
        "type": "OWNS",
        "source": {"external_id": person["external_id"], "type": "Person"},
        "target": {"external_id": car["external_id"], "type": "Car"},
    }
    try:
        results = capture_client.upsert_nodes(
            [
                dict(person, properties=[{"type": "email", "value": f"{unique_suffix}@example.com"}]),
                car,
            ]
        )
        assert len(results) == 2

        capture_client.upsert_relationships([relationship])

        capture_client.delete_node_properties(
            [{"external_id": person["external_id"], "type": "Person", "property_types": ["email"]}]
        )
    finally:
        capture_client.delete_relationships([relationship])
        capture_client.delete_nodes(
            [
                {"external_id": person["external_id"], "type": "Person"},
                {"external_id": car["external_id"], "type": "Car"},
            ]
        )
