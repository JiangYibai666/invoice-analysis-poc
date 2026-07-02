from __future__ import annotations

import json
import os
from typing import Any, TypedDict

from psycopg2.extras import Json, RealDictCursor

from storage.task_store import _connect


DEFAULT_MEMORY_TURN_LIMIT = 6
MAX_MEMORY_FIELD_CHARS = 1200


class ConversationTurn(TypedDict):
    turn_index: int
    user_query: str
    memory_query: str | None
    assistant_summary: str | None


def _memory_turn_limit() -> int:
    raw = os.getenv("DOXA_MEMORY_TURN_LIMIT")
    if not raw:
        return DEFAULT_MEMORY_TURN_LIMIT
    try:
        return max(0, min(20, int(raw)))
    except ValueError:
        return DEFAULT_MEMORY_TURN_LIMIT


def _truncate(value: str | None, limit: int = MAX_MEMORY_FIELD_CHARS) -> str:
    text = (value or "").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def _assistant_summary(final_report: dict[str, Any]) -> str:
    summary = str(final_report.get("summary") or "").strip()
    if summary:
        return summary
    raw_data = final_report.get("raw_data")
    if isinstance(raw_data, dict):
        return str(raw_data.get("summary") or "").strip()
    return ""


def ensure_conversation(conversation_id: str, title: str | None = None) -> None:
    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO invoice_poc_conversations (conversation_id, title)
                VALUES (%s, %s)
                ON CONFLICT (conversation_id) DO UPDATE
                    SET updated_at = NOW(),
                        title = COALESCE(invoice_poc_conversations.title, EXCLUDED.title)
                """,
                (conversation_id, _truncate(title, 160) if title else None),
            )
        conn.commit()
    finally:
        conn.close()


def _fetch_recent_turns(
    cur: Any,
    conversation_id: str,
    limit: int,
    before_turn_index: int | None = None,
) -> list[ConversationTurn]:
    if limit <= 0:
        return []

    before_clause = ""
    params: list[Any] = [conversation_id]
    if before_turn_index is not None:
        before_clause = "AND turn_index < %s"
        params.append(before_turn_index)
    params.append(limit)

    cur.execute(
        f"""
        SELECT turn_index, user_query, memory_query, assistant_summary
        FROM invoice_poc_conversation_turns
        WHERE conversation_id = %s
          AND final_report IS NOT NULL
          {before_clause}
        ORDER BY turn_index DESC
        LIMIT %s
        """,
        params,
    )
    rows = cur.fetchall()
    return [
        {
            "turn_index": int(row["turn_index"]),
            "user_query": row["user_query"],
            "memory_query": row["memory_query"],
            "assistant_summary": row["assistant_summary"],
        }
        for row in reversed(rows)
    ]


def start_conversation_turn(
    conversation_id: str,
    session_id: str,
    user_query: str,
    title: str | None = None,
    limit: int | None = None,
) -> tuple[int, list[ConversationTurn]]:
    """Reserve the next turn index and return completed recent turns.

    The conversation row is locked while the turn index is calculated and the
    placeholder row is inserted. That makes concurrent requests for the same
    conversation allocate distinct turn indexes instead of racing on MAX()+1.
    """
    turn_limit = _memory_turn_limit() if limit is None else max(0, min(20, limit))
    conn = _connect()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO invoice_poc_conversations (conversation_id, title)
                VALUES (%s, %s)
                ON CONFLICT (conversation_id) DO UPDATE
                    SET updated_at = NOW(),
                        title = COALESCE(invoice_poc_conversations.title, EXCLUDED.title)
                """,
                (conversation_id, _truncate(title or user_query, 160)),
            )
            cur.execute(
                """
                SELECT conversation_id
                FROM invoice_poc_conversations
                WHERE conversation_id = %s
                FOR UPDATE
                """,
                (conversation_id,),
            )
            cur.execute(
                """
                SELECT COALESCE(MAX(turn_index), 0) + 1 AS next_turn_index
                FROM invoice_poc_conversation_turns
                WHERE conversation_id = %s
                """,
                (conversation_id,),
            )
            turn_index = int(cur.fetchone()["next_turn_index"])
            recent_turns = _fetch_recent_turns(
                cur,
                conversation_id,
                turn_limit,
                before_turn_index=turn_index,
            )
            cur.execute(
                """
                INSERT INTO invoice_poc_conversation_turns
                    (conversation_id, session_id, turn_index, user_query)
                VALUES (%s, %s, %s, %s)
                """,
                (conversation_id, session_id, turn_index, user_query),
            )
        conn.commit()
        return turn_index, recent_turns
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def load_recent_turns(conversation_id: str, limit: int | None = None) -> list[ConversationTurn]:
    turn_limit = _memory_turn_limit() if limit is None else max(0, min(20, limit))
    if turn_limit <= 0:
        return []

    conn = _connect()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            return _fetch_recent_turns(cur, conversation_id, turn_limit)
    finally:
        conn.close()


def build_memory_context(turns: list[ConversationTurn]) -> str:
    if not turns:
        return ""

    lines = ["Recent conversation context, oldest to newest:"]
    for turn in turns:
        lines.append(f"Turn {turn['turn_index']} user: {_truncate(turn['user_query'])}")
        summary = _truncate(turn.get("assistant_summary"))
        if summary:
            lines.append(f"Turn {turn['turn_index']} assistant: {summary}")
    return "\n".join(lines)


def save_conversation_turn(
    conversation_id: str,
    session_id: str,
    turn_index: int,
    user_query: str,
    memory_query: str,
    final_report: dict[str, Any],
) -> None:
    summary = _assistant_summary(final_report)
    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO invoice_poc_conversation_turns
                    (
                        conversation_id,
                        session_id,
                        turn_index,
                        user_query,
                        memory_query,
                        assistant_summary,
                        final_report
                    )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (conversation_id, turn_index) DO UPDATE
                    SET session_id = EXCLUDED.session_id,
                        user_query = EXCLUDED.user_query,
                        memory_query = EXCLUDED.memory_query,
                        assistant_summary = EXCLUDED.assistant_summary,
                        final_report = EXCLUDED.final_report
                """,
                (
                    conversation_id,
                    session_id,
                    turn_index,
                    user_query,
                    memory_query,
                    _truncate(summary),
                    Json(final_report, dumps=lambda data: json.dumps(data, ensure_ascii=True)),
                ),
            )
            cur.execute(
                """
                UPDATE invoice_poc_conversations
                SET updated_at = NOW()
                WHERE conversation_id = %s
                """,
                (conversation_id,),
            )
        conn.commit()
    finally:
        conn.close()
