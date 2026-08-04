"""Sans-IO request description shared by sync and async clients.

Every SDK operation is expressed once as a :class:`RequestSpec`; the sync and
async base clients only differ in how they send it. This keeps the two client
variants guaranteed-identical.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RequestSpec:
    """A fully-described API request, independent of the HTTP client used."""

    method: str
    path: str
    params: dict[str, Any] = field(default_factory=dict)
    json_body: Any = None
    headers: dict[str, str] = field(default_factory=dict)


def user_token_headers(user_token: str | None) -> dict[str, str]:
    """Headers for an optional end-user access token on AuthZEN/ContX IQ calls.

    The end-user token rides in ``Authorization: Bearer`` *alongside* the
    application-agent ``X-IK-ClientKey`` header.
    """
    if not user_token:
        return {}
    return {"Authorization": f"Bearer {user_token}"}
