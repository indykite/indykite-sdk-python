"""Typed models for the core Config API resources.

Field names match the wire format (snake_case) of
https://openapi.indykite.com/api-documentation-config.
"""

from __future__ import annotations

from typing import Any, ClassVar, Literal

from indykite_sdk._core.credentials import Credentials
from indykite_sdk.config.models.common import CreateResult, _ETagged
from indykite_sdk.errors import CredentialsError

__all__ = [
    "ApiPermission",
    "Application",
    "ApplicationAgent",
    "ApplicationAgentCredential",
    "ApplicationAgentCredentialCreated",
    "AuthorizationPolicy",
    "ConfigStatus",
    "KnowledgeQuery",
    "Organization",
    "Project",
    "ServiceAccount",
    "ServiceAccountCredential",
    "ServiceAccountCredentialCreated",
    "ServiceAccountRole",
]

#: API permission grantable to an application agent.
ApiPermission = Literal["Authorization", "Capture", "ContXIQ", "EntityMatching", "IKGRead", "ReadDataSchema"]

#: Lifecycle status of policies and knowledge queries.
ConfigStatus = Literal["ACTIVE", "INACTIVE", "DRAFT"]

#: Role of a service account.
ServiceAccountRole = Literal["all_editor", "all_viewer"]


class _AuditedResource(_ETagged):
    id: str | None = None
    name: str | None = None
    display_name: str | None = None
    description: str | None = None
    create_time: str | None = None
    created_by: str | None = None
    update_time: str | None = None
    updated_by: str | None = None


class Organization(_AuditedResource):
    """The organization the service account belongs to."""


class Project(_AuditedResource):
    """A project with its own IKG instance."""

    organization_id: str | None = None
    project_id: str | None = None
    region: str | None = None
    replica_region: str | None = None
    ikg_size: str | None = None
    ikg_status: str | None = None
    db_connection: dict[str, Any] | None = None


class Application(_AuditedResource):
    """An application under a project."""

    organization_id: str | None = None
    project_id: str | None = None


class ApplicationAgent(_AuditedResource):
    """An application agent - the identity your workload authenticates as."""

    organization_id: str | None = None
    project_id: str | None = None
    application_id: str | None = None
    api_permissions: list[str] | None = None


class _CredentialCreated(CreateResult):
    """Base for credential-create responses, which include the one-time credential config."""

    display_name: str | None = None
    expire_time: str | None = None
    kid: str | None = None

    _config_field: ClassVar[str] = ""

    def _config(self) -> dict[str, Any]:
        config = (self.model_extra or {}).get(self._config_field)
        if not isinstance(config, dict):
            raise CredentialsError(
                f"The create response has no '{self._config_field}' object; "
                "the credential JSON is only returned once, at creation."
            )
        return config

    def as_credentials(self) -> Credentials:
        """The newly created credential as ready-to-use :class:`~indykite_sdk.Credentials`.

        Only available on the create response - the platform never returns the
        credential JSON again.
        """
        return Credentials.from_json(self._config())


class ApplicationAgentCredentialCreated(_CredentialCreated):
    """Create response for an application-agent credential; keep it safe, it is shown once."""

    application_agent_id: str | None = None
    _config_field = "application_agent_config"


class ServiceAccountCredentialCreated(_CredentialCreated):
    """Create response for a service-account credential; keep it safe, it is shown once."""

    service_account_id: str | None = None
    _config_field = "service_account_config"


class ApplicationAgentCredential(_ETagged):
    """Metadata of an application-agent credential (the secret itself is never re-readable)."""

    id: str | None = None
    display_name: str | None = None
    kid: str | None = None
    application_agent_id: str | None = None
    application_id: str | None = None
    organization_id: str | None = None
    project_id: str | None = None
    create_time: str | None = None
    created_by: str | None = None
    expire_time: str | None = None


class ServiceAccount(_AuditedResource):
    """A service account for managing configuration at the organization level."""

    organization_id: str | None = None
    role: str | None = None


class ServiceAccountCredential(_ETagged):
    """Metadata of a service-account credential (the secret itself is never re-readable)."""

    id: str | None = None
    display_name: str | None = None
    kid: str | None = None
    service_account_id: str | None = None
    organization_id: str | None = None
    create_time: str | None = None
    created_by: str | None = None
    expire_time: str | None = None


class AuthorizationPolicy(_AuditedResource):
    """A KBAC or CIQ authorization policy; ``policy`` is the JSON policy document as a string."""

    organization_id: str | None = None
    project_id: str | None = None
    policy: str | None = None
    status: str | None = None
    tags: list[str] | None = None


class KnowledgeQuery(_AuditedResource):
    """A knowledge query executed via ContX IQ; ``query`` is the JSON query document as a string."""

    organization_id: str | None = None
    project_id: str | None = None
    query: str | None = None
    status: str | None = None
    policy_id: str | None = None
