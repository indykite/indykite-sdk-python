"""Live Config API lifecycle: application -> agent -> credential, fully self-cleaning."""

from __future__ import annotations

from indykite_sdk import ConfigClient, ETagMismatchError, NotFoundError


def test_read_current_organization(config_client: ConfigClient) -> None:
    """Read current organization."""
    organization = config_client.read_current_organization()
    assert organization.id


def test_list_projects(config_client: ConfigClient, organization_id: str) -> None:
    """List projects."""
    projects = config_client.list_projects(organization_id)
    assert isinstance(projects, list)


def test_application_lifecycle(config_client: ConfigClient, project_id: str, unique_suffix: str) -> None:
    """Application lifecycle."""
    created = config_client.create_application(f"sdk-it-app-{unique_suffix}", project_id, description="SDK v2 test")
    assert created.id
    assert created.etag
    try:
        read = config_client.read_application(created.id)
        assert read.name == f"sdk-it-app-{unique_suffix}"
        assert read.etag

        updated = config_client.update_application(created.id, etag=read.etag, display_name="SDK IT App")
        assert updated.etag

        # A stale etag must be rejected with 412.
        try:
            config_client.update_application(created.id, etag=read.etag, display_name="stale write")
        except ETagMismatchError:
            pass
        else:  # pragma: no cover - depends on live behavior
            raise AssertionError("stale etag update unexpectedly succeeded")
    finally:
        current = config_client.read_application(created.id)
        config_client.delete_application(created.id, etag=current.etag)

    try:
        config_client.read_application(created.id)
    except NotFoundError:
        pass
    else:  # pragma: no cover - depends on live behavior
        raise AssertionError("application still readable after delete")


def test_agent_and_credential_bootstrap(config_client: ConfigClient, project_id: str, unique_suffix: str) -> None:
    """Agent and credential bootstrap."""
    app = config_client.create_application(f"sdk-it-agent-app-{unique_suffix}", project_id)
    try:
        agent = config_client.create_application_agent(
            f"sdk-it-agent-{unique_suffix}", app.id, api_permissions=["Authorization", "Capture", "ContXIQ"]
        )
        try:
            credential = config_client.create_application_agent_credential(agent.id)
            try:
                bootstrapped = credential.as_credentials()
                assert bootstrapped.token
                assert bootstrapped.app_agent_id
            finally:
                meta = config_client.read_application_agent_credential(credential.id)
                config_client.delete_application_agent_credential(credential.id, etag=meta.etag or credential.etag)
        finally:
            agent_read = config_client.read_application_agent(agent.id)
            config_client.delete_application_agent(agent.id, etag=agent_read.etag)
    finally:
        app_read = config_client.read_application(app.id)
        config_client.delete_application(app.id, etag=app_read.etag)
