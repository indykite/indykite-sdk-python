"""Drift guard: every sync client and its async twin expose the same public API."""

from __future__ import annotations

import inspect

import pytest

import indykite_sdk

CLIENT_PAIRS = [
    (indykite_sdk.CaptureClient, indykite_sdk.AsyncCaptureClient),
    (indykite_sdk.AuthZENClient, indykite_sdk.AsyncAuthZENClient),
    (indykite_sdk.CIQClient, indykite_sdk.AsyncCIQClient),
    (indykite_sdk.DataSchemaClient, indykite_sdk.AsyncDataSchemaClient),
    (indykite_sdk.EntityMatchingClient, indykite_sdk.AsyncEntityMatchingClient),
    (indykite_sdk.ConfigClient, indykite_sdk.AsyncConfigClient),
]

_LIFECYCLE = {"close", "aclose"}


def _public_methods(cls: type) -> dict[str, inspect.Signature]:
    return {
        name: inspect.signature(member)
        for name, member in inspect.getmembers(cls, inspect.isfunction)
        if not name.startswith("_") and name not in _LIFECYCLE
    }


@pytest.mark.parametrize(("sync_cls", "async_cls"), CLIENT_PAIRS, ids=lambda cls: cls.__name__)
def test_sync_and_async_clients_match(sync_cls: type, async_cls: type) -> None:
    """Sync and async clients match."""
    sync_methods = _public_methods(sync_cls)
    async_methods = _public_methods(async_cls)
    assert sync_methods.keys() == async_methods.keys(), (
        f"{sync_cls.__name__} and {async_cls.__name__} expose different methods"
    )
    for name, sync_signature in sync_methods.items():
        # Return annotations legitimately differ (Iterator vs AsyncIterator); parameters must not.
        assert sync_signature.parameters == async_methods[name].parameters, f"Signature drift on {name}"


def test_all_exports_resolve() -> None:
    """All exports resolve."""
    for name in indykite_sdk.__all__:
        assert getattr(indykite_sdk, name) is not None
