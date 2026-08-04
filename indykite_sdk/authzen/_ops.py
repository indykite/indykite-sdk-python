"""Sans-IO request building shared by the sync and async AuthZEN clients."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from pydantic import ValidationError

from indykite_sdk._core.models import IKModel
from indykite_sdk._core.ops import RequestSpec, user_token_headers
from indykite_sdk.authzen.models import Action, Context, EvaluationItem, Node, NodeType
from indykite_sdk.errors import RequestValidationError

NodeInput = Node | dict[str, Any] | tuple[str, str]
ActionInput = Action | dict[str, Any] | str
ContextInput = Context | dict[str, Any] | None


def _coerce[ModelT: IKModel](value: Any, model_cls: type[ModelT], what: str) -> ModelT:
    try:
        return value if isinstance(value, model_cls) else model_cls.model_validate(value)
    except ValidationError as exc:
        raise RequestValidationError(f"Invalid {what}: {exc}") from exc


def _context_body(context: ContextInput) -> dict[str, Any] | None:
    if context is None:
        return None
    return _coerce(context, Context, "context").to_wire() or None


def evaluation_spec(
    subject: NodeInput, action: ActionInput, resource: NodeInput, context: ContextInput, user_token: str | None
) -> RequestSpec:
    """Build a single-decision request body."""
    body: dict[str, Any] = {
        "subject": _coerce(subject, Node, "subject").to_wire(),
        "action": _coerce(action, Action, "action").to_wire(),
        "resource": _coerce(resource, Node, "resource").to_wire(),
    }
    if (context_body := _context_body(context)) is not None:
        body["context"] = context_body
    return RequestSpec("POST", "/evaluation", json_body=body, headers=user_token_headers(user_token))


def evaluations_spec(
    evaluations: Sequence[EvaluationItem | dict[str, Any]],
    subject: NodeInput | None,
    action: ActionInput | None,
    resource: NodeInput | None,
    context: ContextInput,
    user_token: str | None,
) -> RequestSpec:
    """Build a batch-decision request body (top-level fields act as defaults)."""
    if not evaluations:
        raise RequestValidationError("At least one evaluation item is required.")
    body: dict[str, Any] = {
        "evaluations": [
            _coerce(item, EvaluationItem, f"evaluation item at index {index}").to_wire()
            for index, item in enumerate(evaluations)
        ]
    }
    if subject is not None:
        body["subject"] = _coerce(subject, Node, "subject").to_wire()
    if action is not None:
        body["action"] = _coerce(action, Action, "action").to_wire()
    if resource is not None:
        body["resource"] = _coerce(resource, Node, "resource").to_wire()
    if (context_body := _context_body(context)) is not None:
        body["context"] = context_body
    return RequestSpec("POST", "/evaluations", json_body=body, headers=user_token_headers(user_token))


def search_action_spec(
    subject: NodeInput, resource: NodeInput, context: ContextInput, user_token: str | None
) -> RequestSpec:
    """Build a search/action request body."""
    body: dict[str, Any] = {
        "subject": _coerce(subject, Node, "subject").to_wire(),
        "resource": _coerce(resource, Node, "resource").to_wire(),
    }
    if (context_body := _context_body(context)) is not None:
        body["context"] = context_body
    return RequestSpec("POST", "/search/action", json_body=body, headers=user_token_headers(user_token))


def search_resource_spec(
    subject: NodeInput,
    action: ActionInput,
    resource_type: NodeType | dict[str, Any] | str,
    context: ContextInput,
    user_token: str | None,
) -> RequestSpec:
    """Build a search/resource request body."""
    body: dict[str, Any] = {
        "subject": _coerce(subject, Node, "subject").to_wire(),
        "action": _coerce(action, Action, "action").to_wire(),
        "resource": _coerce(resource_type, NodeType, "resource type").to_wire(),
    }
    if (context_body := _context_body(context)) is not None:
        body["context"] = context_body
    return RequestSpec("POST", "/search/resource", json_body=body, headers=user_token_headers(user_token))


def search_subject_spec(
    resource: NodeInput,
    action: ActionInput,
    subject_type: NodeType | dict[str, Any] | str,
    context: ContextInput,
    user_token: str | None,
) -> RequestSpec:
    """Build a search/subject request body."""
    body: dict[str, Any] = {
        "subject": _coerce(subject_type, NodeType, "subject type").to_wire(),
        "action": _coerce(action, Action, "action").to_wire(),
        "resource": _coerce(resource, Node, "resource").to_wire(),
    }
    if (context_body := _context_body(context)) is not None:
        body["context"] = context_body
    return RequestSpec("POST", "/search/subject", json_body=body, headers=user_token_headers(user_token))
