"""Models for the AuthZEN authorization API (``/access/v1``).

Spec: https://openapi.indykite.com/v1/authzen.yaml - implements the OpenID
AuthZEN specification over IndyKite KBAC policies.
"""

from __future__ import annotations

from typing import Any, Self

from pydantic import model_validator

from indykite_sdk._core.models import IKModel, IKResponseModel

__all__ = [
    "Action",
    "ActionSearchResponse",
    "Context",
    "EvaluationItem",
    "EvaluationResponse",
    "EvaluationsResponse",
    "Node",
    "NodeType",
    "ResourceSearchResponse",
    "ResponseContext",
    "SubjectSearchResponse",
]


class Node(IKModel):
    """A subject or resource: graph node ``type`` (label) + ``id`` (external_id).

    Accepts a ``("Person", "ada")`` tuple or ``{"type": ..., "id": ...}`` dict
    anywhere a subject/resource is expected.
    """

    type: str
    id: str

    @model_validator(mode="before")
    @classmethod
    def _from_tuple(cls, value: Any) -> Any:
        if isinstance(value, (tuple, list)) and len(value) == 2:
            return {"type": value[0], "id": value[1]}
        return value


class NodeType(IKModel):
    """A bare node type, used to scope search results (e.g. all ``Car`` resources)."""

    type: str

    @model_validator(mode="before")
    @classmethod
    def _from_string(cls, value: Any) -> Any:
        if isinstance(value, str):
            return {"type": value}
        return value


class Action(IKModel):
    """A policy action, e.g. ``CAN_DRIVE``. Accepts a bare string too."""

    name: str

    @model_validator(mode="before")
    @classmethod
    def _from_string(cls, value: Any) -> Any:
        if isinstance(value, str):
            return {"name": value}
        return value


class Context(IKModel):
    """Per-request policy inputs.

    ``input_params`` feeds policy input parameters; ``policy_tags`` limits
    evaluation to policies carrying those tags.
    """

    input_params: dict[str, Any] | None = None
    policy_tags: list[str] | None = None


class EvaluationItem(IKModel):
    """One entry of a batch ``evaluations`` call; unset fields fall back to the request defaults."""

    subject: Node | None = None
    action: Action | None = None
    resource: Node | None = None
    context: Context | None = None

    @model_validator(mode="after")
    def _not_empty(self) -> Self:
        if self.subject is None and self.action is None and self.resource is None and self.context is None:
            raise ValueError("an evaluation item must override at least one of subject/action/resource/context")
        return self


class ResponseContext(IKResponseModel):
    """Optional decision context returned by the policy engine."""

    reason: str | None = None
    advice: list[dict[str, str]] | None = None


class EvaluationResponse(IKResponseModel):
    """A single authorization decision."""

    decision: bool = False
    context: ResponseContext | None = None


class EvaluationsResponse(IKResponseModel):
    """Ordered decisions of a batch evaluation - one per requested item."""

    evaluations: list[EvaluationResponse] = []

    @property
    def decisions(self) -> list[bool]:
        """The bare boolean decisions, in request order."""
        return [evaluation.decision for evaluation in self.evaluations]


class ActionSearchResponse(IKResponseModel):
    """Actions a subject may perform on a resource."""

    results: list[Action] = []

    @property
    def action_names(self) -> list[str]:
        """The bare action names, e.g. ``["CAN_DRIVE"]``."""
        return [action.name for action in self.results]


class ResourceSearchResponse(IKResponseModel):
    """Resources (type + id) a subject may perform an action on."""

    results: list[Node] = []


class SubjectSearchResponse(IKResponseModel):
    """Subjects (type + id) allowed to perform an action on a resource."""

    results: list[Node] = []
