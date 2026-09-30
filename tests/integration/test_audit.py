"""Live Audit Log API smoke tests.

The agent must hold the ``Audit`` API permission. The chain of the test project
may be empty, so the tests assert the envelope and the cross-endpoint
invariants that hold for any chain length, not a particular content.
"""

from __future__ import annotations

from indykite_sdk import AuditClient
from indykite_sdk.audit import Checkpoint, LogEntry, Manifest


def test_jwks_returns_signature_keys(audit_client: AuditClient, project_id: str) -> None:
    """Jwks returns signature keys."""
    keys = audit_client.jwks(project_id)
    assert keys.keys, "the platform publishes at least one signing key"
    for key in keys.keys:
        assert key.kty == "EC"
        assert key.kid


def test_logs_and_manifests_page_in_lockstep(audit_client: AuditClient, project_id: str) -> None:
    """Logs and manifests page in lockstep."""
    logs = audit_client.list_logs(project_id, page_size=5)
    manifests = audit_client.list_manifests(project_id, page_size=5)
    assert isinstance(logs.has_more, bool)
    # The chain may grow between the two calls, so compare only the sequences both pages cover.
    manifests_by_sequence = {manifest.sequence: manifest for manifest in manifests.items}
    for batch in logs.items:
        assert isinstance(batch, LogEntry)
        assert isinstance(batch.data, list)
        manifest = manifests_by_sequence.get(batch.sequence)
        if manifest is None:
            continue
        assert isinstance(manifest, Manifest)
        assert batch.batch_id == manifest.batch_id
        assert batch.hash == manifest.data_hash
        assert batch.chain_hash == manifest.head_hash


def test_manifests_chain_is_linked(audit_client: AuditClient, project_id: str) -> None:
    """Manifests chain is linked."""
    manifests = list(audit_client.iter_manifests(project_id, page_size=50))
    previous_head = ""
    for expected_sequence, manifest in enumerate(manifests, start=1):
        assert manifest.sequence == expected_sequence
        assert (manifest.prev_hash or "") == previous_head
        assert manifest.signature and manifest.kid
        previous_head = manifest.head_hash or ""


def test_checkpoints_are_newest_first_and_within_the_chain(audit_client: AuditClient, project_id: str) -> None:
    """Checkpoints are newest first and within the chain."""
    checkpoints = list(audit_client.iter_checkpoints(project_id, page_size=10))
    chain_length = sum(1 for _ in audit_client.iter_manifests(project_id))
    sequences = [checkpoint.sequence for checkpoint in checkpoints]
    assert sequences == sorted(sequences, reverse=True)
    for checkpoint in checkpoints:
        assert isinstance(checkpoint, Checkpoint)
        assert 1 <= checkpoint.sequence <= chain_length
        assert checkpoint.head_hash and checkpoint.signature and checkpoint.created_at
