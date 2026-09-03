"""Live Config API lifecycle: application -> agent -> credential and audit signing, fully self-cleaning."""

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


def test_audit_signing_lifecycle(config_client: ConfigClient, project_id: str, unique_suffix: str) -> None:
    """Audit signing lifecycle: platform-managed create, read, customer-managed update, list, delete."""
    name = f"sdk-it-audit-signing-{unique_suffix}"
    created = config_client.create_audit_signing(name, project_id, description="SDK v2 test")
    assert created.id
    assert created.etag
    try:
        platform_managed = config_client.read_audit_signing(created.id)
        assert platform_managed.name == name
        assert platform_managed.provider == "PLATFORM_MANAGED"
        assert platform_managed.etag

        # Consumed by the update below, so it is the stale etag the 412 check needs.
        stale_etag = platform_managed.etag

        updated = config_client.update_audit_signing(
            created.id,
            etag=stale_etag,
            provider="CUSTOMER_AWS_KMS",
            key_resource="arn:aws:kms:eu-west-1:123456789012:key/sdk-it",
            kid=f"sdk-it-{unique_suffix}",
            auth_params={"access_key_id": "sdk-it-key", "secret_access_key": "sdk-it-secret"},
        )
        assert updated.etag
        assert updated.etag != stale_etag

        # auth_params come back with their keys only - values are never readable.
        customer_managed = config_client.read_audit_signing(created.id)
        assert customer_managed.provider == "CUSTOMER_AWS_KMS"
        assert customer_managed.kid == f"sdk-it-{unique_suffix}"
        assert customer_managed.auth_params == {"access_key_id": "", "secret_access_key": ""}

        listed = config_client.list_audit_signings(project_id, full_fetch=True, search=name)
        assert any(item.id == created.id and item.provider == "CUSTOMER_AWS_KMS" for item in listed)

        # The etag the update already consumed must now be rejected with 412.
        try:
            config_client.update_audit_signing(created.id, etag=stale_etag, provider="PLATFORM_MANAGED")
        except ETagMismatchError:
            pass
        else:  # pragma: no cover - depends on live behavior
            raise AssertionError("stale etag update unexpectedly succeeded")
    finally:
        current = config_client.read_audit_signing(created.id)
        config_client.delete_audit_signing(created.id, etag=current.etag)

    try:
        config_client.read_audit_signing(created.id)
    except NotFoundError:
        pass
    else:  # pragma: no cover - depends on live behavior
        raise AssertionError("audit signing still readable after delete")
