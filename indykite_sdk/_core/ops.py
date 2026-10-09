"""Sans-IO request description shared by sync and async clients.

Every SDK operation is expressed once as a :class:`RequestSpec`; the sync and
async base clients only differ in how they send it. This keeps the two client
variants guaranteed-identical.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from indykite_sdk.errors import RequestValidationError


@dataclass(slots=True)
class RequestSpec:
    """A fully-described API request, independent of the HTTP client used."""

    method: str
    path: str
    params: dict[str, Any] = field(default_factory=dict)
    json_body: Any = None
    headers: dict[str, str] = field(default_factory=dict)


def user_token_headers(user_token: str | None, delegated_token: str | None = None) -> dict[str, str]:
    """Headers for the optional request tokens on AuthZEN/ContX IQ calls.

    Both ride *alongside* the application-agent ``X-IK-ClientKey`` header, and
    the platform publishes their claim sets to policy conditions under the
    reserved parameter names ``token`` and ``ik_token``:

    - the end-user access token in ``Authorization: Bearer``; its claims are
      readable by policies as ``$token`` (e.g. ``$token.sub``);
    - the IndyKite delegated token in ``X-IK-Token``; its claims, including
      the RFC 8693 ``act`` delegation chain, are readable as ``$ik_token``
      (e.g. ``$ik_token.act.sub``).

    The delegated token is only accepted together with the end-user token.
    """
    if delegated_token and not user_token:
        raise RequestValidationError("delegated_token requires user_token: X-IK-Token is sent with the end-user token.")
    headers: dict[str, str] = {}
    if user_token:
        headers["Authorization"] = f"Bearer {user_token}"
    if delegated_token:
        headers["X-IK-Token"] = delegated_token
    return headers
