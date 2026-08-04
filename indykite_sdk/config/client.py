"""Synchronous Config API client."""

from __future__ import annotations

from typing import Any

import httpx

from indykite_sdk._core.http import BaseSyncClient
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

__all__ = ["ConfigClient"]

Timeout = httpx.Timeout | float | None


class ConfigClient(BaseSyncClient):  # skipcq: PYL-R0904 - one method per REST operation
    """Manage IndyKite platform configuration via the Config API (``/configs/v1``).

    Authenticates with **service-account** credentials
    (``INDYKITE_SERVICE_ACCOUNT_CREDENTIALS[_FILE]``) as a bearer token.

    Every resource follows the same lifecycle:

    - ``create_*`` returns a :class:`~indykite_sdk.config.models.CreateResult`
      whose ``.id`` and ``.etag`` you keep;
    - ``read_*`` returns the resource with a fresh ``.etag``;
    - ``update_*`` and ``delete_*`` require that ``etag`` (``If-Match``) - a
      stale value raises :class:`~indykite_sdk.ETagMismatchError`, in which
      case re-read and retry.

    Example: bootstrap a project with an application agent::

        from indykite_sdk import ConfigClient

        with ConfigClient() as config:
            org = config.read_current_organization()
            project = config.create_project("my-project", org.id, region="europe-west1")
            app = config.create_application("my-app", project.id)
            agent = config.create_application_agent(
                "my-agent", app.id, api_permissions=["Authorization", "Capture", "ContXIQ"]
            )
            credential = config.create_application_agent_credential(agent.id)
            credential.as_credentials()  # shown once - store it now

    Resources the SDK does not fully type yet (event sinks, token introspects,
    trust-score profiles, external data resolvers, capture pipelines, entity
    matching pipelines, MCP servers) take/return their documented JSON bodies
    as dicts - see https://openapi.indykite.com/api-documentation-config.
    """

    _api_prefix = "/configs/v1"
    _auth_kind = "service_account"

    # -- generic plumbing ---------------------------------------------------

    def _list(self, path: str, model: type, params: dict[str, Any], timeout: Timeout) -> list[Any]:
        return ops.parse_list(model, self._send(ops.list_spec(path, params), timeout=timeout))

    def _create(self, path: str, body: dict[str, Any], timeout: Timeout, model: type = CreateResult) -> Any:
        return ops.parse_one(model, self._send(ops.create_spec(path, body), timeout=timeout))

    def _read(self, path: str, resource_id: str, model: type, timeout: Timeout, **kwargs: Any) -> Any:
        return ops.parse_one(model, self._send(ops.read_spec(path, resource_id, **kwargs), timeout=timeout))

    def _update(self, path: str, resource_id: str, body: dict[str, Any], etag: str, timeout: Timeout) -> UpdateResult:
        return ops.parse_one(UpdateResult, self._send(ops.update_spec(path, resource_id, body, etag), timeout=timeout))

    def _delete(self, path: str, resource_id: str, etag: str, timeout: Timeout) -> None:
        self._send(ops.delete_spec(path, resource_id, etag), timeout=timeout)

    # -- organizations ------------------------------------------------------

    def read_current_organization(self, *, timeout: Timeout = None) -> Organization:
        """Read the organization the service account belongs to (``GET /organizations/current``)."""
        return ops.parse_one(Organization, self._send(RequestSpec("GET", "/organizations/current"), timeout=timeout))

    # -- projects -----------------------------------------------------------

    def list_projects(
        self, organization_id: str, *, search: str | None = None, timeout: Timeout = None
    ) -> list[Project]:
        """List projects in an organization."""
        return self._list("/projects", Project, {"organization_id": organization_id, "search": search}, timeout)

    def create_project(
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
        """Create a project with its own IKG."""
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
        return self._create("/projects", body, timeout)

    def read_project(self, project_id: str, *, version: int | None = None, timeout: Timeout = None) -> Project:
        """Read a project by ID."""
        return self._read("/projects", project_id, Project, timeout, version=version)

    def update_project(
        self,
        project_id: str,
        *,
        etag: str,
        display_name: str | None = None,
        description: str | None = None,
        timeout: Timeout = None,
    ) -> UpdateResult:
        """Update a project's display name/description (``If-Match`` guarded)."""
        body = {"display_name": display_name, "description": description}
        return self._update("/projects", project_id, body, etag, timeout)

    def delete_project(self, project_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete a project and everything in it (``If-Match`` guarded)."""
        self._delete("/projects", project_id, etag, timeout)

    # -- applications -------------------------------------------------------

    def list_applications(
        self, project_id: str, *, search: str | None = None, timeout: Timeout = None
    ) -> list[Application]:
        """List applications in a project."""
        return self._list("/applications", Application, {"project_id": project_id, "search": search}, timeout)

    def create_application(
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
        return self._create("/applications", body, timeout)

    def read_application(self, application_id: str, *, timeout: Timeout = None) -> Application:
        """Read an application by ID."""
        return self._read("/applications", application_id, Application, timeout)

    def update_application(
        self,
        application_id: str,
        *,
        etag: str,
        display_name: str | None = None,
        description: str | None = None,
        timeout: Timeout = None,
    ) -> UpdateResult:
        """Update an application (``If-Match`` guarded)."""
        body = {"display_name": display_name, "description": description}
        return self._update("/applications", application_id, body, etag, timeout)

    def delete_application(self, application_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete an application (``If-Match`` guarded)."""
        self._delete("/applications", application_id, etag, timeout)

    # -- application agents -------------------------------------------------

    def list_application_agents(
        self, project_id: str, *, search: str | None = None, timeout: Timeout = None
    ) -> list[ApplicationAgent]:
        """List application agents in a project."""
        return self._list(
            "/application-agents", ApplicationAgent, {"project_id": project_id, "search": search}, timeout
        )

    def create_application_agent(
        self,
        name: str,
        application_id: str,
        api_permissions: list[ApiPermission | str],
        *,
        display_name: str | None = None,
        description: str | None = None,
        timeout: Timeout = None,
    ) -> CreateResult:
        """Create an application agent restricted to the given API permissions.

        ``api_permissions`` values: ``Authorization``, ``Capture``, ``ContXIQ``,
        ``EntityMatching``, ``IKGRead``, ``ReadDataSchema``.
        """
        body = {
            "name": name,
            "application_id": application_id,
            "api_permissions": list(api_permissions),
            "display_name": display_name,
            "description": description,
        }
        return self._create("/application-agents", body, timeout)

    def read_application_agent(self, agent_id: str, *, timeout: Timeout = None) -> ApplicationAgent:
        """Read an application agent by ID."""
        return self._read("/application-agents", agent_id, ApplicationAgent, timeout)

    def update_application_agent(
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
        return self._update("/application-agents", agent_id, body, etag, timeout)

    def delete_application_agent(self, agent_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete an application agent (``If-Match`` guarded)."""
        self._delete("/application-agents", agent_id, etag, timeout)

    # -- application agent credentials (no update) --------------------------

    def list_application_agent_credentials(
        self, project_id: str, *, search: str | None = None, timeout: Timeout = None
    ) -> list[ApplicationAgentCredential]:
        """List application-agent credential metadata in a project (secrets are never returned)."""
        return self._list(
            "/application-agent-credentials",
            ApplicationAgentCredential,
            {"project_id": project_id, "search": search},
            timeout,
        )

    def create_application_agent_credential(
        self,
        application_agent_id: str,
        *,
        display_name: str | None = None,
        expire_time: str | None = None,
        timeout: Timeout = None,
    ) -> ApplicationAgentCredentialCreated:
        """Create a credential for an application agent.

        The response's :meth:`~indykite_sdk.config.models.core.ApplicationAgentCredentialCreated.as_credentials`
        is the **only** time the credential JSON is available - store it.

        Args:
            expire_time: Optional RFC 3339 expiry, e.g. ``"2027-08-04T00:00:00Z"``.
        """
        body = {
            "application_agent_id": application_agent_id,
            "display_name": display_name,
            "expire_time": expire_time,
        }
        return self._create("/application-agent-credentials", body, timeout, ApplicationAgentCredentialCreated)

    def read_application_agent_credential(
        self, credential_id: str, *, timeout: Timeout = None
    ) -> ApplicationAgentCredential:
        """Read credential metadata (never the secret) by ID."""
        return self._read("/application-agent-credentials", credential_id, ApplicationAgentCredential, timeout)

    def delete_application_agent_credential(self, credential_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Revoke an application-agent credential (``If-Match`` guarded)."""
        self._delete("/application-agent-credentials", credential_id, etag, timeout)

    # -- service accounts ---------------------------------------------------

    def list_service_accounts(
        self, organization_id: str, *, search: str | None = None, timeout: Timeout = None
    ) -> list[ServiceAccount]:
        """List service accounts in an organization."""
        return self._list(
            "/service-accounts", ServiceAccount, {"organization_id": organization_id, "search": search}, timeout
        )

    def create_service_account(
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
        return self._create("/service-accounts", body, timeout)

    def read_service_account(self, service_account_id: str, *, timeout: Timeout = None) -> ServiceAccount:
        """Read a service account by ID."""
        return self._read("/service-accounts", service_account_id, ServiceAccount, timeout)

    def update_service_account(
        self,
        service_account_id: str,
        *,
        etag: str,
        display_name: str | None = None,
        description: str | None = None,
        timeout: Timeout = None,
    ) -> UpdateResult:
        """Update a service account (``If-Match`` guarded)."""
        body = {"display_name": display_name, "description": description}
        return self._update("/service-accounts", service_account_id, body, etag, timeout)

    def delete_service_account(self, service_account_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete a service account (``If-Match`` guarded)."""
        self._delete("/service-accounts", service_account_id, etag, timeout)

    # -- service account credentials (no update) ----------------------------

    def list_service_account_credentials(
        self, organization_id: str, *, search: str | None = None, timeout: Timeout = None
    ) -> list[ServiceAccountCredential]:
        """List service-account credential metadata (secrets are never returned)."""
        return self._list(
            "/service-account-credentials",
            ServiceAccountCredential,
            {"organization_id": organization_id, "search": search},
            timeout,
        )

    def create_service_account_credential(
        self,
        service_account_id: str,
        *,
        display_name: str | None = None,
        expire_time: str | None = None,
        timeout: Timeout = None,
    ) -> ServiceAccountCredentialCreated:
        """Create a credential for a service account - the JSON is only returned this once."""
        body = {"service_account_id": service_account_id, "display_name": display_name, "expire_time": expire_time}
        return self._create("/service-account-credentials", body, timeout, ServiceAccountCredentialCreated)

    def read_service_account_credential(
        self, credential_id: str, *, timeout: Timeout = None
    ) -> ServiceAccountCredential:
        """Read credential metadata (never the secret) by ID."""
        return self._read("/service-account-credentials", credential_id, ServiceAccountCredential, timeout)

    def delete_service_account_credential(self, credential_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Revoke a service-account credential (``If-Match`` guarded)."""
        self._delete("/service-account-credentials", credential_id, etag, timeout)

    # -- authorization policies ---------------------------------------------

    def list_authorization_policies(
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
        return self._list("/authorization-policies", AuthorizationPolicy, params, timeout)

    def create_authorization_policy(
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
        """Create an authorization policy.

        ``policy`` is the policy document as a JSON **string** (``2.0-kbac``,
        ``3.0-kbac``, or CIQ format). With ``status="DRAFT"`` an invalid
        document may be saved; ``ACTIVE`` requires it to validate.
        """
        body = {
            "name": name,
            "project_id": project_id,
            "policy": policy,
            "status": status,
            "tags": tags,
            "display_name": display_name,
            "description": description,
        }
        return self._create("/authorization-policies", body, timeout)

    def read_authorization_policy(self, policy_id: str, *, timeout: Timeout = None) -> AuthorizationPolicy:
        """Read an authorization policy by ID."""
        return self._read("/authorization-policies", policy_id, AuthorizationPolicy, timeout)

    def update_authorization_policy(
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
        return self._update("/authorization-policies", policy_id, body, etag, timeout)

    def delete_authorization_policy(self, policy_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete an authorization policy (``If-Match`` guarded)."""
        self._delete("/authorization-policies", policy_id, etag, timeout)

    # -- knowledge queries ---------------------------------------------------

    def list_knowledge_queries(
        self,
        project_id: str,
        *,
        full_fetch: bool = False,
        search: str | None = None,
        timeout: Timeout = None,
    ) -> list[KnowledgeQuery]:
        """List knowledge queries in a project."""
        params = {"project_id": project_id, "full_fetch": full_fetch, "search": search}
        return self._list("/knowledge-queries", KnowledgeQuery, params, timeout)

    def create_knowledge_query(
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
        """Create a knowledge query (executed via :class:`~indykite_sdk.CIQClient`).

        ``query`` is the knowledge-query document as a JSON **string**;
        ``policy_id`` names the CIQ authorization policy that guards it.
        """
        body = {
            "name": name,
            "project_id": project_id,
            "query": query,
            "status": status,
            "policy_id": policy_id,
            "display_name": display_name,
            "description": description,
        }
        return self._create("/knowledge-queries", body, timeout)

    def read_knowledge_query(self, query_id: str, *, timeout: Timeout = None) -> KnowledgeQuery:
        """Read a knowledge query by ID."""
        return self._read("/knowledge-queries", query_id, KnowledgeQuery, timeout)

    def update_knowledge_query(
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
        return self._update("/knowledge-queries", query_id, body, etag, timeout)

    def delete_knowledge_query(self, query_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete a knowledge query (``If-Match`` guarded)."""
        self._delete("/knowledge-queries", query_id, etag, timeout)

    # -- dict-payload resources ---------------------------------------------
    # These resources have large, evolving schemas; the SDK passes their
    # documented JSON bodies through as dicts. See
    # https://openapi.indykite.com/api-documentation-config for each format.

    def list_event_sinks(
        self, project_id: str, *, full_fetch: bool = False, search: str | None = None, timeout: Timeout = None
    ) -> list[ConfigResource]:
        """List event sinks (outbound event configurations) in a project."""
        params = {"project_id": project_id, "full_fetch": full_fetch, "search": search}
        return self._list("/event-sinks", ConfigResource, params, timeout)

    def create_event_sink(self, body: dict[str, Any], *, timeout: Timeout = None) -> CreateResult:
        """Create an event sink from its documented JSON body (Kafka/Event Grid/Service Bus/PubSub)."""
        return self._create("/event-sinks", body, timeout)

    def read_event_sink(self, sink_id: str, *, timeout: Timeout = None) -> ConfigResource:
        """Read an event sink by ID."""
        return self._read("/event-sinks", sink_id, ConfigResource, timeout)

    def update_event_sink(
        self, sink_id: str, body: dict[str, Any], *, etag: str, timeout: Timeout = None
    ) -> UpdateResult:
        """Update an event sink (``If-Match`` guarded)."""
        return self._update("/event-sinks", sink_id, body, etag, timeout)

    def delete_event_sink(self, sink_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete an event sink (``If-Match`` guarded)."""
        self._delete("/event-sinks", sink_id, etag, timeout)

    def list_external_data_resolvers(
        self, project_id: str, *, full_fetch: bool = False, search: str | None = None, timeout: Timeout = None
    ) -> list[ConfigResource]:
        """List external data resolvers in a project."""
        params = {"project_id": project_id, "full_fetch": full_fetch, "search": search}
        return self._list("/external-data-resolvers", ConfigResource, params, timeout)

    def create_external_data_resolver(self, body: dict[str, Any], *, timeout: Timeout = None) -> CreateResult:
        """Create an external data resolver from its documented JSON body."""
        return self._create("/external-data-resolvers", body, timeout)

    def read_external_data_resolver(self, resolver_id: str, *, timeout: Timeout = None) -> ConfigResource:
        """Read an external data resolver by ID."""
        return self._read("/external-data-resolvers", resolver_id, ConfigResource, timeout)

    def update_external_data_resolver(
        self, resolver_id: str, body: dict[str, Any], *, etag: str, timeout: Timeout = None
    ) -> UpdateResult:
        """Update an external data resolver (``If-Match`` guarded)."""
        return self._update("/external-data-resolvers", resolver_id, body, etag, timeout)

    def delete_external_data_resolver(self, resolver_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete an external data resolver (``If-Match`` guarded)."""
        self._delete("/external-data-resolvers", resolver_id, etag, timeout)

    def list_token_introspects(
        self, project_id: str, *, full_fetch: bool = False, search: str | None = None, timeout: Timeout = None
    ) -> list[ConfigResource]:
        """List token-introspect configurations in a project."""
        params = {"project_id": project_id, "full_fetch": full_fetch, "search": search}
        return self._list("/token-introspects", ConfigResource, params, timeout)

    def create_token_introspect(self, body: dict[str, Any], *, timeout: Timeout = None) -> CreateResult:
        """Create a token-introspect configuration from its documented JSON body."""
        return self._create("/token-introspects", body, timeout)

    def read_token_introspect(self, introspect_id: str, *, timeout: Timeout = None) -> ConfigResource:
        """Read a token-introspect configuration by ID."""
        return self._read("/token-introspects", introspect_id, ConfigResource, timeout)

    def update_token_introspect(
        self, introspect_id: str, body: dict[str, Any], *, etag: str, timeout: Timeout = None
    ) -> UpdateResult:
        """Update a token-introspect configuration (``If-Match`` guarded)."""
        return self._update("/token-introspects", introspect_id, body, etag, timeout)

    def delete_token_introspect(self, introspect_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete a token-introspect configuration (``If-Match`` guarded)."""
        self._delete("/token-introspects", introspect_id, etag, timeout)

    def list_trust_score_profiles(
        self, project_id: str, *, full_fetch: bool = False, search: str | None = None, timeout: Timeout = None
    ) -> list[ConfigResource]:
        """List trust-score profiles in a project."""
        params = {"project_id": project_id, "full_fetch": full_fetch, "search": search}
        return self._list("/trust-score-profiles", ConfigResource, params, timeout)

    def create_trust_score_profile(self, body: dict[str, Any], *, timeout: Timeout = None) -> CreateResult:
        """Create a trust-score profile from its documented JSON body."""
        return self._create("/trust-score-profiles", body, timeout)

    def read_trust_score_profile(self, profile_id: str, *, timeout: Timeout = None) -> ConfigResource:
        """Read a trust-score profile by ID."""
        return self._read("/trust-score-profiles", profile_id, ConfigResource, timeout)

    def update_trust_score_profile(
        self, profile_id: str, body: dict[str, Any], *, etag: str, timeout: Timeout = None
    ) -> UpdateResult:
        """Update a trust-score profile (``If-Match`` guarded)."""
        return self._update("/trust-score-profiles", profile_id, body, etag, timeout)

    def delete_trust_score_profile(self, profile_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete a trust-score profile (``If-Match`` guarded)."""
        self._delete("/trust-score-profiles", profile_id, etag, timeout)

    def list_entity_matching_pipelines(
        self, project_id: str, *, full_fetch: bool = False, search: str | None = None, timeout: Timeout = None
    ) -> list[ConfigResource]:
        """List entity-matching pipelines in a project."""
        params = {"project_id": project_id, "full_fetch": full_fetch, "search": search}
        return self._list("/entity-matching-pipelines", ConfigResource, params, timeout)

    def create_entity_matching_pipeline(self, body: dict[str, Any], *, timeout: Timeout = None) -> CreateResult:
        """Create an entity-matching pipeline (run it with :class:`~indykite_sdk.EntityMatchingClient`)."""
        return self._create("/entity-matching-pipelines", body, timeout)

    def read_entity_matching_pipeline(self, pipeline_id: str, *, timeout: Timeout = None) -> ConfigResource:
        """Read an entity-matching pipeline by ID."""
        return self._read("/entity-matching-pipelines", pipeline_id, ConfigResource, timeout)

    def update_entity_matching_pipeline(
        self, pipeline_id: str, body: dict[str, Any], *, etag: str, timeout: Timeout = None
    ) -> UpdateResult:
        """Update an entity-matching pipeline (``If-Match`` guarded)."""
        return self._update("/entity-matching-pipelines", pipeline_id, body, etag, timeout)

    def delete_entity_matching_pipeline(self, pipeline_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete an entity-matching pipeline (``If-Match`` guarded)."""
        self._delete("/entity-matching-pipelines", pipeline_id, etag, timeout)

    def list_mcp_servers(self, project_id: str, *, timeout: Timeout = None) -> list[ConfigResource]:
        """List MCP server configurations in a project."""
        return self._list("/mcp-servers", ConfigResource, {"project_id": project_id}, timeout)

    def create_mcp_server(self, body: dict[str, Any], *, timeout: Timeout = None) -> CreateResult:
        """Create an MCP server configuration from its documented JSON body."""
        return self._create("/mcp-servers", body, timeout)

    def read_mcp_server(self, server_id: str, *, timeout: Timeout = None) -> ConfigResource:
        """Read an MCP server configuration by ID."""
        return self._read("/mcp-servers", server_id, ConfigResource, timeout)

    def update_mcp_server(
        self, server_id: str, body: dict[str, Any], *, etag: str, timeout: Timeout = None
    ) -> UpdateResult:
        """Update an MCP server configuration (``If-Match`` guarded)."""
        return self._update("/mcp-servers", server_id, body, etag, timeout)

    def delete_mcp_server(self, server_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete an MCP server configuration (``If-Match`` guarded)."""
        self._delete("/mcp-servers", server_id, etag, timeout)

    # -- capture pipelines (no update) --------------------------------------

    def list_capture_pipelines(
        self, project_id: str, *, full_fetch: bool = False, search: str | None = None, timeout: Timeout = None
    ) -> list[ConfigResource]:
        """List capture pipelines in a project."""
        params = {"project_id": project_id, "full_fetch": full_fetch, "search": search}
        return self._list("/capture-pipelines", ConfigResource, params, timeout)

    def create_capture_pipeline(self, body: dict[str, Any], *, timeout: Timeout = None) -> CreateResult:
        """Create a capture pipeline from its documented JSON body."""
        return self._create("/capture-pipelines", body, timeout)

    def read_capture_pipeline(self, pipeline_id: str, *, timeout: Timeout = None) -> ConfigResource:
        """Read a capture pipeline by ID."""
        return self._read("/capture-pipelines", pipeline_id, ConfigResource, timeout)

    def delete_capture_pipeline(self, pipeline_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete a capture pipeline (``If-Match`` guarded)."""
        self._delete("/capture-pipelines", pipeline_id, etag, timeout)

    def list_capture_pipeline_topics(
        self, project_id: str, *, full_fetch: bool = False, search: str | None = None, timeout: Timeout = None
    ) -> list[ConfigResource]:
        """List capture-pipeline topics in a project."""
        params = {"project_id": project_id, "full_fetch": full_fetch, "search": search}
        return self._list("/capture-pipeline-topics", ConfigResource, params, timeout)

    def create_capture_pipeline_topic(self, body: dict[str, Any], *, timeout: Timeout = None) -> CreateResult:
        """Create a capture-pipeline topic from its documented JSON body."""
        return self._create("/capture-pipeline-topics", body, timeout)

    def read_capture_pipeline_topic(self, topic_id: str, *, timeout: Timeout = None) -> ConfigResource:
        """Read a capture-pipeline topic by ID."""
        return self._read("/capture-pipeline-topics", topic_id, ConfigResource, timeout)

    def delete_capture_pipeline_topic(self, topic_id: str, *, etag: str, timeout: Timeout = None) -> None:
        """Delete a capture-pipeline topic (``If-Match`` guarded)."""
        self._delete("/capture-pipeline-topics", topic_id, etag, timeout)

    # -- data schema --------------------------------------------------------

    def rebuild_data_schema(self, project_id: str, *, timeout: Timeout = None) -> None:
        """Trigger a rebuild of the project's IKG data schema (``POST /data-schema/rebuild``).

        **Experimental**: this endpoint is live but not yet in the published spec.
        """
        self._send(RequestSpec("POST", "/data-schema/rebuild", json_body={"project_id": project_id}), timeout=timeout)
