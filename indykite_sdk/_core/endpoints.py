"""Base-URL resolution for the IndyKite REST APIs.

Precedence (highest wins), mirroring the Go SDK's
``WithBaseURL > WithRegion > credential base URL``:

1. ``base_url=`` constructor argument (e.g. ``https://api.dev.indykite.xyz``)
2. ``INDYKITE_BASE_URL`` environment variable
3. ``region=`` argument or ``INDYKITE_REGION`` environment variable
   (``eu`` or ``us``) → ``https://{region}.api.indykite.com``
4. The credential's ``baseUrl`` (or ``endpoint``) field, when it is an
   HTTP(S) URL (other values are ignored)
5. Default: the ``eu`` production region
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from indykite_sdk.errors import CredentialsError

if TYPE_CHECKING:
    from indykite_sdk._core.credentials import Credentials

REGIONS = ("eu", "us")
DEFAULT_REGION = "eu"


def _region_url(region: str) -> str:
    if region not in REGIONS:
        raise CredentialsError(f"Unknown IndyKite region {region!r}; expected one of {REGIONS}.")
    return f"https://{region}.api.indykite.com"


def resolve_base_url(
    *,
    base_url: str | None = None,
    credentials: Credentials | None = None,
    region: str | None = None,
) -> str:
    """Resolve the API host base URL (without any per-API path prefix)."""
    resolved = base_url or os.environ.get("INDYKITE_BASE_URL")
    if not resolved:
        env_region = os.environ.get("INDYKITE_REGION")
        if region or env_region:
            resolved = _region_url(region or env_region or "")
    if not resolved and credentials is not None:
        for candidate in (credentials.base_url, credentials.endpoint):
            if candidate and candidate.startswith(("http://", "https://")):
                resolved = candidate
                break
    if not resolved:
        resolved = _region_url(DEFAULT_REGION)
    if not resolved.startswith(("http://", "https://")):
        raise CredentialsError(f"Base URL {resolved!r} must start with http:// or https://.")
    return resolved.rstrip("/")
