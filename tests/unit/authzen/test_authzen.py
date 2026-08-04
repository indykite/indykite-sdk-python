"""AuthZEN client: request shapes, convenience inputs, user tokens, responses."""

from __future__ import annotations

import pytest

from indykite_sdk import AsyncAuthZENClient, AuthZENClient, RequestValidationError
from indykite_sdk.authzen import Context, EvaluationItem, Node
from tests.unit.conftest import sent_json


def test_evaluation_body_and_decision(make_client, mock_api) -> None:
    """Evaluation body and decision."""
    mock_api.respond({"decision": True})
    client = make_client(AuthZENClient)
    result = client.evaluation(
        subject={"type": "Person", "id": "ada"},
        action={"name": "CAN_DRIVE"},
        resource={"type": "Car", "id": "kitt"},
    )
    assert result.decision is True
    assert mock_api.last.url.path == "/access/v1/evaluation"
    assert sent_json(mock_api.last) == {
        "subject": {"type": "Person", "id": "ada"},
        "action": {"name": "CAN_DRIVE"},
        "resource": {"type": "Car", "id": "kitt"},
    }


def test_evaluation_convenience_inputs(make_client, mock_api) -> None:
    """Evaluation convenience inputs."""
    client = make_client(AuthZENClient)
    client.evaluation(("Person", "ada"), "CAN_DRIVE", ("Car", "kitt"))
    assert sent_json(mock_api.last) == {
        "subject": {"type": "Person", "id": "ada"},
        "action": {"name": "CAN_DRIVE"},
        "resource": {"type": "Car", "id": "kitt"},
    }


def test_evaluation_context_and_user_token(make_client, mock_api) -> None:
    """Evaluation context and user token."""
    client = make_client(AuthZENClient)
    client.evaluation(
        ("Person", "ada"),
        "CAN_DRIVE",
        ("Car", "kitt"),
        context={"input_params": {"budget": 100}, "policy_tags": ["fleet"]},
        user_token="user-jwt",
    )
    body = sent_json(mock_api.last)
    assert body["context"] == {"input_params": {"budget": 100}, "policy_tags": ["fleet"]}
    assert mock_api.last.headers["Authorization"] == "Bearer user-jwt"
    assert mock_api.last.headers["X-IK-ClientKey"] == "app-agent-token-value"


def test_evaluation_default_decision_false(make_client, mock_api) -> None:
    """Evaluation default decision false."""
    mock_api.respond({})
    client = make_client(AuthZENClient)
    assert client.evaluation(("Person", "ada"), "CAN_DRIVE", ("Car", "kitt")).decision is False


def test_evaluation_invalid_subject_raises(make_client) -> None:
    """Evaluation invalid subject raises."""
    client = make_client(AuthZENClient)
    with pytest.raises(RequestValidationError, match="subject"):
        client.evaluation({"type": "Person"}, "CAN_DRIVE", ("Car", "kitt"))


def test_evaluations_defaults_and_items(make_client, mock_api) -> None:
    """Evaluations defaults and items."""
    mock_api.respond({"evaluations": [{"decision": True}, {"decision": False}]})
    client = make_client(AuthZENClient)
    result = client.evaluations(
        [
            {"resource": {"type": "Car", "id": "kitt"}},
            EvaluationItem(resource=Node(type="Car", id="karr")),
        ],
        subject=("Person", "ada"),
        action="CAN_DRIVE",
    )
    body = sent_json(mock_api.last)
    assert body["subject"] == {"type": "Person", "id": "ada"}
    assert body["action"] == {"name": "CAN_DRIVE"}
    assert body["evaluations"] == [
        {"resource": {"type": "Car", "id": "kitt"}},
        {"resource": {"type": "Car", "id": "karr"}},
    ]
    assert result.decisions == [True, False]


def test_evaluations_empty_items_raise(make_client) -> None:
    """Evaluations empty items raise."""
    client = make_client(AuthZENClient)
    with pytest.raises(RequestValidationError, match="At least one"):
        client.evaluations([])


def test_evaluations_item_with_no_overrides_raises(make_client) -> None:
    """Evaluations item with no overrides raises."""
    client = make_client(AuthZENClient)
    with pytest.raises(RequestValidationError, match="at least one"):
        client.evaluations([{}], subject=("Person", "ada"))


def test_searches_search_action(make_client, mock_api) -> None:
    """Searches search action."""
    mock_api.respond({"results": [{"name": "CAN_DRIVE"}, {"name": "CAN_WASH"}]})
    client = make_client(AuthZENClient)
    result = client.search_action(("Person", "ada"), ("Car", "kitt"))
    assert mock_api.last.url.path == "/access/v1/search/action"
    assert result.action_names == ["CAN_DRIVE", "CAN_WASH"]


def test_searches_search_resource_with_bare_type(make_client, mock_api) -> None:
    """Searches search resource with bare type."""
    mock_api.respond({"results": [{"type": "Car", "id": "kitt"}]})
    client = make_client(AuthZENClient)
    result = client.search_resource(("Person", "ada"), "CAN_DRIVE", "Car")
    assert sent_json(mock_api.last) == {
        "subject": {"type": "Person", "id": "ada"},
        "action": {"name": "CAN_DRIVE"},
        "resource": {"type": "Car"},
    }
    assert result.results[0].id == "kitt"


def test_searches_search_subject(make_client, mock_api) -> None:
    """Searches search subject."""
    mock_api.respond({"results": [{"type": "Person", "id": "ada"}]})
    client = make_client(AuthZENClient)
    result = client.search_subject(("Car", "kitt"), "CAN_DRIVE", "Person", context=Context(policy_tags=["x"]))
    assert sent_json(mock_api.last) == {
        "subject": {"type": "Person"},
        "action": {"name": "CAN_DRIVE"},
        "resource": {"type": "Car", "id": "kitt"},
        "context": {"policy_tags": ["x"]},
    }
    assert result.results[0].type == "Person"


async def test_async_authzen_evaluation(make_async_client, mock_api) -> None:
    """Async authzen evaluation."""
    mock_api.respond({"decision": True, "context": {"reason": "policy matched"}})
    async with make_async_client(AsyncAuthZENClient) as client:
        result = await client.evaluation(("Person", "ada"), "CAN_DRIVE", ("Car", "kitt"))
    assert result.decision is True
    assert result.context is not None
    assert result.context.reason == "policy matched"


async def test_async_authzen_search_resource(make_async_client, mock_api) -> None:
    """Async authzen search resource."""
    mock_api.respond({"results": []})
    async with make_async_client(AsyncAuthZENClient) as client:
        result = await client.search_resource(("Person", "ada"), "CAN_DRIVE", "Car", user_token="user-jwt")
    assert result.results == []
    assert mock_api.last.headers["Authorization"] == "Bearer user-jwt"


async def test_async_authzen_remaining_endpoints_round_trip(make_async_client, mock_api) -> None:
    """Async authzen remaining endpoints round trip."""
    mock_api.respond({"evaluations": [{"decision": True}]})
    async with make_async_client(AsyncAuthZENClient) as client:
        batch = await client.evaluations(
            [{"resource": {"type": "Car", "id": "kitt"}}], subject=("Person", "ada"), action="CAN_DRIVE"
        )
        await client.search_action(("Person", "ada"), ("Car", "kitt"))
        await client.search_subject(("Car", "kitt"), "CAN_DRIVE", "Person")
    assert batch.decisions == [True]
    paths = [request.url.path.removeprefix("/access/v1") for request in mock_api.requests]
    assert paths == ["/evaluations", "/search/action", "/search/subject"]
