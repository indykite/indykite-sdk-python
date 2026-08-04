"""Asynchronous AuthZEN authorization client."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import httpx

from indykite_sdk._core.http import BaseAsyncClient
from indykite_sdk.authzen import _ops
from indykite_sdk.authzen.models import (
    ActionSearchResponse,
    EvaluationItem,
    EvaluationResponse,
    EvaluationsResponse,
    NodeType,
    ResourceSearchResponse,
    SubjectSearchResponse,
)

__all__ = ["AsyncAuthZENClient"]


class AsyncAuthZENClient(BaseAsyncClient):
    """Async variant of :class:`indykite_sdk.AuthZENClient` — same methods, ``await``-able.

    Example::

        from indykite_sdk import AsyncAuthZENClient

        async with AsyncAuthZENClient() as client:
            result = await client.evaluation(("Person", "ada"), "CAN_DRIVE", ("Car", "kitt"))
    """

    _api_prefix = "/access/v1"
    _auth_kind = "app_agent"

    async def evaluation(
        self,
        subject: _ops.NodeInput,
        action: _ops.ActionInput,
        resource: _ops.NodeInput,
        context: _ops.ContextInput = None,
        *,
        user_token: str | None = None,
        timeout: httpx.Timeout | float | None = None,
    ) -> EvaluationResponse:
        """Decide whether ``subject`` may perform ``action`` on ``resource`` (``POST /evaluation``)."""
        spec = _ops.evaluation_spec(subject, action, resource, context, user_token)
        return EvaluationResponse.model_validate((await self._send(spec, timeout=timeout)).json())

    async def evaluations(
        self,
        evaluations: Sequence[EvaluationItem | dict[str, Any]],
        *,
        subject: _ops.NodeInput | None = None,
        action: _ops.ActionInput | None = None,
        resource: _ops.NodeInput | None = None,
        context: _ops.ContextInput = None,
        user_token: str | None = None,
        timeout: httpx.Timeout | float | None = None,
    ) -> EvaluationsResponse:
        """Batch decisions in one call (``POST /evaluations``)."""
        spec = _ops.evaluations_spec(evaluations, subject, action, resource, context, user_token)
        return EvaluationsResponse.model_validate((await self._send(spec, timeout=timeout)).json())

    async def search_action(
        self,
        subject: _ops.NodeInput,
        resource: _ops.NodeInput,
        context: _ops.ContextInput = None,
        *,
        user_token: str | None = None,
        timeout: httpx.Timeout | float | None = None,
    ) -> ActionSearchResponse:
        """List the actions ``subject`` may perform on ``resource`` (``POST /search/action``)."""
        spec = _ops.search_action_spec(subject, resource, context, user_token)
        return ActionSearchResponse.model_validate((await self._send(spec, timeout=timeout)).json())

    async def search_resource(
        self,
        subject: _ops.NodeInput,
        action: _ops.ActionInput,
        resource_type: NodeType | dict[str, Any] | str,
        context: _ops.ContextInput = None,
        *,
        user_token: str | None = None,
        timeout: httpx.Timeout | float | None = None,
    ) -> ResourceSearchResponse:
        """List the resources of ``resource_type`` on which ``subject`` may perform ``action``."""
        spec = _ops.search_resource_spec(subject, action, resource_type, context, user_token)
        return ResourceSearchResponse.model_validate((await self._send(spec, timeout=timeout)).json())

    async def search_subject(
        self,
        resource: _ops.NodeInput,
        action: _ops.ActionInput,
        subject_type: NodeType | dict[str, Any] | str,
        context: _ops.ContextInput = None,
        *,
        user_token: str | None = None,
        timeout: httpx.Timeout | float | None = None,
    ) -> SubjectSearchResponse:
        """List the subjects of ``subject_type`` allowed to perform ``action`` on ``resource``."""
        spec = _ops.search_subject_spec(resource, action, subject_type, context, user_token)
        return SubjectSearchResponse.model_validate((await self._send(spec, timeout=timeout)).json())
