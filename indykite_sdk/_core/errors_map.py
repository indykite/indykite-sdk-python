"""Map non-success HTTP responses to typed SDK exceptions.

Error bodies follow the platform shape ``{"message": "...", "errors": ["..."]}``
(e.g. 422 → ``{"message": "Unprocessable Entity", "errors": [...]}``).
"""

from __future__ import annotations

import httpx

from indykite_sdk.errors import (
    APIStatusError,
    AuthenticationError,
    BadRequestError,
    ConflictError,
    ETagMismatchError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    UnprocessableEntityError,
)

_STATUS_TO_ERROR: dict[int, type[APIStatusError]] = {
    400: BadRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    409: ConflictError,
    412: ETagMismatchError,
    422: UnprocessableEntityError,
    429: RateLimitError,
}

_HINTS: dict[int, dict[str, str]] = {
    401: {
        "app_agent": (
            "The X-IK-ClientKey token was rejected. Ensure INDYKITE_APPLICATION_CREDENTIALS holds the "
            "application-agent credential token (not a service-account credential) and that it has not expired. "
            "An 'insufficient API access level' message means the agent lacks the API permission this endpoint "
            "needs (e.g. Audit for /audit/v1, ReadAuthZConfigs for /access/v1/policies)."
        ),
        "service_account": (
            "The bearer token was rejected. Ensure INDYKITE_SERVICE_ACCOUNT_CREDENTIALS holds a service-account "
            "credential JSON with a valid 'token' and that it has not expired."
        ),
    },
    403: {
        "app_agent": (
            "The application agent is not allowed to access this resource. A project_id you passed must be the "
            "project the agent belongs to; the agent's API permissions (Audit, Authorization, Capture, ContXIQ, "
            "EntityMatching, ReadAuthZConfigs, ReadDataSchema) are managed in the IndyKite Hub."
        ),
        "service_account": "The service account is not allowed to manage this resource.",
    },
    404: {"*": "Check the resource ID and that it belongs to the project/organization of your credentials."},
    412: {"*": "The etag is stale: another change happened first. Re-read the resource and retry with its fresh etag."},
    429: {"*": "Rate limited. Wait and retry; the Retry-After header suggests how long."},
}


def raise_for_status(response: httpx.Response, *, auth_kind: str) -> None:
    """Raise the typed exception matching ``response`` (no-op on success)."""
    if response.is_success:
        return
    status = response.status_code
    message = response.reason_phrase or f"HTTP {status}"
    errors: list[str] = []
    try:
        body = response.json()
    except ValueError:
        body = None
    if isinstance(body, dict):
        if isinstance(body.get("message"), str):
            message = body["message"]
        if isinstance(body.get("errors"), list):
            errors = [str(e) for e in body["errors"]]

    error_cls = _STATUS_TO_ERROR.get(status)
    if error_cls is None:
        error_cls = InternalServerError if status >= 500 else APIStatusError

    hints = _HINTS.get(status, {})
    hint = hints.get(auth_kind) or hints.get("*")

    raise error_cls(
        message,
        status_code=status,
        method=response.request.method,
        url=str(response.request.url),
        errors=errors,
        hint=hint,
        response=response,
    )
