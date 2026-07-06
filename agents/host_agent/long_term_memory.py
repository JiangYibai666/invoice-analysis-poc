from __future__ import annotations

import re
from typing import Any

from storage.memory_store import (
    LongTermMemory,
    default_memory_scope_id,
    embedding_model,
    list_long_term_memories,
    long_term_memory_enabled,
    long_term_memory_limit,
    search_long_term_memories,
    upsert_long_term_memory,
)
from tools.document_match_query import extract_do_no, extract_invoice_no, extract_po_no


_BUSINESS_QUERY_TYPES = {
    "invoice_analysis",
    "purchase_order_analysis",
    "delivery_order_analysis",
    "multi_agent_analysis",
    "document_matching",
}
_CROSS_CONVERSATION_CUE_RE = re.compile(
    r"\b(previous|last|last time|earlier|before|already checked|we checked|i checked)\b"
    r"|之前|上次|刚才|查过|看过|历史|以前",
    re.IGNORECASE,
)
_LAST_INVOICE_RE = re.compile(
    r"\b(?:previous|last|earlier)\s+(?:invoice|inv)\b|(?:上次|之前|刚才|最近).{0,8}发票",
    re.IGNORECASE,
)
_LAST_PO_RE = re.compile(
    r"\b(?:previous|last|earlier)\s+(?:po|purchase\s+order)\b|(?:上次|之前|刚才|最近).{0,8}(?:po|采购订单)",
    re.IGNORECASE,
)
_LAST_DO_RE = re.compile(
    r"\b(?:previous|last|earlier)\s+(?:do|delivery\s+order)\b|(?:上次|之前|刚才|最近).{0,8}(?:do|送货单|交货单)",
    re.IGNORECASE,
)


def _memory_enabled() -> bool:
    return long_term_memory_enabled()


def _embed_text(text: str) -> list[float]:
    try:
        from tools.gemini_sql import generate_embedding, get_client

        return generate_embedding(get_client(), text, embedding_model())
    except Exception:  # noqa: BLE001
        return []


def _business_report(report: dict[str, Any]) -> bool:
    qtype = str(report.get("query_type") or report.get("raw_data", {}).get("query_type") or "")
    return qtype in _BUSINESS_QUERY_TYPES or qtype.endswith("_analysis")


def _memory_content(
    entity_label: str | None,
    entity_value: str | None,
    query: str,
    summary: str,
) -> str:
    prefix = f"{entity_label} {entity_value}: " if entity_label and entity_value else ""
    return f"{prefix}User asked: {query}\nAnswer summary: {summary}".strip()


def _entity_refs(text: str) -> list[tuple[str, str]]:
    refs: list[tuple[str, str]] = []
    for kind, extractor in (
        ("po", extract_po_no),
        ("do", extract_do_no),
        ("invoice", extract_invoice_no),
    ):
        value = extractor(text)
        if value:
            refs.append((kind, value))
    return refs


def _preferred_cross_conversation_entity_type(query: str) -> str | None:
    if _LAST_INVOICE_RE.search(query):
        return "invoice"
    if _LAST_PO_RE.search(query):
        return "po"
    if _LAST_DO_RE.search(query):
        return "do"
    return None


def _dedupe_memories(memories: list[LongTermMemory]) -> list[LongTermMemory]:
    seen: set[int] = set()
    deduped: list[LongTermMemory] = []
    for memory in memories:
        memory_id = int(memory["memory_id"])
        if memory_id in seen:
            continue
        seen.add(memory_id)
        deduped.append(memory)
    return deduped


def _latest_entity_memories(
    memory_scope_id: str,
    entity_type: str,
    limit: int,
) -> list[LongTermMemory]:
    candidates = list_long_term_memories(memory_scope_id, limit=50)
    entity_memories = [
        memory
        for memory in candidates
        if memory.get("memory_type") == "entity"
        and memory.get("entity_type") == entity_type
        and memory.get("entity_value")
    ]
    entity_memories.sort(
        key=lambda memory: (
            _user_query_contains_entity_ref(memory, entity_type),
            str(memory.get("updated_at") or ""),
        ),
        reverse=True,
    )
    return entity_memories[:limit]


def _user_query_contains_entity_ref(memory: LongTermMemory, entity_type: str) -> bool:
    content = str(memory.get("content") or "")
    before_summary = content.split("\n", 1)[0]
    if "User asked:" not in before_summary:
        return False
    user_query = before_summary.partition("User asked:")[2]
    extractor = {
        "invoice": extract_invoice_no,
        "po": extract_po_no,
        "do": extract_do_no,
    }.get(entity_type)
    if not extractor:
        return False
    return bool(extractor(user_query))


def save_long_term_memories_for_turn(
    memory_scope_id: str | None,
    conversation_id: str,
    turn_index: int,
    user_query: str,
    memory_query: str,
    report: dict[str, Any],
) -> None:
    if not _memory_enabled() or not _business_report(report):
        return

    scope_id = memory_scope_id or default_memory_scope_id()
    summary = str(report.get("summary") or "").strip()
    if not summary:
        return

    combined_text = " ".join(
        part for part in (user_query, memory_query, summary) if part
    )
    refs = _entity_refs(combined_text)
    memories: list[tuple[str, str | None, str | None, str, float]] = []
    for entity_type, entity_value in refs:
        memories.append(
            (
                "entity",
                entity_type,
                entity_value,
                _memory_content(entity_type, entity_value, user_query, summary),
                0.8,
            )
        )

    memories.append(
        (
            "summary",
            "turn",
            f"{conversation_id}:{turn_index}",
            _memory_content(None, None, user_query, summary),
            0.55 if refs else 0.45,
        )
    )

    for memory_type, entity_type, entity_value, content, importance in memories:
        embedding = _embed_text(content)
        upsert_long_term_memory(
            scope_id,
            memory_type,
            entity_type,
            entity_value,
            content,
            conversation_id,
            turn_index,
            importance,
            embedding,
        )


def retrieve_long_term_memories(
    memory_scope_id: str | None,
    query: str,
    limit: int | None = None,
) -> list[LongTermMemory]:
    if not _memory_enabled():
        return []
    scope_id = memory_scope_id or default_memory_scope_id()
    refs = dict(_entity_refs(query))
    memory_limit = long_term_memory_limit() if limit is None else max(0, min(20, limit))
    if memory_limit <= 0:
        return []
    preferred_type = (
        _preferred_cross_conversation_entity_type(query)
        if not refs and _CROSS_CONVERSATION_CUE_RE.search(query)
        else None
    )
    embedding = _embed_text(query)
    semantic = search_long_term_memories(scope_id, query, refs, embedding, limit)
    if not preferred_type:
        return semantic

    preferred = _latest_entity_memories(scope_id, preferred_type, limit=memory_limit)
    return _dedupe_memories([*preferred, *semantic])[:memory_limit]


def build_long_term_memory_context(memories: list[LongTermMemory]) -> str:
    if not memories:
        return ""
    lines = ["Relevant long-term memory, most relevant first:"]
    for memory in memories:
        entity = ""
        if memory.get("entity_type") and memory.get("entity_value"):
            entity = f" [{memory['entity_type']} {memory['entity_value']}]"
        lines.append(f"-{entity} {memory['content']}")
    return "\n".join(lines)


def maybe_rewrite_with_long_term_memory(
    query: str,
    memories: list[LongTermMemory],
) -> tuple[str, dict]:
    payload = {
        "retrieved_count": len(memories),
        "context": build_long_term_memory_context(memories),
        "items": memories,
        "rewritten": False,
        "rewritten_query": query,
    }
    has_current_ref = bool(extract_po_no(query) or extract_do_no(query) or extract_invoice_no(query))
    if has_current_ref or not memories or not _CROSS_CONVERSATION_CUE_RE.search(query):
        return query, payload

    preferred_type = _preferred_cross_conversation_entity_type(query)
    ordered_memories = memories
    if preferred_type:
        ordered_memories = [
            *[memory for memory in memories if memory.get("entity_type") == preferred_type],
            *[memory for memory in memories if memory.get("entity_type") != preferred_type],
        ]

    for memory in ordered_memories:
        entity_type = memory.get("entity_type")
        entity_value = memory.get("entity_value")
        if entity_type in {"invoice", "po", "do"} and entity_value:
            label = {
                "invoice": "invoice",
                "po": "purchase order",
                "do": "delivery order",
            }[entity_type]
            rewritten = f"{query} Referring to long-term memory's {label} {entity_value}."
            payload["rewritten"] = True
            payload["rewritten_query"] = rewritten
            payload["selected_memory_id"] = memory["memory_id"]
            return rewritten, payload
    return query, payload
