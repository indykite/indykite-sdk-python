"""Export a project's tamper-proof audit trail via the Audit Log API.

Requires INDYKITE_APPLICATION_CREDENTIALS[_FILE] for an application agent that
holds the ``Audit`` API permission, and INDYKITE_TEST_PROJECT_ID set to the
project that agent belongs to. Writes logs.json, manifests.json,
checkpoints.json and jwks.json to the current directory, which together form
a self-describing export: the manifests link the batches through
prev_hash / head_hash, the checkpoints fix the chain head at known times, and
the JWKS names the keys every signature was made with.
"""

import json
import os

from indykite_sdk import AuditClient


def main() -> None:
    """Run the example."""
    project_id = os.environ["INDYKITE_TEST_PROJECT_ID"]

    with AuditClient() as client:
        # The public signing keys - fetch them first and keep them with the export.
        keys = client.jwks(project_id)
        print(f"Signing keys: {[key.kid for key in keys.keys]}")

        # Manifests are small: the chain linkage without the event payloads.
        manifests = list(client.iter_manifests(project_id))
        print(f"Chain length: {len(manifests)} batches")
        for manifest in manifests[-3:]:
            prev_hash, head_hash = (manifest.prev_hash or "")[:12], (manifest.head_hash or "")[:12]
            print(f"  #{manifest.sequence} {prev_hash}.. -> {head_hash}.. kid={manifest.kid}")

        # Logs page in lockstep with manifests; each batch carries its audit events in `data`.
        logs = list(client.iter_logs(project_id, page_size=20))
        events = [event for batch in logs for event in batch.data]
        print(f"Audit events: {len(events)}")

        # Checkpoints come newest first; a young project may have none yet.
        checkpoints = list(client.iter_checkpoints(project_id))
        if checkpoints:
            newest = checkpoints[0]
            print(f"Newest checkpoint: sequence {newest.sequence} at {newest.created_at}")

    for name, items in (
        ("jwks.json", keys),
        ("manifests.json", manifests),
        ("logs.json", logs),
        ("checkpoints.json", checkpoints),
    ):
        with open(name, "w", encoding="utf-8") as handle:
            payload = items.model_dump() if hasattr(items, "model_dump") else [item.model_dump() for item in items]
            json.dump(payload, handle, indent=2)
        print(f"Wrote {name}")


if __name__ == "__main__":
    main()
