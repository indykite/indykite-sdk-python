"""Integration test setup.

These tests hit a live IndyKite environment and are deselected by default
(``pytest -m integration`` runs them). They need:

- ``INDYKITE_APPLICATION_CREDENTIALS[_FILE]`` — the raw application-agent
  credential token
- ``INDYKITE_SERVICE_ACCOUNT_CREDENTIALS[_FILE]`` — service-account credential JSON
- ``INDYKITE_BASE_URL`` — optional, e.g. ``https://api.dev.indykite.xyz``
- ``INDYKITE_TEST_ORGANIZATION_ID`` / ``INDYKITE_TEST_PROJECT_ID`` — existing IDs
- ``INDYKITE_TEST_KNOWLEDGE_QUERY_ID`` — an ACTIVE knowledge query (CIQ test)
- ``INDYKITE_TEST_ENTITY_MATCHING_PIPELINE_ID`` — an entity-matching pipeline

Tests skip themselves when their prerequisites are missing, so a partial
environment still runs what it can.
"""

from __future__ import annotations

import os
import uuid
from collections.abc import Iterator

import pytest

from indykite_sdk import AuthZENClient, CaptureClient, CIQClient, ConfigClient, DataSchemaClient, EntityMatchingClient

_INTEGRATION_DIR = os.path.dirname(__file__)


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Mark every test in this directory with the ``integration`` marker.

    This hook sees the whole session's items; only mark the ones in this directory.
    """
    for item in items:
        if str(item.path).startswith(_INTEGRATION_DIR):
            item.add_marker(pytest.mark.integration)


def require_env(name: str, alternative: str | None = None) -> str:
    """Return the value of ``name`` (or ``alternative``), skipping the test when neither is set."""
    value = os.environ.get(name) or (os.environ.get(alternative) if alternative else None)
    if not value:
        pytest.skip(f"{name} is not set")
    return value


@pytest.fixture(scope="session")
def unique_suffix() -> str:
    """Unique per-run suffix so created resources never collide."""
    return uuid.uuid4().hex[:10]


@pytest.fixture(scope="session")
def organization_id() -> str:
    """The organization ID under test, from INDYKITE_TEST_ORGANIZATION_ID."""
    return require_env("INDYKITE_TEST_ORGANIZATION_ID")


@pytest.fixture(scope="session")
def project_id() -> str:
    """The project ID under test, from INDYKITE_TEST_PROJECT_ID."""
    return require_env("INDYKITE_TEST_PROJECT_ID")


@pytest.fixture
def config_client() -> Iterator[ConfigClient]:
    """A ConfigClient authenticated from the environment."""
    require_env("INDYKITE_SERVICE_ACCOUNT_CREDENTIALS", "INDYKITE_SERVICE_ACCOUNT_CREDENTIALS_FILE")
    with ConfigClient() as client:
        yield client


@pytest.fixture
def capture_client() -> Iterator[CaptureClient]:
    """A CaptureClient authenticated from the environment."""
    require_env("INDYKITE_APPLICATION_CREDENTIALS", "INDYKITE_APPLICATION_CREDENTIALS_FILE")
    with CaptureClient() as client:
        yield client


@pytest.fixture
def authzen_client() -> Iterator[AuthZENClient]:
    """An AuthZENClient authenticated from the environment."""
    require_env("INDYKITE_APPLICATION_CREDENTIALS", "INDYKITE_APPLICATION_CREDENTIALS_FILE")
    with AuthZENClient() as client:
        yield client


@pytest.fixture
def ciq_client() -> Iterator[CIQClient]:
    """A CIQClient authenticated from the environment."""
    require_env("INDYKITE_APPLICATION_CREDENTIALS", "INDYKITE_APPLICATION_CREDENTIALS_FILE")
    with CIQClient() as client:
        yield client


@pytest.fixture
def data_schema_client() -> Iterator[DataSchemaClient]:
    """A DataSchemaClient authenticated from the environment."""
    require_env("INDYKITE_APPLICATION_CREDENTIALS", "INDYKITE_APPLICATION_CREDENTIALS_FILE")
    with DataSchemaClient() as client:
        yield client


@pytest.fixture
def entity_matching_client() -> Iterator[EntityMatchingClient]:
    """An EntityMatchingClient authenticated from the environment."""
    require_env("INDYKITE_APPLICATION_CREDENTIALS", "INDYKITE_APPLICATION_CREDENTIALS_FILE")
    with EntityMatchingClient() as client:
        yield client
