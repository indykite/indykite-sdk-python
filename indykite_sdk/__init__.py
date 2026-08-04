"""IndyKite Python SDK - REST clients for the IndyKite platform APIs.

Quickstart::

    from indykite_sdk import AuthZENClient

    with AuthZENClient() as client:  # reads INDYKITE_APPLICATION_CREDENTIALS[_FILE]
        result = client.evaluation(
            subject={"type": "Person", "id": "ada"},
            action={"name": "CAN_DRIVE"},
            resource={"type": "Car", "id": "kitt"},
        )
        print(result.decision)

Each platform API has a sync and an async client. Config API clients use
service-account credentials; all others use application-agent credentials.
"""

from indykite_sdk._core.credentials import Credentials
from indykite_sdk._core.retry import RetryConfig
from indykite_sdk.authzen import AsyncAuthZENClient, AuthZENClient
from indykite_sdk.capture import AsyncCaptureClient, CaptureClient
from indykite_sdk.ciq import AsyncCIQClient, CIQClient
from indykite_sdk.config import AsyncConfigClient, ConfigClient
from indykite_sdk.data_schema import AsyncDataSchemaClient, DataSchemaClient
from indykite_sdk.entity_matching import AsyncEntityMatchingClient, EntityMatchingClient
from indykite_sdk.errors import (
    APIStatusError,
    AuthenticationError,
    BadRequestError,
    ChunkedCaptureError,
    ConflictError,
    CredentialsError,
    ETagMismatchError,
    IndyKiteConnectionError,
    IndyKiteError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    PipelineTimeoutError,
    RateLimitError,
    RequestValidationError,
)
from indykite_sdk.version import __version__

__all__ = [
    "APIStatusError",
    "__version__",
    "AsyncAuthZENClient",
    "AsyncCIQClient",
    "AsyncCaptureClient",
    "AsyncConfigClient",
    "AsyncDataSchemaClient",
    "AsyncEntityMatchingClient",
    "AuthZENClient",
    "AuthenticationError",
    "BadRequestError",
    "CIQClient",
    "CaptureClient",
    "ConfigClient",
    "ChunkedCaptureError",
    "ConflictError",
    "Credentials",
    "CredentialsError",
    "DataSchemaClient",
    "ETagMismatchError",
    "EntityMatchingClient",
    "IndyKiteConnectionError",
    "IndyKiteError",
    "InternalServerError",
    "NotFoundError",
    "PermissionDeniedError",
    "PipelineTimeoutError",
    "RateLimitError",
    "RequestValidationError",
    "RetryConfig",
]
