"""Asynchronous Config API client.

Method-by-method async mirror of :class:`indykite_sdk.ConfigClient`; see that
class for detailed documentation of each operation.
"""

from __future__ import annotations

from typing import Any

import httpx

from indykite_sdk._core.http import BaseAsyncClient
from indykite_sdk._core.ops import RequestSpec
from indykite_sdk.config import _resources as ops
from indykite_sdk.config.models import (
    ApiPermission,
    Application,
    ApplicationAgent,
    ApplicationAgentCredential,
    ApplicationAgentCredentialCreated,
    AuthorizationPolicy,
    ConfigResource,
    ConfigStatus,
    CreateResult,
    KnowledgeQuery,
    Organization,
    Project,
    ServiceAccount,
    ServiceAccountCredential,
    ServiceAccountCredentialCreated,
    ServiceAccountRole,
    UpdateResult,
)

__all__ = ["AsyncConfigClient"]

Timeout = httpx.Timeout | float | None


class AsyncConfigClient(BaseAsyncClient):  # skipcq: PYL-R0904 - one method per REST operation
    """Async variant of :class:`indykite_sdk.ConfigClient` - same methods, ``await``-able.

    Example::

        from indykite_sdk import AsyncConfigClient

        async with AsyncConfigClient() as config:
            org = await config.read_current_organization()
    """

    _api_prefix = "/configs/v1"
    _auth_kind = "service_account"

    # -- generic plumbing ---------------------------------------------------

    async def _list(self, path: str, model: type, params: dict[str, Any], timeout: Timeout) -> list[Any]:
        return ops.parse_list(model, await self._send(ops.list_spec(path, params), timeout=timeout))

    async def _create(self, path: str, body: dict[str, Any], timeout: Timeout, model: type = CreateResult) -> Any:
        return ops.parse_one(model, await self._send(ops.create_spec(path, body), timeout=timeout))

    async def _read(self, path: str, resource_id: str, model: type, timeout: Timeout, **kwargs: Any) -> Any:
        return ops.parse_one(model, await self._send(ops.read_spec(path, resource_id, **kwargs), timeout=timeout))

    async def _update(
        self, path: str, resource_id: str, body: dict[str, Any], etag: str, timeout: Timeout
    ) -> UpdateResult:
        return ops.parse_one(
            UpdateResult, await self._send(ops.update_spec(path, resource_id, body, etag), timeout=timeout)
        )

    async def _delete(self, path: str, resource_id: str, etag: str, timeout: Timeout) -> None:
        await self._send(ops.delete_spec(path, resource_id, etag), timeout=timeout)

    # -- organizations ------------------------------------------------------

    async def read_current_organization(self, *, timeout: Timeout = None) -> Organization:
        """Read the organization the service account belongs to."""
        response = await self._send(RequestSpec("GET", "/organizations/current"), timeout=timeout)
        return ops.parse_one(Organization, response)

    # -- projects -----------------------------------------------------------

    async def list_projects(
        self, organization_id: str, *, search: str | None = None, timeout: Timeout = None
    ) -> list[Project]:
        """List projects in an organization."""
        return await self._list("/projects", Project, {"organization_id": organization_id, "search": search}, timeout)

    async def create_project(
        self,
        name: str,
        organization_id: str,
        region: str,
        *,
        display_name: str | None = None,
        description: str | None = None,
        ikg_size: str | None = None,
        replica_region: str | None = None,
        db_connection: dict[str, Any] | None = None,
        timeout: Timeout = None,
    ) -> CreateResult:
        """Create a project."""
        body = {
            "name": name,
            "organization_id": organization_id,
            "region": region,
            "display_name": display_name,
            "description": description,
            "ikg_size": ikg_size,
            "replica_region": replica_region,
            "db_connection": db_connection,
        }
        return await self._create("/projects", body, timeout)

    async def read_project(self, project_id: str, *, version: int | None = None, timeout: Timeout = None) -> Project:
        """Read a project by ID."""
        return await self._read("/projects", project_id, Project, timeout, version=version)

    async def update_project(
        self,
        project_id: str,
        *,
        etag: str,
        display_name: str | None = None,
        description: str | None = None,
        timeout: Timeout = None,
    ) -> UpdateResult:
        """Update a project (``If-Match`` guarded)."""
        return await self._update(
            "/projects", project_id, {"display_name": display_name, "description": description}, etag, timeout
        )

    async def delete_project(self, project_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete a project (``If-Match`` guarded)."""
        await self._delete("/projects", project_id, etag, timeout)

    # -- applications -------------------------------------------------------

    async def list_applications(
        self, project_id: str, *, search: str | None = None, timeout: Timeout = None
    ) -> list[Application]:
        """List applications in a project."""
        return await self._list("/applications", Application, {"project_id": project_id, "search": search}, timeout)

    async def create_application(
        self,
        name: str,
        project_id: str,
        *,
        display_name: str | None = None,
        description: str | None = None,
        timeout: Timeout = None,
    ) -> CreateResult:
        """Create an application under a project."""
        body = {"name": name, "project_id": project_id, "display_name": display_name, "description": description}
        return await self._create("/applications", body, timeout)

    async def read_application(self, application_id: str, *, timeout: Timeout = None) -> Application:
        """Read an application by ID."""
        return await self._read("/applications", application_id, Application, timeout)

    async def update_application(
        self,
        application_id: str,
        *,
        etag: str,
        display_name: str | None = None,
        description: str | None = None,
        timeout: Timeout = None,
    ) -> UpdateResult:
        """Update an application (``If-Match`` guarded)."""
        return await self._update(
            "/applications", application_id, {"display_name": display_name, "description": description}, etag, timeout
        )

    async def delete_application(self, application_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete an application (``If-Match`` guarded)."""
        await self._delete("/applications", application_id, etag, timeout)

    # -- application agents -------------------------------------------------

    async def list_application_agents(
        self, project_id: str, *, search: str | None = None, timeout: Timeout = None
    ) -> list[ApplicationAgent]:
        """List application agents in a project."""
        return await self._list(
            "/application-agents", ApplicationAgent, {"project_id": project_id, "search": search}, timeout
        )

    async def create_application_agent(
        self,
        name: str,
        application_id: str,
        api_permissions: list[ApiPermission | str],
        *,
        display_name: str | None = None,
        description: str | None = None,
        timeout: Timeout = None,
    ) -> CreateResult:
        """Create an application agent restricted to the given API permissions."""
        body = {
            "name": name,
            "application_id": application_id,
            "api_permissions": list(api_permissions),
            "display_name": display_name,
            "description": description,
        }
        return await self._create("/application-agents", body, timeout)

    async def read_application_agent(self, agent_id: str, *, timeout: Timeout = None) -> ApplicationAgent:
        """Read an application agent by ID."""
        return await self._read("/application-agents", agent_id, ApplicationAgent, timeout)

    async def update_application_agent(
        self,
        agent_id: str,
        *,
        etag: str,
        api_permissions: list[ApiPermission | str] | None = None,
        display_name: str | None = None,
        description: str | None = None,
        timeout: Timeout = None,
    ) -> UpdateResult:
        """Update an application agent (``If-Match`` guarded)."""
        body = {
            "api_permissions": list(api_permissions) if api_permissions is not None else None,
            "display_name": display_name,
            "description": description,
        }
        return await self._update("/application-agents", agent_id, body, etag, timeout)

    async def delete_application_agent(self, agent_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete an application agent (``If-Match`` guarded)."""
        await self._delete("/application-agents", agent_id, etag, timeout)

    # -- application agent credentials (no update) --------------------------

    async def list_application_agent_credentials(
        self, project_id: str, *, search: str | None = None, timeout: Timeout = None
    ) -> list[ApplicationAgentCredential]:
        """List application-agent credential metadata in a project."""
        return await self._list(
            "/application-agent-credentials",
            ApplicationAgentCredential,
            {"project_id": project_id, "search": search},
            timeout,
        )

    async def create_application_agent_credential(
        self,
        application_agent_id: str,
        *,
        display_name: str | None = None,
        expire_time: str | None = None,
        timeout: Timeout = None,
    ) -> ApplicationAgentCredentialCreated:
        """Create an application-agent credential - the JSON is only returned this once."""
        body = {
            "application_agent_id": application_agent_id,
            "display_name": display_name,
            "expire_time": expire_time,
        }
        return await self._create("/application-agent-credentials", body, timeout, ApplicationAgentCredentialCreated)

    async def read_application_agent_credential(
        self, credential_id: str, *, timeout: Timeout = None
    ) -> ApplicationAgentCredential:
        """Read credential metadata (never the secret) by ID."""
        return await self._read("/application-agent-credentials", credential_id, ApplicationAgentCredential, timeout)

    async def delete_application_agent_credential(
        self, credential_id: str, *, etag: str, timeout: Timeout = None
    ) -> None:
        """Revoke an application-agent credential (``If-Match`` guarded)."""
        await self._delete("/application-agent-credentials", credential_id, etag, timeout)

    # -- service accounts ---------------------------------------------------

    async def list_service_accounts(
        self, organization_id: str, *, search: str | None = None, timeout: Timeout = None
    ) -> list[ServiceAccount]:
        """List service accounts in an organization."""
        return await self._list(
            "/service-accounts", ServiceAccount, {"organization_id": organization_id, "search": search}, timeout
        )

    async def create_service_account(
        self,
        name: str,
        organization_id: str,
        role: ServiceAccountRole | str,
        *,
        display_name: str | None = None,
        description: str | None = None,
        timeout: Timeout = None,
    ) -> CreateResult:
        """Create a service account (``role``: ``all_editor`` or ``all_viewer``)."""
        body = {
            "name": name,
            "organization_id": organization_id,
            "role": role,
            "display_name": display_name,
            "description": description,
        }
        return await self._create("/service-accounts", body, timeout)

    async def read_service_account(self, service_account_id: str, *, timeout: Timeout = None) -> ServiceAccount:
        """Read a service account by ID."""
        return await self._read("/service-accounts", service_account_id, ServiceAccount, timeout)

    async def update_service_account(
        self,
        service_account_id: str,
        *,
        etag: str,
        display_name: str | None = None,
        description: str | None = None,
        timeout: Timeout = None,
    ) -> UpdateResult:
        """Update a service account (``If-Match`` guarded)."""
        return await self._update(
            "/service-accounts",
            service_account_id,
            {"display_name": display_name, "description": description},
            etag,
            timeout,
        )

    async def delete_service_account(self, service_account_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete a service account (``If-Match`` guarded)."""
        await self._delete("/service-accounts", service_account_id, etag, timeout)

    # -- service account credentials (no update) ----------------------------

    async def list_service_account_credentials(
        self, organization_id: str, *, search: str | None = None, timeout: Timeout = None
    ) -> list[ServiceAccountCredential]:
        """List service-account credential metadata."""
        return await self._list(
            "/service-account-credentials",
            ServiceAccountCredential,
            {"organization_id": organization_id, "search": search},
            timeout,
        )

    async def create_service_account_credential(
        self,
        service_account_id: str,
        *,
        display_name: str | None = None,
        expire_time: str | None = None,
        timeout: Timeout = None,
    ) -> ServiceAccountCredentialCreated:
        """Create a service-account credential - the JSON is only returned this once."""
        body = {"service_account_id": service_account_id, "display_name": display_name, "expire_time": expire_time}
        return await self._create("/service-account-credentials", body, timeout, ServiceAccountCredentialCreated)

    async def read_service_account_credential(
        self, credential_id: str, *, timeout: Timeout = None
    ) -> ServiceAccountCredential:
        """Read credential metadata (never the secret) by ID."""
        return await self._read("/service-account-credentials", credential_id, ServiceAccountCredential, timeout)

    async def delete_service_account_credential(
        self, credential_id: str, *, etag: str, timeout: Timeout = None
    ) -> None:
        """Revoke a service-account credential (``If-Match`` guarded)."""
        await self._delete("/service-account-credentials", credential_id, etag, timeout)

    # -- authorization policies ---------------------------------------------

    async def list_authorization_policies(
        self,
        project_id: str,
        *,
        policy_type: str | None = None,
        full_fetch: bool = False,
        search: str | None = None,
        timeout: Timeout = None,
    ) -> list[AuthorizationPolicy]:
        """List authorization policies; ``policy_type`` ("kbac" or "ciq") maps to the ``type`` filter."""
        params = {"project_id": project_id, "type": policy_type, "full_fetch": full_fetch, "search": search}
        return await self._list("/authorization-policies", AuthorizationPolicy, params, timeout)

    async def create_authorization_policy(
        self,
        name: str,
        project_id: str,
        policy: str,
        status: ConfigStatus | str,
        *,
        tags: list[str] | None = None,
        display_name: str | None = None,
        description: str | None = None,
        timeout: Timeout = None,
    ) -> CreateResult:
        """Create an authorization policy (``policy`` is the JSON document as a string)."""
        body = {
            "name": name,
            "project_id": project_id,
            "policy": policy,
            "status": status,
            "tags": tags,
            "display_name": display_name,
            "description": description,
        }
        return await self._create("/authorization-policies", body, timeout)

    async def read_authorization_policy(self, policy_id: str, *, timeout: Timeout = None) -> AuthorizationPolicy:
        """Read an authorization policy by ID."""
        return await self._read("/authorization-policies", policy_id, AuthorizationPolicy, timeout)

    async def update_authorization_policy(
        self,
        policy_id: str,
        *,
        etag: str,
        policy: str | None = None,
        status: ConfigStatus | str | None = None,
        tags: list[str] | None = None,
        display_name: str | None = None,
        description: str | None = None,
        timeout: Timeout = None,
    ) -> UpdateResult:
        """Update an authorization policy (``If-Match`` guarded)."""
        body = {
            "policy": policy,
            "status": status,
            "tags": tags,
            "display_name": display_name,
            "description": description,
        }
        return await self._update("/authorization-policies", policy_id, body, etag, timeout)

    async def delete_authorization_policy(self, policy_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete an authorization policy (``If-Match`` guarded)."""
        await self._delete("/authorization-policies", policy_id, etag, timeout)

    # -- knowledge queries ---------------------------------------------------

    async def list_knowledge_queries(
        self,
        project_id: str,
        *,
        full_fetch: bool = False,
        search: str | None = None,
        timeout: Timeout = None,
    ) -> list[KnowledgeQuery]:
        """List knowledge queries in a project."""
        params = {"project_id": project_id, "full_fetch": full_fetch, "search": search}
        return await self._list("/knowledge-queries", KnowledgeQuery, params, timeout)

    async def create_knowledge_query(
        self,
        name: str,
        project_id: str,
        query: str,
        status: ConfigStatus | str,
        policy_id: str,
        *,
        display_name: str | None = None,
        description: str | None = None,
        timeout: Timeout = None,
    ) -> CreateResult:
        """Create a knowledge query guarded by the CIQ policy ``policy_id``."""
        body = {
            "name": name,
            "project_id": project_id,
            "query": query,
            "status": status,
            "policy_id": policy_id,
            "display_name": display_name,
            "description": description,
        }
        return await self._create("/knowledge-queries", body, timeout)

    async def read_knowledge_query(self, query_id: str, *, timeout: Timeout = None) -> KnowledgeQuery:
        """Read a knowledge query by ID."""
        return await self._read("/knowledge-queries", query_id, KnowledgeQuery, timeout)

    async def update_knowledge_query(
        self,
        query_id: str,
        *,
        etag: str,
        query: str | None = None,
        status: ConfigStatus | str | None = None,
        policy_id: str | None = None,
        display_name: str | None = None,
        description: str | None = None,
        timeout: Timeout = None,
    ) -> UpdateResult:
        """Update a knowledge query (``If-Match`` guarded)."""
        body = {
            "query": query,
            "status": status,
            "policy_id": policy_id,
            "display_name": display_name,
            "description": description,
        }
        return await self._update("/knowledge-queries", query_id, body, etag, timeout)

    async def delete_knowledge_query(self, query_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete a knowledge query (``If-Match`` guarded)."""
        await self._delete("/knowledge-queries", query_id, etag, timeout)

    # -- dict-payload resources ---------------------------------------------

    async def list_event_sinks(
        self, project_id: str, *, full_fetch: bool = False, search: str | None = None, timeout: Timeout = None
    ) -> list[ConfigResource]:
        """List event sinks in a project."""
        params = {"project_id": project_id, "full_fetch": full_fetch, "search": search}
        return await self._list("/event-sinks", ConfigResource, params, timeout)

    async def create_event_sink(self, body: dict[str, Any], *, timeout: Timeout = None) -> CreateResult:
        """Create an event sink from its documented JSON body."""
        return await self._create("/event-sinks", body, timeout)

    async def read_event_sink(self, sink_id: str, *, timeout: Timeout = None) -> ConfigResource:
        """Read an event sink by ID."""
        return await self._read("/event-sinks", sink_id, ConfigResource, timeout)

    async def update_event_sink(
        self, sink_id: str, body: dict[str, Any], *, etag: str, timeout: Timeout = None
    ) -> UpdateResult:
        """Update an event sink (``If-Match`` guarded)."""
        return await self._update("/event-sinks", sink_id, body, etag, timeout)

    async def delete_event_sink(self, sink_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete an event sink (``If-Match`` guarded)."""
        await self._delete("/event-sinks", sink_id, etag, timeout)

    async def list_external_data_resolvers(
        self, project_id: str, *, full_fetch: bool = False, search: str | None = None, timeout: Timeout = None
    ) -> list[ConfigResource]:
        """List external data resolvers in a project."""
        params = {"project_id": project_id, "full_fetch": full_fetch, "search": search}
        return await self._list("/external-data-resolvers", ConfigResource, params, timeout)

    async def create_external_data_resolver(self, body: dict[str, Any], *, timeout: Timeout = None) -> CreateResult:
        """Create an external data resolver from its documented JSON body."""
        return await self._create("/external-data-resolvers", body, timeout)

    async def read_external_data_resolver(self, resolver_id: str, *, timeout: Timeout = None) -> ConfigResource:
        """Read an external data resolver by ID."""
        return await self._read("/external-data-resolvers", resolver_id, ConfigResource, timeout)

    async def update_external_data_resolver(
        self, resolver_id: str, body: dict[str, Any], *, etag: str, timeout: Timeout = None
    ) -> UpdateResult:
        """Update an external data resolver (``If-Match`` guarded)."""
        return await self._update("/external-data-resolvers", resolver_id, body, etag, timeout)

    async def delete_external_data_resolver(self, resolver_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete an external data resolver (``If-Match`` guarded)."""
        await self._delete("/external-data-resolvers", resolver_id, etag, timeout)

    async def list_token_introspects(
        self, project_id: str, *, full_fetch: bool = False, search: str | None = None, timeout: Timeout = None
    ) -> list[ConfigResource]:
        """List token-introspect configurations in a project."""
        params = {"project_id": project_id, "full_fetch": full_fetch, "search": search}
        return await self._list("/token-introspects", ConfigResource, params, timeout)

    async def create_token_introspect(self, body: dict[str, Any], *, timeout: Timeout = None) -> CreateResult:
        """Create a token-introspect configuration from its documented JSON body."""
        return await self._create("/token-introspects", body, timeout)

    async def read_token_introspect(self, introspect_id: str, *, timeout: Timeout = None) -> ConfigResource:
        """Read a token-introspect configuration by ID."""
        return await self._read("/token-introspects", introspect_id, ConfigResource, timeout)

    async def update_token_introspect(
        self, introspect_id: str, body: dict[str, Any], *, etag: str, timeout: Timeout = None
    ) -> UpdateResult:
        """Update a token-introspect configuration (``If-Match`` guarded)."""
        return await self._update("/token-introspects", introspect_id, body, etag, timeout)

    async def delete_token_introspect(self, introspect_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete a token-introspect configuration (``If-Match`` guarded)."""
        await self._delete("/token-introspects", introspect_id, etag, timeout)

    async def list_trust_score_profiles(
        self, project_id: str, *, full_fetch: bool = False, search: str | None = None, timeout: Timeout = None
    ) -> list[ConfigResource]:
        """List trust-score profiles in a project."""
        params = {"project_id": project_id, "full_fetch": full_fetch, "search": search}
        return await self._list("/trust-score-profiles", ConfigResource, params, timeout)

    async def create_trust_score_profile(self, body: dict[str, Any], *, timeout: Timeout = None) -> CreateResult:
        """Create a trust-score profile from its documented JSON body."""
        return await self._create("/trust-score-profiles", body, timeout)

    async def read_trust_score_profile(self, profile_id: str, *, timeout: Timeout = None) -> ConfigResource:
        """Read a trust-score profile by ID."""
        return await self._read("/trust-score-profiles", profile_id, ConfigResource, timeout)

    async def update_trust_score_profile(
        self, profile_id: str, body: dict[str, Any], *, etag: str, timeout: Timeout = None
    ) -> UpdateResult:
        """Update a trust-score profile (``If-Match`` guarded)."""
        return await self._update("/trust-score-profiles", profile_id, body, etag, timeout)

    async def delete_trust_score_profile(self, profile_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete a trust-score profile (``If-Match`` guarded)."""
        await self._delete("/trust-score-profiles", profile_id, etag, timeout)

    async def list_entity_matching_pipelines(
        self, project_id: str, *, full_fetch: bool = False, search: str | None = None, timeout: Timeout = None
    ) -> list[ConfigResource]:
        """List entity-matching pipelines in a project."""
        params = {"project_id": project_id, "full_fetch": full_fetch, "search": search}
        return await self._list("/entity-matching-pipelines", ConfigResource, params, timeout)

    async def create_entity_matching_pipeline(self, body: dict[str, Any], *, timeout: Timeout = None) -> CreateResult:
        """Create an entity-matching pipeline from its documented JSON body."""
        return await self._create("/entity-matching-pipelines", body, timeout)

    async def read_entity_matching_pipeline(self, pipeline_id: str, *, timeout: Timeout = None) -> ConfigResource:
        """Read an entity-matching pipeline by ID."""
        return await self._read("/entity-matching-pipelines", pipeline_id, ConfigResource, timeout)

    async def update_entity_matching_pipeline(
        self, pipeline_id: str, body: dict[str, Any], *, etag: str, timeout: Timeout = None
    ) -> UpdateResult:
        """Update an entity-matching pipeline (``If-Match`` guarded)."""
        return await self._update("/entity-matching-pipelines", pipeline_id, body, etag, timeout)

    async def delete_entity_matching_pipeline(self, pipeline_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete an entity-matching pipeline (``If-Match`` guarded)."""
        await self._delete("/entity-matching-pipelines", pipeline_id, etag, timeout)

    async def list_mcp_servers(self, project_id: str, *, timeout: Timeout = None) -> list[ConfigResource]:
        """List MCP server configurations in a project."""
        return await self._list("/mcp-servers", ConfigResource, {"project_id": project_id}, timeout)

    async def create_mcp_server(self, body: dict[str, Any], *, timeout: Timeout = None) -> CreateResult:
        """Create an MCP server configuration from its documented JSON body."""
        return await self._create("/mcp-servers", body, timeout)

    async def read_mcp_server(self, server_id: str, *, timeout: Timeout = None) -> ConfigResource:
        """Read an MCP server configuration by ID."""
        return await self._read("/mcp-servers", server_id, ConfigResource, timeout)

    async def update_mcp_server(
        self, server_id: str, body: dict[str, Any], *, etag: str, timeout: Timeout = None
    ) -> UpdateResult:
        """Update an MCP server configuration (``If-Match`` guarded)."""
        return await self._update("/mcp-servers", server_id, body, etag, timeout)

    async def delete_mcp_server(self, server_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete an MCP server configuration (``If-Match`` guarded)."""
        await self._delete("/mcp-servers", server_id, etag, timeout)

    # -- capture pipelines (no update) --------------------------------------

    async def list_capture_pipelines(
        self, project_id: str, *, full_fetch: bool = False, search: str | None = None, timeout: Timeout = None
    ) -> list[ConfigResource]:
        """List capture pipelines in a project."""
        params = {"project_id": project_id, "full_fetch": full_fetch, "search": search}
        return await self._list("/capture-pipelines", ConfigResource, params, timeout)

    async def create_capture_pipeline(self, body: dict[str, Any], *, timeout: Timeout = None) -> CreateResult:
        """Create a capture pipeline from its documented JSON body."""
        return await self._create("/capture-pipelines", body, timeout)

    async def read_capture_pipeline(self, pipeline_id: str, *, timeout: Timeout = None) -> ConfigResource:
        """Read a capture pipeline by ID."""
        return await self._read("/capture-pipelines", pipeline_id, ConfigResource, timeout)

    async def delete_capture_pipeline(self, pipeline_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete a capture pipeline (``If-Match`` guarded)."""
        await self._delete("/capture-pipelines", pipeline_id, etag, timeout)

    async def list_capture_pipeline_topics(
        self, project_id: str, *, full_fetch: bool = False, search: str | None = None, timeout: Timeout = None
    ) -> list[ConfigResource]:
        """List capture-pipeline topics in a project."""
        params = {"project_id": project_id, "full_fetch": full_fetch, "search": search}
        return await self._list("/capture-pipeline-topics", ConfigResource, params, timeout)

    async def create_capture_pipeline_topic(self, body: dict[str, Any], *, timeout: Timeout = None) -> CreateResult:
        """Create a capture-pipeline topic from its documented JSON body."""
        return await self._create("/capture-pipeline-topics", body, timeout)

    async def read_capture_pipeline_topic(self, topic_id: str, *, timeout: Timeout = None) -> ConfigResource:
        """Read a capture-pipeline topic by ID."""
        return await self._read("/capture-pipeline-topics", topic_id, ConfigResource, timeout)

    async def delete_capture_pipeline_topic(self, topic_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete a capture-pipeline topic (``If-Match`` guarded)."""
        await self._delete("/capture-pipeline-topics", topic_id, etag, timeout)

    # -- data schema --------------------------------------------------------

    async def rebuild_data_schema(self, project_id: str, *, timeout: Timeout = None) -> None:
        """Trigger a rebuild of the project's IKG data schema. **Experimental** (not in public spec)."""
        await self._send(
            RequestSpec("POST", "/data-schema/rebuild", json_body={"project_id": project_id}), timeout=timeout
        )
