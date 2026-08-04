"""Ingest nodes and relationships into the IKG via the Capture API.

Requires INDYKITE_APPLICATION_CREDENTIALS[_FILE].
"""

from indykite_sdk import CaptureClient


def main() -> None:
    """Run the example."""
    with CaptureClient() as client:
        results = client.upsert_nodes(
            [
                {
                    "external_id": "ada",
                    "type": "Person",
                    "is_identity": True,
                    "properties": [
                        {
                            "type": "email",
                            "value": "ada@example.com",
                            "metadata": {"assurance_level": 2, "source": "example-hr"},
                        }
                    ],
                },
                {"external_id": "kitt", "type": "Car", "properties": [{"type": "model", "value": "K.I.T.T."}]},
            ]
        )
        print(f"Upserted {len(results)} nodes")

        client.upsert_relationships(
            [
                {
                    "type": "OWNS",
                    "source": {"external_id": "ada", "type": "Person"},
                    "target": {"external_id": "kitt", "type": "Car"},
                }
            ]
        )
        print("Linked ada -[OWNS]-> kitt")


if __name__ == "__main__":
    main()
