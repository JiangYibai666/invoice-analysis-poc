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


class ConversationDebugTurn(ConversationTurn):
    session_id: str
    status: str
    error_message: str | None
    final_report: dict[str, Any] | None
    created_at: str
    completed_at: str | None
    updated_at: str


class ConversationListItem(TypedDict):
    conversation_id: str
    title: str | None
    turn_count: int
    last_status: str | None
    last_user_query: str | None
    created_at: str
    updated_at: str


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
          AND status = 'completed'
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
                    (conversation_id, session_id, turn_index, user_query, status)
                VALUES (%s, %s, %s, %s, 'started')
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
                        final_report,
                        status,
                        error_message,
                        completed_at,
                        updated_at
                    )
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'completed', NULL, NOW(), NOW())
                ON CONFLICT (conversation_id, turn_index) DO UPDATE
                    SET session_id = EXCLUDED.session_id,
                        user_query = EXCLUDED.user_query,
                        memory_query = EXCLUDED.memory_query,
                        assistant_summary = EXCLUDED.assistant_summary,
                        final_report = EXCLUDED.final_report,
                        status = 'completed',
                        error_message = NULL,
                        completed_at = COALESCE(
                            invoice_poc_conversation_turns.completed_at,
                            EXCLUDED.completed_at
                        ),
                        updated_at = NOW()
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


def fail_conversation_turn(
    conversation_id: str,
    session_id: str,
    turn_index: int,
    user_query: str,
    memory_query: str,
    error_message: str,
) -> None:
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
                        status,
                        error_message,
                        completed_at,
                        updated_at
                    )
                VALUES (%s, %s, %s, %s, %s, 'failed', %s, NOW(), NOW())
                ON CONFLICT (conversation_id, turn_index) DO UPDATE
                    SET session_id = EXCLUDED.session_id,
                        user_query = EXCLUDED.user_query,
                        memory_query = EXCLUDED.memory_query,
                        status = 'failed',
                        error_message = EXCLUDED.error_message,
                        completed_at = COALESCE(
                            invoice_poc_conversation_turns.completed_at,
                            EXCLUDED.completed_at
                        ),
                        updated_at = NOW()
                """,
                (
                    conversation_id,
                    session_id,
                    turn_index,
                    user_query,
                    memory_query,
                    _truncate(error_message, 2000),
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


def load_conversation_debug_turns(
    conversation_id: str,
    limit: int = 20,
) -> list[ConversationDebugTurn]:
    turn_limit = max(1, min(100, limit))
    conn = _connect()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    turn_index,
                    session_id,
                    user_query,
                    memory_query,
                    assistant_summary,
                    final_report,
                    status,
                    error_message,
                    created_at,
                    completed_at,
                    updated_at
                FROM invoice_poc_conversation_turns
                WHERE conversation_id = %s
                ORDER BY turn_index DESC
                LIMIT %s
                """,
                (conversation_id, turn_limit),
            )
            rows = cur.fetchall()
    finally:
        conn.close()

    turns: list[ConversationDebugTurn] = []
    for row in reversed(rows):
        turns.append(
            {
                "turn_index": int(row["turn_index"]),
                "session_id": row["session_id"],
                "user_query": row["user_query"],
                "memory_query": row["memory_query"],
                "assistant_summary": row["assistant_summary"],
                "final_report": row["final_report"],
                "status": row["status"],
                "error_message": row["error_message"],
                "created_at": row["created_at"].isoformat(),
                "completed_at": row["completed_at"].isoformat() if row["completed_at"] else None,
                "updated_at": row["updated_at"].isoformat(),
            }
        )
    return turns


def list_conversations(limit: int = 30) -> list[ConversationListItem]:
    conversation_limit = max(1, min(100, limit))
    conn = _connect()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                WITH ranked_turns AS (
                    SELECT
                        conversation_id,
                        user_query,
                        status,
                        ROW_NUMBER() OVER (
                            PARTITION BY conversation_id
                            ORDER BY turn_index DESC
                        ) AS rn
                    FROM invoice_poc_conversation_turns
                ),
                turn_counts AS (
                    SELECT conversation_id, COUNT(*) AS turn_count
                    FROM invoice_poc_conversation_turns
                    GROUP BY conversation_id
                )
                SELECT
                    c.conversation_id,
                    c.title,
                    COALESCE(tc.turn_count, 0) AS turn_count,
                    rt.status AS last_status,
                    rt.user_query AS last_user_query,
                    c.created_at,
                    c.updated_at
                FROM invoice_poc_conversations c
                LEFT JOIN turn_counts tc ON tc.conversation_id = c.conversation_id
                LEFT JOIN ranked_turns rt
                    ON rt.conversation_id = c.conversation_id
                   AND rt.rn = 1
                ORDER BY c.updated_at DESC
                LIMIT %s
                """,
                (conversation_limit,),
            )
            rows = cur.fetchall()
    finally:
        conn.close()

    return [
        {
            "conversation_id": row["conversation_id"],
            "title": row["title"],
            "turn_count": int(row["turn_count"]),
            "last_status": row["last_status"],
            "last_user_query": row["last_user_query"],
            "created_at": row["created_at"].isoformat(),
            "updated_at": row["updated_at"].isoformat(),
        }
        for row in rows
    ]


def delete_conversation(conversation_id: str) -> bool:
    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM invoice_poc_conversation_turns
                WHERE conversation_id = %s
                """,
                (conversation_id,),
            )
            cur.execute(
                """
                DELETE FROM invoice_poc_conversations
                WHERE conversation_id = %s
                """,
                (conversation_id,),
            )
            deleted = cur.rowcount > 0
        conn.commit()
        return deleted
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
