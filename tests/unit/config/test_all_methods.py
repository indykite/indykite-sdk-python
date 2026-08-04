"""Smoke-exercise every public ConfigClient method (sync and async) against the mock API.

The detailed behavior is covered in test_config.py; this guards that each of
the ~80 mechanical resource wrappers builds a valid request and parses the
response, in both client variants.
"""

from __future__ import annotations

import inspect
from typing import Any

import pytest

from indykite_sdk import AsyncConfigClient, ConfigClient

_ARG_VALUES: dict[str, Any] = {
    "api_permissions": ["Authorization"],
    "body": {"name": "resource-name", "project_id": "gid:project-1"},
    "policy": "{}",
    "query": "{}",
    "status": "ACTIVE",
    "region": "europe-west1",
    "role": "all_editor",
    "name": "resource-name",
    "etag": "etag-1",
}


def _required_kwargs(method: Any) -> dict[str, Any]:
    kwargs: dict[str, Any] = {}
    for name, parameter in inspect.signature(method).parameters.items():
        if name == "self" or parameter.default is not inspect.Parameter.empty:
            continue
        kwargs[name] = _ARG_VALUES.get(name, "gid:some-id")
    return kwargs


def _public_methods(cls: type) -> list[str]:
    return [name for name, _member in inspect.getmembers(cls, inspect.isfunction) if not name.startswith("_")]


SYNC_METHODS = [name for name in _public_methods(ConfigClient) if name not in {"close"}]


@pytest.mark.parametrize("method_name", SYNC_METHODS)
def test_sync_method_round_trips(method_name: str, make_client, mock_api) -> None:
    """Sync method round trips."""
    client = make_client(ConfigClient)
    method = getattr(client, method_name)
    method(**_required_kwargs(method))
    assert mock_api.last.url.path.startswith("/configs/v1")


@pytest.mark.parametrize("method_name", [name for name in _public_methods(AsyncConfigClient) if name != "aclose"])
async def test_async_method_round_trips(method_name: str, make_async_client, mock_api) -> None:
    """Async method round trips."""
    async with make_async_client(AsyncConfigClient) as client:
        method = getattr(client, method_name)
        await method(**_required_kwargs(method))
    assert mock_api.last.url.path.startswith("/configs/v1")
