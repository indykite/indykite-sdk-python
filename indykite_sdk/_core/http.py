"""Sync and async base clients shared by every per-API client.

Subclasses only declare their API path prefix and credential kind; all
transport concerns (auth, base URL, timeouts, retries, error mapping) live
here so the twelve public clients behave identically.
"""

from __future__ import annotations

import asyncio
import platform
import time
from typing import TYPE_CHECKING, Any, ClassVar, Self

import httpx

from indykite_sdk._core.auth import AppAgentAuth, ServiceAccountAuth
from indykite_sdk._core.credentials import CredentialKind, Credentials
from indykite_sdk._core.endpoints import resolve_base_url
from indykite_sdk._core.errors_map import raise_for_status
from indykite_sdk._core.retry import DEFAULT_RETRY, RetryConfig, retry_delay, should_retry
from indykite_sdk.errors import IndyKiteConnectionError
from indykite_sdk.version import __version__

if TYPE_CHECKING:
    from indykite_sdk._core.ops import RequestSpec

_CONNECT_RETRIES = 2

USER_AGENT = f"indykite-sdk-python/{__version__} (python/{platform.python_version()}; httpx/{httpx.__version__})"

DEFAULT_TIMEOUT = httpx.Timeout(connect=5.0, read=30.0, write=30.0, pool=5.0)


class _ClientBase:
    """Configuration shared by the sync and async variants."""

    #: Per-API path prefix, e.g. ``/capture/v1``.
    _api_prefix: ClassVar[str]
    #: Which credential kind (and therefore auth header) this API uses.
    _auth_kind: ClassVar[CredentialKind]

    def __init__(
        self,
        credentials: Credentials | dict[str, Any] | str | None = None,
        *,
        base_url: str | None = None,
        region: str | None = None,
        timeout: httpx.Timeout | float | None = None,
        retries: RetryConfig | None = DEFAULT_RETRY,
        http_client: httpx.Client | httpx.AsyncClient | None = None,
    ) -> None:
        """Configure the client.

        Args:
            credentials: A :class:`~indykite_sdk.Credentials`, or ``None`` to
                load from the standard environment variables for this API's
                credential kind. Data-plane clients also accept the raw
                application-agent credential token string; ``ConfigClient``
                accepts the service-account credential JSON string/dict.
            base_url: Full API host override, e.g. ``https://api.dev.indykite.xyz``.
            region: ``"eu"`` (default) or ``"us"``; ignored when ``base_url``
                or ``INDYKITE_BASE_URL`` is set.
            timeout: Request timeout; a float applies to all timeout phases.
            retries: Retry policy for idempotent requests; ``None`` disables retries.
            http_client: A preconfigured httpx client (proxies, instrumentation,
                custom transports). The SDK still applies auth, base URL and
                default headers to it.
        """
        if isinstance(credentials, Credentials):
            self._credentials = credentials
        elif isinstance(credentials, str) and self._auth_kind == "app_agent":
            # The App Agent credential is the raw token itself, not JSON.
            self._credentials = Credentials.from_token(credentials)
        elif credentials is not None:
            self._credentials = Credentials.from_json(credentials)
        else:
            self._credentials = Credentials.from_env(self._auth_kind)
        host = resolve_base_url(base_url=base_url, credentials=self._credentials, region=region)
        self._base_url = f"{host}{self._api_prefix}"
        self._auth = (
            ServiceAccountAuth(self._credentials)
            if self._auth_kind == "service_account"
            else AppAgentAuth(self._credentials)
        )
        self._timeout = timeout if timeout is not None else DEFAULT_TIMEOUT
        self._retries = retries
        self._provided_client = http_client

    @property
    def credentials(self) -> Credentials:
        """The credentials this client authenticates with."""
        return self._credentials

    @property
    def base_url(self) -> str:
        """The resolved API base URL, including the API path prefix."""
        return self._base_url

    @staticmethod
    def _default_headers() -> dict[str, str]:
        return {"User-Agent": USER_AGENT, "Accept": "application/json"}


class BaseSyncClient(_ClientBase):
    """Blocking client; use as a context manager or call :meth:`close`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        client = self._provided_client
        if client is None:
            client = httpx.Client(transport=httpx.HTTPTransport(retries=_CONNECT_RETRIES))
        elif not isinstance(client, httpx.Client):
            raise TypeError("http_client must be an httpx.Client for sync clients")
        client.auth = self._auth
        client.base_url = httpx.URL(self._base_url)
        client.headers.update(self._default_headers())
        client.timeout = self._timeout if isinstance(self._timeout, httpx.Timeout) else httpx.Timeout(self._timeout)
        self._client = client

    def close(self) -> None:
        """Release the underlying HTTP connection pool."""
        self._client.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def _send(self, spec: RequestSpec, *, timeout: httpx.Timeout | float | None = None) -> httpx.Response:
        attempt = 1
        while True:
            try:
                response = self._client.request(
                    spec.method,
                    # An empty path must hit the API prefix exactly, without a trailing slash.
                    spec.path or self._base_url,
                    params=spec.params or None,
                    json=spec.json_body,
                    headers=spec.headers or None,
                    timeout=timeout if timeout is not None else httpx.USE_CLIENT_DEFAULT,
                )
            except httpx.TransportError as exc:
                raise IndyKiteConnectionError(f"Could not reach {self._base_url}: {exc}") from exc
            if response.is_success:
                return response
            retries = self._retries
            if retries is not None and should_retry(retries, spec.method, response.status_code, attempt):
                time.sleep(retry_delay(retries, attempt, response.headers.get("Retry-After")))
                attempt += 1
                continue
            raise_for_status(response, auth_kind=self._auth_kind)
            return response  # pragma: no cover - raise_for_status always raises here


class BaseAsyncClient(_ClientBase):
    """Asyncio client; use ``async with`` or call :meth:`aclose`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        client = self._provided_client
        if client is None:
            client = httpx.AsyncClient(transport=httpx.AsyncHTTPTransport(retries=_CONNECT_RETRIES))
        elif not isinstance(client, httpx.AsyncClient):
            raise TypeError("http_client must be an httpx.AsyncClient for async clients")
        client.auth = self._auth
        client.base_url = httpx.URL(self._base_url)
        client.headers.update(self._default_headers())
        client.timeout = self._timeout if isinstance(self._timeout, httpx.Timeout) else httpx.Timeout(self._timeout)
        self._client = client

    async def aclose(self) -> None:
        """Release the underlying HTTP connection pool."""
        await self._client.aclose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.aclose()

    async def _send(self, spec: RequestSpec, *, timeout: httpx.Timeout | float | None = None) -> httpx.Response:
        attempt = 1
        while True:
            try:
                response = await self._client.request(
                    spec.method,
                    # An empty path must hit the API prefix exactly, without a trailing slash.
                    spec.path or self._base_url,
                    params=spec.params or None,
                    json=spec.json_body,
                    headers=spec.headers or None,
                    timeout=timeout if timeout is not None else httpx.USE_CLIENT_DEFAULT,
                )
            except httpx.TransportError as exc:
                raise IndyKiteConnectionError(f"Could not reach {self._base_url}: {exc}") from exc
            if response.is_success:
                return response
            retries = self._retries
            if retries is not None and should_retry(retries, spec.method, response.status_code, attempt):
                await asyncio.sleep(retry_delay(retries, attempt, response.headers.get("Retry-After")))
                attempt += 1
                continue
            raise_for_status(response, auth_kind=self._auth_kind)
            return response  # pragma: no cover - raise_for_status always raises here
