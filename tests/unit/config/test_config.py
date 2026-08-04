"""Config client: CRUD shapes, ETag handling, credential bootstrap, dict resources."""

from __future__ import annotations

import httpx
import pytest

from indykite_sdk import (
    AsyncConfigClient,
    ConfigClient,
    CredentialsError,
    ETagMismatchError,
    RequestValidationError,
)
from tests.unit.conftest import sent_json

PROJECT = {
    "id": "gid:project-1",
    "name": "my-project",
    "organization_id": "gid:org-1",
    "region": "europe-west1",
    "ikg_size": "2GB",
}


def test_organization_read_current(make_client, mock_api) -> None:
    """Organization read current."""
    mock_api.respond({"id": "gid:org-1", "name": "acme"})
    client = make_client(ConfigClient)
    org = client.read_current_organization()
    assert mock_api.last.method == "GET"
    assert mock_api.last.url.path == "/configs/v1/organizations/current"
    assert mock_api.last.headers["Authorization"] == "Bearer service-account-token-value"
    assert org.id == "gid:org-1"


def test_project_crud_list_params(make_client, mock_api) -> None:
    """Project crud list params."""
    mock_api.respond({"data": [PROJECT]})
    client = make_client(ConfigClient)
    projects = client.list_projects("gid:org-1", search="my")
    assert mock_api.last.url.path == "/configs/v1/projects"
    assert dict(mock_api.last.url.params) == {"organization_id": "gid:org-1", "search": "my"}
    assert projects[0].region == "europe-west1"


def test_project_crud_create_drops_none_and_captures_etag(make_client, mock_api) -> None:
    """Project crud create drops none and captures etag."""
    mock_api.respond(httpx.Response(201, json={"id": "gid:project-1"}, headers={"ETag": "etag-1"}))
    client = make_client(ConfigClient)
    created = client.create_project("my-project", "gid:org-1", "europe-west1", description="demo")
    assert sent_json(mock_api.last) == {
        "name": "my-project",
        "organization_id": "gid:org-1",
        "region": "europe-west1",
        "description": "demo",
    }
    assert created.id == "gid:project-1"
    assert created.etag == "etag-1"


def test_project_crud_read_captures_etag(make_client, mock_api) -> None:
    """Project crud read captures etag."""
    mock_api.respond(httpx.Response(200, json=PROJECT, headers={"ETag": "etag-2"}))
    client = make_client(ConfigClient)
    project = client.read_project("gid:project-1")
    assert mock_api.last.url.path == "/configs/v1/projects/gid:project-1"
    assert project.etag == "etag-2"


def test_project_crud_update_sends_if_match(make_client, mock_api) -> None:
    """Project crud update sends if match."""
    mock_api.respond(httpx.Response(200, json={"id": "gid:project-1"}, headers={"ETag": "etag-3"}))
    client = make_client(ConfigClient)
    updated = client.update_project("gid:project-1", etag="etag-2", display_name="My Project")
    assert mock_api.last.method == "PUT"
    assert mock_api.last.headers["If-Match"] == "etag-2"
    assert sent_json(mock_api.last) == {"display_name": "My Project"}
    assert updated.etag == "etag-3"


def test_project_crud_delete_sends_if_match(make_client, mock_api) -> None:
    """Project crud delete sends if match."""
    client = make_client(ConfigClient)
    client.delete_project("gid:project-1", etag="etag-2")
    assert mock_api.last.method == "DELETE"
    assert mock_api.last.headers["If-Match"] == "etag-2"


def test_project_crud_update_without_etag_is_client_side_error(make_client, mock_api) -> None:
    """Project crud update without etag is client side error."""
    client = make_client(ConfigClient)
    with pytest.raises(RequestValidationError, match="etag"):
        client.update_project("gid:project-1", etag="", display_name="x")
    assert mock_api.requests == []


def test_project_crud_stale_etag_maps_to_etag_mismatch(make_client, mock_api) -> None:
    """Project crud stale etag maps to etag mismatch."""
    mock_api.respond((412, {"message": "Precondition Failed", "errors": ["update failed: precondition failed"]}))
    client = make_client(ConfigClient)
    with pytest.raises(ETagMismatchError) as exc_info:
        client.update_project("gid:project-1", etag="stale", display_name="x")
    assert exc_info.value.errors == ["update failed: precondition failed"]


def test_application_agents_create_body(make_client, mock_api) -> None:
    """Application agents create body."""
    client = make_client(ConfigClient)
    client.create_application_agent("my-agent", "gid:app-1", ["Authorization", "Capture"])
    assert mock_api.last.url.path == "/configs/v1/application-agents"
    assert sent_json(mock_api.last) == {
        "name": "my-agent",
        "application_id": "gid:app-1",
        "api_permissions": ["Authorization", "Capture"],
    }


def test_application_agents_update_permissions(make_client, mock_api) -> None:
    """Application agents update permissions."""
    client = make_client(ConfigClient)
    client.update_application_agent("gid:agent-1", etag="e", api_permissions=["ContXIQ"])
    assert sent_json(mock_api.last) == {"api_permissions": ["ContXIQ"]}


def test_credentials_create_app_agent_credential_bootstrap(make_client, mock_api) -> None:
    """Credentials create app agent credential bootstrap."""
    mock_api.respond(
        httpx.Response(
            201,
            json={
                "id": "gid:cred-1",
                "kid": "kid-1",
                "application_agent_id": "gid:agent-1",
                "application_agent_config": {
                    "appAgentId": "gid:agent-1",
                    "appSpaceId": "gid:project-1",
                    "token": "fresh-agent-token",
                },
            },
            headers={"ETag": "etag-1"},
        )
    )
    client = make_client(ConfigClient)
    created = client.create_application_agent_credential("gid:agent-1", expire_time="2027-01-01T00:00:00Z")
    assert sent_json(mock_api.last) == {
        "application_agent_id": "gid:agent-1",
        "expire_time": "2027-01-01T00:00:00Z",
    }
    credentials = created.as_credentials()
    assert credentials.token == "fresh-agent-token"
    assert credentials.app_agent_id == "gid:agent-1"


def test_credentials_as_credentials_missing_config_raises(make_client, mock_api) -> None:
    """Credentials as credentials missing config raises."""
    mock_api.respond(httpx.Response(201, json={"id": "gid:cred-1"}))
    client = make_client(ConfigClient)
    created = client.create_application_agent_credential("gid:agent-1")
    with pytest.raises(CredentialsError, match="application_agent_config"):
        created.as_credentials()


def test_credentials_create_service_account_credential(make_client, mock_api) -> None:
    """Credentials create service account credential."""
    mock_api.respond(
        httpx.Response(
            201,
            json={
                "id": "gid:cred-2",
                "service_account_id": "gid:sa-1",
                "service_account_config": {"serviceAccountId": "gid:sa-1", "token": "fresh-sa-token"},
            },
        )
    )
    client = make_client(ConfigClient)
    created = client.create_service_account_credential("gid:sa-1")
    assert created.as_credentials().token == "fresh-sa-token"


def test_credentials_have_no_update_method() -> None:
    """Credentials have no update method."""
    assert not hasattr(ConfigClient, "update_application_agent_credential")
    assert not hasattr(ConfigClient, "update_service_account_credential")
    assert not hasattr(ConfigClient, "update_capture_pipeline")
    assert not hasattr(ConfigClient, "update_capture_pipeline_topic")


def test_authorization_policies_list_filters(make_client, mock_api) -> None:
    """Authorization policies list filters."""
    client = make_client(ConfigClient)
    client.list_authorization_policies("gid:project-1", policy_type="kbac", full_fetch=True)
    assert dict(mock_api.last.url.params) == {
        "project_id": "gid:project-1",
        "type": "kbac",
        "full_fetch": "true",
    }


def test_authorization_policies_full_fetch_false_omitted(make_client, mock_api) -> None:
    """Authorization policies full fetch false omitted."""
    client = make_client(ConfigClient)
    client.list_authorization_policies("gid:project-1")
    assert dict(mock_api.last.url.params) == {"project_id": "gid:project-1"}


def test_authorization_policies_create_body(make_client, mock_api) -> None:
    """Authorization policies create body."""
    client = make_client(ConfigClient)
    client.create_authorization_policy(
        "drivers", "gid:project-1", '{"meta": {"policyVersion": "2.0-kbac"}}', "ACTIVE", tags=["fleet"]
    )
    assert sent_json(mock_api.last) == {
        "name": "drivers",
        "project_id": "gid:project-1",
        "policy": '{"meta": {"policyVersion": "2.0-kbac"}}',
        "status": "ACTIVE",
        "tags": ["fleet"],
    }


def test_dict_resources_event_sink_body_passthrough(make_client, mock_api) -> None:
    """Dict resources event sink body passthrough."""
    body = {"name": "sink", "project_id": "gid:project-1", "provider": {"kafka": {"brokers": ["b:9092"]}}}
    client = make_client(ConfigClient)
    client.create_event_sink(body)
    assert mock_api.last.url.path == "/configs/v1/event-sinks"
    assert sent_json(mock_api.last) == body


def test_dict_resources_read_keeps_unknown_fields(make_client, mock_api) -> None:
    """Dict resources read keeps unknown fields."""
    mock_api.respond({"id": "gid:sink-1", "name": "sink", "provider": {"kafka": {}}, "routes": []})
    client = make_client(ConfigClient)
    sink = client.read_event_sink("gid:sink-1")
    assert sink.name == "sink"
    assert sink.field("provider") == {"kafka": {}}
    assert sink.field("missing", "fallback") == "fallback"


def test_dict_resources_mcp_server_list(make_client, mock_api) -> None:
    """Dict resources mcp server list."""
    mock_api.respond({"data": [{"id": "gid:mcp-1", "enabled": True}]})
    client = make_client(ConfigClient)
    servers = client.list_mcp_servers("gid:project-1")
    assert servers[0].field("enabled") is True


def test_dict_resources_rebuild_data_schema(make_client, mock_api) -> None:
    """Dict resources rebuild data schema."""
    mock_api.respond((202, {"status": "Rebuilding..."}))
    client = make_client(ConfigClient)
    client.rebuild_data_schema("gid:project-1")
    assert mock_api.last.url.path == "/configs/v1/data-schema/rebuild"
    assert sent_json(mock_api.last) == {"project_id": "gid:project-1"}


async def test_async_config_lifecycle(make_async_client, mock_api) -> None:
    """Async config lifecycle."""
    mock_api.respond(httpx.Response(201, json={"id": "gid:app-1"}, headers={"ETag": "e1"}))
    mock_api.respond(httpx.Response(200, json={"id": "gid:app-1", "name": "my-app"}, headers={"ETag": "e1"}))
    mock_api.respond(httpx.Response(200, json={"id": "gid:app-1"}, headers={"ETag": "e2"}))
    mock_api.respond({"id": "gid:app-1"})
    async with make_async_client(AsyncConfigClient) as client:
        created = await client.create_application("my-app", "gid:project-1")
        read = await client.read_application(created.id)
        updated = await client.update_application(created.id, etag=read.etag, display_name="My App")
        await client.delete_application(created.id, etag=updated.etag)
    assert [request.method for request in mock_api.requests] == ["POST", "GET", "PUT", "DELETE"]
    assert mock_api.requests[3].headers["If-Match"] == "e2"
