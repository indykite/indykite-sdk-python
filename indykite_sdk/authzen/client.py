"""Synchronous AuthZEN authorization client."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import httpx

from indykite_sdk._core.http import BaseSyncClient
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

__all__ = ["AuthZENClient"]


class AuthZENClient(BaseSyncClient):
    """Make KBAC authorization decisions via the AuthZEN API (``/access/v1``).

    Authenticates with the raw **application-agent credential token**
    (``INDYKITE_APPLICATION_CREDENTIALS[_FILE]``) sent as ``X-IK-ClientKey``.
    Every method accepts an optional ``user_token`` - a third-party end-user
    access token forwarded as ``Authorization: Bearer`` so the decision runs
    in that user's context (requires a Token Introspect configuration).

    Example::

        from indykite_sdk import AuthZENClient

        with AuthZENClient() as client:
            if client.evaluation(("Person", "ada"), "CAN_DRIVE", ("Car", "kitt")).decision:
                print("ada may drive kitt")
    """

    _api_prefix = "/access/v1"
    _auth_kind = "app_agent"

    def evaluation(
        self,
        subject: _ops.NodeInput,
        action: _ops.ActionInput,
        resource: _ops.NodeInput,
        context: _ops.ContextInput = None,
        *,
        user_token: str | None = None,
        timeout: httpx.Timeout | float | None = None,
    ) -> EvaluationResponse:
        """Decide whether ``subject`` may perform ``action`` on ``resource`` (``POST /evaluation``).

        Args:
            subject: ``("Person", "ada")``, ``{"type": "Person", "id": "ada"}``, or a ``Node``.
            action: ``"CAN_DRIVE"``, ``{"name": ...}``, or an ``Action``.
            resource: same forms as ``subject``.
            context: optional ``{"input_params": {...}, "policy_tags": [...]}``.
        """
        spec = _ops.evaluation_spec(subject, action, resource, context, user_token)
        return EvaluationResponse.model_validate(self._send(spec, timeout=timeout).json())

    def evaluations(
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
        """Batch decisions in one call (``POST /evaluations``).

        Top-level ``subject``/``action``/``resource``/``context`` act as
        defaults; each item overrides any of them. Results come back in
        request order (``response.decisions``).
        """
        spec = _ops.evaluations_spec(evaluations, subject, action, resource, context, user_token)
        return EvaluationsResponse.model_validate(self._send(spec, timeout=timeout).json())

    def search_action(
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
        return ActionSearchResponse.model_validate(self._send(spec, timeout=timeout).json())

    def search_resource(
        self,
        subject: _ops.NodeInput,
        action: _ops.ActionInput,
        resource_type: NodeType | dict[str, Any] | str,
        context: _ops.ContextInput = None,
        *,
        user_token: str | None = None,
        timeout: httpx.Timeout | float | None = None,
    ) -> ResourceSearchResponse:
        """List the resources of ``resource_type`` on which ``subject`` may perform ``action``.

        (``POST /search/resource``) - e.g. "which Cars can ada drive?"::

            client.search_resource(("Person", "ada"), "CAN_DRIVE", "Car")
        """
        spec = _ops.search_resource_spec(subject, action, resource_type, context, user_token)
        return ResourceSearchResponse.model_validate(self._send(spec, timeout=timeout).json())

    def search_subject(
        self,
        resource: _ops.NodeInput,
        action: _ops.ActionInput,
        subject_type: NodeType | dict[str, Any] | str,
        context: _ops.ContextInput = None,
        *,
        user_token: str | None = None,
        timeout: httpx.Timeout | float | None = None,
    ) -> SubjectSearchResponse:
        """List the subjects of ``subject_type`` allowed to perform ``action`` on ``resource``.

        (``POST /search/subject``) - e.g. "who can drive kitt?"::

            client.search_subject(("Car", "kitt"), "CAN_DRIVE", "Person")
        """
        spec = _ops.search_subject_spec(resource, action, subject_type, context, user_token)
        return SubjectSearchResponse.model_validate(self._send(spec, timeout=timeout).json())
