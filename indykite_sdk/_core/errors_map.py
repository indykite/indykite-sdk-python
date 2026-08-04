"""Map non-success HTTP responses to typed SDK exceptions.

Error bodies follow the platform shape ``{"message": "...", "errors": ["..."]}``
(e.g. 412 → ``{"message": "Precondition Failed", "errors": [...]}``).
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
)

_STATUS_TO_ERROR: dict[int, type[APIStatusError]] = {
    400: BadRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    409: ConflictError,
    412: ETagMismatchError,
    429: RateLimitError,
}

_HINTS: dict[int, dict[str, str]] = {
    401: {
        "app_agent": (
            "The X-IK-ClientKey token was rejected. Ensure INDYKITE_APPLICATION_CREDENTIALS holds an "
            "application-agent credential JSON (not a service-account one) and that it has not expired."
        ),
        "service_account": (
            "The bearer token was rejected. Ensure INDYKITE_SERVICE_ACCOUNT_CREDENTIALS holds a service-account "
            "credential JSON with a valid 'token' and that it has not expired."
        ),
    },
    403: {
        "app_agent": (
            "The application agent lacks the required API permission. Check its apiPermissions "
            "(e.g. Capture, Authorization, ContXIQ, EntityMatching) in the IndyKite Hub."
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
