from __future__ import annotations

import pytest

from agents.host_agent import router


def test_route_query_normalizes_valid_llm_json(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(router, "get_client", lambda: object())
    monkeypatch.setattr(
        router,
        "generate_content",
        lambda _client, _prompt: """
        {
          "target_agents": ["InvoiceAgent", "InvoiceAgent"],
          "reason": "invoice amount analysis",
          "required_entities": ["invoice"],
          "task_type": "invoice_analysis"
        }
        """,
    )

    route = router.route_query("List the 5 invoices with the highest amounts")

    assert route["target_agents"] == ["InvoiceAgent"]
    assert route["task_type"] == "invoice_analysis"
    assert route["capabilities"]["InvoiceAgent"]["agent_name"] == "InvoiceAgent"


def test_route_query_falls_back_when_llm_returns_invalid_json(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(router, "get_client", lambda: object())
    monkeypatch.setattr(router, "generate_content", lambda _client, _prompt: "not json")

    route = router.route_query("Which delivery orders are pending?")

    assert route["target_agents"] == ["DeliveryOrderAgent"]
    assert route["task_type"] == "delivery_order_analysis"
    assert route["reason"] == "Fallback routing based on keyword matching."


def test_route_query_does_not_short_circuit_highest_amount_query(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []

    monkeypatch.setattr(router, "get_client", lambda: object())

    def fake_generate_content(_client: object, prompt: str) -> str:
        calls.append(prompt)
        return """
        {
          "target_agents": ["InvoiceAgent"],
          "reason": "model selected invoice agent",
          "required_entities": [],
          "task_type": "invoice_analysis"
        }
        """

    monkeypatch.setattr(router, "generate_content", fake_generate_content)

    route = router.route_query("List the 5 invoices with the highest amounts")

    assert calls, "route_query should still call the LLM router for this query"
    assert route["target_agents"] == ["InvoiceAgent"]
    assert route["reason"] == "model selected invoice agent"
