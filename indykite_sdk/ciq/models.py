"""Models for the ContX IQ API (``/contx-iq/v1``).

Spec: https://openapi.indykite.com/v1/ciq.yaml
"""

from __future__ import annotations

from typing import Any

from indykite_sdk._core.models import IKResponseModel

__all__ = ["ExecuteRecord", "ExecuteResponse"]


class ExecuteRecord(IKResponseModel):
    """One result row of a knowledge-query execution.

    Keys are query-defined, e.g. ``nodes["car.property.model"]`` or
    ``aggregate_values["count(person)"]``.
    """

    nodes: dict[str, Any] = {}
    relationships: dict[str, Any] = {}
    aggregate_values: dict[str, Any] = {}


class ExecuteResponse(IKResponseModel):
    """The result set of a knowledge-query execution."""

    data: list[ExecuteRecord] = []
