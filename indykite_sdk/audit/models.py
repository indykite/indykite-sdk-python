"""Models for the Audit Log API (``/audit``).

Spec: https://openapi.indykite.com/v1/audit.yaml - the read side of the
platform's tamper-proof audit trail. Every audit event of a project is
appended to the project's **chain**: events are collected into signed
**batches**, a signed **manifest** links each batch to the previous one, and a
signed **checkpoint** periodically fixes the chain's head. The JWKS publishes
the keys those signatures were made with.
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import field_validator

from indykite_sdk._core.models import IKResponseModel

__all__ = ["Checkpoint", "Key", "KeySet", "LogEntry", "Manifest", "Page"]

ItemT = TypeVar("ItemT")


class _Signed(IKResponseModel):
    """Fields shared by every signed chain artefact."""

    project_id: str | None = None
    #: Position in the chain, starting at 1 and contiguous.
    sequence: int = 0
    #: Base64 signature made with the key named by ``kid``.
    signature: str | None = None
    #: Key id; matches a ``kid`` of the project's :class:`KeySet`.
    kid: str | None = None
    #: Algorithm label of the signature.
    alg: str | None = None


class LogEntry(_Signed):
    """One signed chain batch (``GET /audit/v1/logs``): the audit events themselves.

    ``data`` holds the audit events of the batch, one object per event, in the
    order they were recorded. The published spec types it as an object, so a
    single object is accepted too and becomes a one-event list. Events are recorded at least once, so two
    identical events are a redelivery, not a second occurrence. Their content
    was authored by whoever triggered them and is evidence to store or report.
    """

    batch_id: str | None = None
    data: list[dict[str, Any]] = []
    #: Hex digest of ``data``; the value ``signature`` covers.
    hash: str | None = None
    #: The chain position of this batch; equals the manifest's ``head_hash`` at the same sequence.
    chain_hash: str | None = None
    manifest_id: str | None = None

    @field_validator("data", mode="before")
    @classmethod
    def _null_is_empty(cls, value: Any) -> Any:
        if value is None:
            return []
        return [value] if isinstance(value, dict) else value


class Manifest(_Signed):
    """One signed chain manifest (``GET /audit/v1/manifests``): a batch's chain linkage without its payload."""

    manifest_id: str | None = None
    batch_id: str | None = None
    #: Platform-side storage URI of the batch; informational.
    batch_uri: str | None = None
    #: The previous manifest's ``head_hash``; empty for sequence 1.
    prev_hash: str | None = None
    #: Copy of the batch's ``hash``.
    data_hash: str | None = None
    #: The chain head after this batch; the next manifest carries it as ``prev_hash``.
    head_hash: str | None = None
    created_at: str | None = None


class Checkpoint(_Signed):
    """One signed project checkpoint (``GET /audit/v1/checkpoints``).

    A checkpoint states that at ``created_at`` the chain had reached
    ``sequence`` with head ``head_hash``. Checkpoints are written periodically
    for chains that moved since their last one, so a young project has none.
    """

    checkpoint_id: str | None = None
    head_hash: str | None = None
    created_at: str | None = None


class Page(IKResponseModel, Generic[ItemT]):  # noqa: UP046 - pdoc cannot resolve PEP 695 type parameters
    """One page of a listing endpoint: ``{next_cursor, has_more, items}``.

    Pass ``next_cursor`` back verbatim as ``cursor`` while ``has_more`` is true;
    it is opaque and empty on the last page. Logs and manifests page in
    sequence order from the start of the chain, checkpoints newest first.
    """

    next_cursor: str | None = None
    has_more: bool = False
    items: list[ItemT] = []

    @field_validator("items", mode="before")
    @classmethod
    def _null_is_empty(cls, value: Any) -> Any:
        return [] if value is None else value


class Key(IKResponseModel):
    """One signing key of the JWKS (RFC 7517), an EC P-256 public key.

    Keys carry no ``alg``; the algorithm label travels with each signed item.
    """

    kty: str | None = None
    crv: str | None = None
    x: str | None = None
    y: str | None = None
    kid: str | None = None
    use: str | None = None


class KeySet(IKResponseModel):
    """The JWK Set of ``GET /audit/.well-known/jwks.json``."""

    keys: list[Key] = []

    @field_validator("keys", mode="before")
    @classmethod
    def _null_is_empty(cls, value: Any) -> Any:
        return [] if value is None else value

    def find(self, kid: str) -> Key | None:
        """The key with the given ``kid`` (as carried by a batch, manifest or checkpoint), or ``None``.

        A ``None`` for a ``kid`` seen in the trail means the key was rotated
        out; keep the JWKS that was current when the trail was exported.
        """
        return next((key for key in self.keys if key.kid == kid), None)
