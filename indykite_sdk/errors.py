"""Public exception hierarchy for the IndyKite SDK.

Every SDK operation raises on failure - no method ever returns ``None`` to
signal an error. Catch :class:`IndyKiteError` to handle anything raised by the
SDK, or a specific subclass for targeted handling::

    from indykite_sdk import CaptureClient, NotFoundError

    with CaptureClient() as client:
        try:
            client.delete_nodes([{"external_id": "millicent", "type": "Person"}])
        except NotFoundError as exc:
            print(exc)  # includes method, URL, status and an actionable hint
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import httpx

__all__ = [
    "APIStatusError",
    "AuthenticationError",
    "BadRequestError",
    "ChunkedCaptureError",
    "ConflictError",
    "CredentialsError",
    "ETagMismatchError",
    "IndyKiteConnectionError",
    "IndyKiteError",
    "InternalServerError",
    "NotFoundError",
    "PermissionDeniedError",
    "PipelineTimeoutError",
    "RateLimitError",
    "RequestValidationError",
]


class IndyKiteError(Exception):
    """Base class for every exception raised by the IndyKite SDK."""


class CredentialsError(IndyKiteError):
    """Credentials are missing, unreadable, or not usable for the requested API."""


class IndyKiteConnectionError(IndyKiteError):
    """The API could not be reached (DNS failure, connect timeout, TLS error, ...).

    The underlying :mod:`httpx` transport error is available as ``__cause__``.
    """


class RequestValidationError(IndyKiteError, ValueError):
    """The request is invalid and was rejected client-side, before any network call.

    Raised for example when a capture batch exceeds 250 items or a payload
    fails model validation. Fix the input; retrying will not help.
    """


class APIStatusError(IndyKiteError):
    """The API answered with a non-success HTTP status.

    Attributes:
        status_code: HTTP status code of the response.
        message: The ``message`` field of the error body (or raw text).
        errors: The ``errors`` list of the error body, if present.
        method: HTTP method of the failed request.
        url: Full URL of the failed request.
        hint: One-line actionable suggestion for fixing the failure.
        response: The raw ``httpx.Response``.
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        method: str,
        url: str,
        errors: list[str] | None = None,
        hint: str | None = None,
        response: httpx.Response | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.method = method
        self.url = url
        self.errors = errors or []
        self.hint = hint
        self.response = response

    def __str__(self) -> str:
        text = f"{self.method} {self.url} returned {self.status_code}: {self.message}"
        if self.errors:
            text += f" ({'; '.join(self.errors)})"
        if self.hint:
            text += f" Hint: {self.hint}"
        return text


class BadRequestError(APIStatusError):
    """HTTP 400 - the API rejected the request payload or parameters."""


class AuthenticationError(APIStatusError):
    """HTTP 401 - the credential token was missing, expired, or rejected."""


class PermissionDeniedError(APIStatusError):
    """HTTP 403 - the credential is valid but lacks permission for this operation."""


class NotFoundError(APIStatusError):
    """HTTP 404 - the resource does not exist (or is outside the credential's scope)."""


class ConflictError(APIStatusError):
    """HTTP 409 - the request conflicts with the current state (e.g. duplicate name)."""


class ETagMismatchError(APIStatusError):
    """HTTP 412 - the ``If-Match`` etag is stale; re-read the resource and retry."""


class RateLimitError(APIStatusError):
    """HTTP 429 - too many requests.

    ``retry_after`` exposes the ``Retry-After`` response header in seconds when
    the API provided one.
    """

    @property
    def retry_after(self) -> float | None:
        """The ``Retry-After`` response header in seconds, when the API sent one."""
        if self.response is None:
            return None
        value = self.response.headers.get("Retry-After")
        try:
            return float(value) if value is not None else None
        except ValueError:
            return None


class InternalServerError(APIStatusError):
    """HTTP 5xx - the API failed internally; safe to retry idempotent calls."""


class ChunkedCaptureError(IndyKiteError):
    """An ``auto_chunk`` capture call failed partway through.

    Attributes:
        completed: Results of the chunks that succeeded before the failure,
            in request order.
        failed_at: Index (0-based, in items) of the first item of the chunk
            that failed.

    The failure that stopped the run is available as ``__cause__``.
    """

    def __init__(self, message: str, *, completed: list[Any], failed_at: int) -> None:
        super().__init__(message)
        self.completed = completed
        self.failed_at = failed_at


class PipelineTimeoutError(IndyKiteError, TimeoutError):
    """``wait_for_completion`` gave up before the pipeline reached a final state."""
