from __future__ import annotations

import json
import re
from typing import Any, TypedDict

from agents.capabilities import AGENT_CAPABILITIES, AgentName
from agents.host_agent.prompts import ROUTER_PROMPT_TEMPLATE
from tools.gemini_sql import generate_content, get_client


class RouteDecision(TypedDict):
    target_agents: list[AgentName]
    reason: str
    required_entities: list[str]
    task_type: str
    capabilities: dict[str, dict]


_VALID_AGENTS: set[str] = set(AGENT_CAPABILITIES)
_VALID_TASK_TYPES = {
    "invoice_analysis",
    "purchase_order_analysis",
    "delivery_order_analysis",
    "purchase_and_delivery_order_analysis",
    "off_topic",
}

# Keyword hints used as a last-resort fallback when the LLM returns no valid agents.
_KEYWORD_FALLBACK: list[tuple[list[str], AgentName, str]] = [
    (["purchase order", " po ", "po ", " po,", "p.o."], "PurchaseOrderAgent", "purchase_order_analysis"),
    (["delivery order", " do ", "do ", " do,", "d.o."], "DeliveryOrderAgent", "delivery_order_analysis"),
    (["invoice", "supplier", "buyer", "payment"], "InvoiceAgent", "invoice_analysis"),
]


def _extract_json(text: str) -> dict[str, Any]:
    stripped = text.strip()
    stripped = re.sub(r"^```(?:json)?\s*\n?", "", stripped, flags=re.IGNORECASE)
    stripped = re.sub(r"\n?```\s*$", "", stripped)
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", stripped, flags=re.DOTALL)
        if not match:
            raise ValueError(f"Router did not return JSON: {text}") from None
        return json.loads(match.group(0))


def _normalize_route(payload: dict[str, Any]) -> RouteDecision:
    raw_agents = payload.get("target_agents")
    if not isinstance(raw_agents, list):
        raise ValueError("Router JSON must include target_agents as a list.")

    task_type = str(payload.get("task_type") or "").strip()
    if task_type not in _VALID_TASK_TYPES:
        raise ValueError(f"Router selected invalid task_type: {task_type}")

    target_agents: list[AgentName] = []
    for raw_agent in raw_agents:
        if raw_agent not in _VALID_AGENTS:
            raise ValueError(f"Router selected unknown agent: {raw_agent}")
        if raw_agent not in target_agents:
            target_agents.append(raw_agent)

    # Off-topic questions legitimately carry no agents; the HostAgent answers directly.
    if not target_agents and task_type != "off_topic":
        raise ValueError("Router must select at least one target agent.")

    required_entities_raw = payload.get("required_entities", [])
    if not isinstance(required_entities_raw, list):
        raise ValueError("Router JSON required_entities must be a list.")
    required_entities = [str(entity) for entity in required_entities_raw]

    reason = str(payload.get("reason") or "Selected by LLM router.").strip()

    return {
        "target_agents": target_agents,
        "reason": reason,
        "required_entities": required_entities,
        "task_type": task_type,
        "capabilities": {agent: AGENT_CAPABILITIES[agent] for agent in target_agents},
    }


def _fallback_route(query: str) -> RouteDecision:
    """Keyword-based fallback when the LLM router fails to return a valid decision."""
    q = query.lower()
    # "PO invoice" / "DO invoice" describe a subset of invoices (those with a linked
    # PO/DO), not PO/DO records — route them to InvoiceAgent regardless of the PO/DO
    # keywords they contain.
    if "po invoice" in q or "do invoice" in q:
        return {
            "target_agents": ["InvoiceAgent"],
            "reason": "'PO/DO invoice' refers to invoices with a linked PO/DO.",
            "required_entities": [],
            "task_type": "invoice_analysis",
            "capabilities": {"InvoiceAgent": AGENT_CAPABILITIES["InvoiceAgent"]},
        }
    for keywords, agent, ttype in _KEYWORD_FALLBACK:
        if any(kw in q for kw in keywords):
            return {
                "target_agents": [agent],
                "reason": "Fallback routing based on keyword matching.",
                "required_entities": [],
                "task_type": ttype,
                "capabilities": {agent: AGENT_CAPABILITIES[agent]},
            }
    # Last resort: all three agents try to answer
    all_agents: list[AgentName] = ["InvoiceAgent", "PurchaseOrderAgent", "DeliveryOrderAgent"]
    return {
        "target_agents": all_agents,
        "reason": "Could not determine intent; broadcasting to all agents.",
        "required_entities": [],
        "task_type": "invoice_analysis",
        "capabilities": {a: AGENT_CAPABILITIES[a] for a in all_agents},
    }


def route_query(query: str) -> RouteDecision:
    capabilities_json = json.dumps(AGENT_CAPABILITIES, indent=2)
    prompt = ROUTER_PROMPT_TEMPLATE.format(
        capabilities_json=capabilities_json,
        query=query,
    )

    try:
        client = get_client()
        payload = _extract_json(generate_content(client, prompt))
        return _normalize_route(payload)
    except (ValueError, KeyError):
        return _fallback_route(query)
