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
    "document_matching",
}


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

    target_agents: list[AgentName] = []
    for raw_agent in raw_agents:
        if raw_agent not in _VALID_AGENTS:
            raise ValueError(f"Router selected unknown agent: {raw_agent}")
        if raw_agent not in target_agents:
            target_agents.append(raw_agent)

    if not target_agents:
        raise ValueError("Router must select at least one target agent.")

    task_type = str(payload.get("task_type") or "").strip()
    if task_type not in _VALID_TASK_TYPES:
        raise ValueError(f"Router selected invalid task_type: {task_type}")

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


def route_query(query: str) -> RouteDecision:
    capabilities_json = json.dumps(AGENT_CAPABILITIES, indent=2)
    prompt = ROUTER_PROMPT_TEMPLATE.format(
        capabilities_json=capabilities_json,
        query=query,
    )

    client = get_client()
    payload = _extract_json(generate_content(client, prompt))
    return _normalize_route(payload)
