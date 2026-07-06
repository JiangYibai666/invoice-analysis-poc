from __future__ import annotations

import json
import os
import re
from math import sqrt
from typing import Any, TypedDict

from psycopg2.extras import Json, RealDictCursor

from storage.task_store import _connect


DEFAULT_MEMORY_TURN_LIMIT = 6
MAX_MEMORY_FIELD_CHARS = 1200
DEFAULT_MEMORY_SCOPE_ID = "local-user"
DEFAULT_LONG_TERM_MEMORY_LIMIT = 5
DEFAULT_MEMORY_MIN_IMPORTANCE = 0.4
EMBEDDING_DIMENSIONS = 768


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


class LongTermMemory(TypedDict):
    memory_id: int
    memory_scope_id: str
    memory_type: str
    entity_type: str | None
    entity_value: str | None
    content: str
    source_conversation_id: str | None
    source_turn_index: int | None
    importance: float
    status: str
    created_at: str
    updated_at: str


def default_memory_scope_id() -> str:
    return (os.getenv("DOXA_MEMORY_SCOPE_ID") or DEFAULT_MEMORY_SCOPE_ID).strip() or DEFAULT_MEMORY_SCOPE_ID


def long_term_memory_enabled() -> bool:
    raw = os.getenv("DOXA_LONG_TERM_MEMORY_ENABLED")
    if raw is None:
        return True
    return raw.lower() not in {"0", "false", "no", "off"}


def long_term_memory_limit() -> int:
    raw = os.getenv("DOXA_LONG_TERM_MEMORY_LIMIT")
    if not raw:
        return DEFAULT_LONG_TERM_MEMORY_LIMIT
    try:
        return max(0, min(20, int(raw)))
    except ValueError:
        return DEFAULT_LONG_TERM_MEMORY_LIMIT


def memory_min_importance() -> float:
    raw = os.getenv("DOXA_MEMORY_MIN_IMPORTANCE")
    if not raw:
        return DEFAULT_MEMORY_MIN_IMPORTANCE
    try:
        return max(0.0, min(1.0, float(raw)))
    except ValueError:
        return DEFAULT_MEMORY_MIN_IMPORTANCE


def embedding_model() -> str:
    return os.getenv("DOXA_EMBEDDING_MODEL", "text-embedding-004")


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


def _embedding_vector_literal(embedding: list[float] | None) -> str | None:
    if not embedding:
        return None
    return "[" + ",".join(f"{float(value):.8f}" for value in embedding[:EMBEDDING_DIMENSIONS]) + "]"


def _has_vector_column(cur: Any) -> bool:
    cur.execute(
        """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = 'invoice_poc_long_term_memories'
              AND column_name = 'embedding_vector'
        ) AS has_vector
        """
    )
    row = cur.fetchone()
    if isinstance(row, dict):
        return bool(row["has_vector"])
    return bool(row[0])


def _safe_words(text: str) -> list[str]:
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9_-]{2,}", text.lower())
    stop = {
        "the", "and", "for", "with", "that", "this", "what", "which", "show",
        "list", "invoice", "purchase", "order", "delivery", "about", "from",
    }
    return [word for word in words if word not in stop][:8]


def _cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right:
        return 0.0
    pairs = list(zip(left, right))
    dot = sum(a * b for a, b in pairs)
    left_norm = sqrt(sum(a * a for a, _ in pairs))
    right_norm = sqrt(sum(b * b for _, b in pairs))
    if not left_norm or not right_norm:
        return 0.0
    return dot / (left_norm * right_norm)


def ensure_conversation(
    conversation_id: str,
    title: str | None = None,
    memory_scope_id: str | None = None,
) -> None:
    scope_id = memory_scope_id or default_memory_scope_id()
    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO invoice_poc_conversations (conversation_id, memory_scope_id, title)
                VALUES (%s, %s, %s)
                ON CONFLICT (conversation_id) DO UPDATE
                    SET updated_at = NOW(),
                        memory_scope_id = COALESCE(invoice_poc_conversations.memory_scope_id, EXCLUDED.memory_scope_id),
                        title = COALESCE(invoice_poc_conversations.title, EXCLUDED.title)
                """,
                (conversation_id, scope_id, _truncate(title, 160) if title else None),
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
    memory_scope_id: str | None = None,
    title: str | None = None,
    limit: int | None = None,
) -> tuple[int, list[ConversationTurn]]:
    """Reserve the next turn index and return completed recent turns.

    The conversation row is locked while the turn index is calculated and the
    placeholder row is inserted. That makes concurrent requests for the same
    conversation allocate distinct turn indexes instead of racing on MAX()+1.
    """
    turn_limit = _memory_turn_limit() if limit is None else max(0, min(20, limit))
    scope_id = memory_scope_id or default_memory_scope_id()
    conn = _connect()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO invoice_poc_conversations (conversation_id, memory_scope_id, title)
                VALUES (%s, %s, %s)
                ON CONFLICT (conversation_id) DO UPDATE
                    SET updated_at = NOW(),
                        memory_scope_id = COALESCE(invoice_poc_conversations.memory_scope_id, EXCLUDED.memory_scope_id),
                        title = COALESCE(invoice_poc_conversations.title, EXCLUDED.title)
                """,
                (conversation_id, scope_id, _truncate(title or user_query, 160)),
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
    memory_scope_id: str | None = None,
) -> list[ConversationDebugTurn]:
    turn_limit = max(1, min(100, limit))
    scope_id = memory_scope_id or default_memory_scope_id()
    conn = _connect()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    t.turn_index,
                    t.session_id,
                    t.user_query,
                    t.memory_query,
                    t.assistant_summary,
                    t.final_report,
                    t.status,
                    t.error_message,
                    t.created_at,
                    t.completed_at,
                    t.updated_at
                FROM invoice_poc_conversation_turns t
                JOIN invoice_poc_conversations c
                  ON c.conversation_id = t.conversation_id
                WHERE t.conversation_id = %s
                  AND c.memory_scope_id = %s
                ORDER BY t.turn_index DESC
                LIMIT %s
                """,
                (conversation_id, scope_id, turn_limit),
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


def list_conversations(
    limit: int = 30,
    memory_scope_id: str | None = None,
) -> list[ConversationListItem]:
    conversation_limit = max(1, min(100, limit))
    scope_id = memory_scope_id or default_memory_scope_id()
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
                WHERE c.memory_scope_id = %s
                ORDER BY c.updated_at DESC
                LIMIT %s
                """,
                (scope_id, conversation_limit),
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


def delete_conversation(
    conversation_id: str,
    memory_scope_id: str | None = None,
) -> bool:
    scope_id = memory_scope_id or default_memory_scope_id()
    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT 1
                FROM invoice_poc_conversations
                WHERE conversation_id = %s
                  AND memory_scope_id = %s
                """,
                (conversation_id, scope_id),
            )
            if cur.fetchone() is None:
                conn.commit()
                return False
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


def upsert_long_term_memory(
    memory_scope_id: str,
    memory_type: str,
    entity_type: str | None,
    entity_value: str | None,
    content: str,
    source_conversation_id: str | None,
    source_turn_index: int | None,
    importance: float,
    embedding: list[float] | None = None,
) -> int:
    if importance < memory_min_importance():
        return 0
    scope_id = memory_scope_id or default_memory_scope_id()
    vector_literal = _embedding_vector_literal(embedding)
    conn = _connect()
    try:
        with conn.cursor() as cur:
            has_vector = _has_vector_column(cur)
            if has_vector and vector_literal:
                cur.execute(
                    """
                    INSERT INTO invoice_poc_long_term_memories
                        (
                            memory_scope_id,
                            memory_type,
                            entity_type,
                            entity_value,
                            content,
                            source_conversation_id,
                            source_turn_index,
                            embedding,
                            embedding_vector,
                            importance,
                            status,
                            updated_at
                        )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s::vector, %s, 'active', NOW())
                    ON CONFLICT (memory_scope_id, memory_type, entity_type, entity_value)
                    DO UPDATE SET
                        content = EXCLUDED.content,
                        source_conversation_id = EXCLUDED.source_conversation_id,
                        source_turn_index = EXCLUDED.source_turn_index,
                        embedding = EXCLUDED.embedding,
                        embedding_vector = EXCLUDED.embedding_vector,
                        importance = GREATEST(invoice_poc_long_term_memories.importance, EXCLUDED.importance),
                        status = 'active',
                        updated_at = NOW()
                    RETURNING memory_id
                    """,
                    (
                        scope_id,
                        memory_type,
                        entity_type,
                        entity_value,
                        _truncate(content, 3000),
                        source_conversation_id,
                        source_turn_index,
                        Json(embedding or [], dumps=lambda data: json.dumps(data, ensure_ascii=True)),
                        vector_literal,
                        max(0.0, min(1.0, importance)),
                    ),
                )
            else:
                cur.execute(
                    """
                    INSERT INTO invoice_poc_long_term_memories
                        (
                            memory_scope_id,
                            memory_type,
                            entity_type,
                            entity_value,
                            content,
                            source_conversation_id,
                            source_turn_index,
                            embedding,
                            importance,
                            status,
                            updated_at
                        )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'active', NOW())
                    ON CONFLICT (memory_scope_id, memory_type, entity_type, entity_value)
                    DO UPDATE SET
                        content = EXCLUDED.content,
                        source_conversation_id = EXCLUDED.source_conversation_id,
                        source_turn_index = EXCLUDED.source_turn_index,
                        embedding = EXCLUDED.embedding,
                        importance = GREATEST(invoice_poc_long_term_memories.importance, EXCLUDED.importance),
                        status = 'active',
                        updated_at = NOW()
                    RETURNING memory_id
                    """,
                    (
                        scope_id,
                        memory_type,
                        entity_type,
                        entity_value,
                        _truncate(content, 3000),
                        source_conversation_id,
                        source_turn_index,
                        Json(embedding or [], dumps=lambda data: json.dumps(data, ensure_ascii=True)),
                        max(0.0, min(1.0, importance)),
                    ),
                )
            memory_id = int(cur.fetchone()[0])
        conn.commit()
        return memory_id
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def list_long_term_memories(
    memory_scope_id: str | None = None,
    limit: int = 30,
    query: str | None = None,
) -> list[LongTermMemory]:
    scope_id = memory_scope_id or default_memory_scope_id()
    memory_limit = max(1, min(100, limit))
    words = _safe_words(query or "")
    conn = _connect()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            clauses = ["memory_scope_id = %s", "status = 'active'"]
            params: list[Any] = [scope_id]
            if words:
                like_clauses = []
                for word in words:
                    like_clauses.append("(LOWER(content) LIKE %s OR LOWER(COALESCE(entity_value, '')) LIKE %s)")
                    params.extend([f"%{word}%", f"%{word}%"])
                clauses.append("(" + " OR ".join(like_clauses) + ")")
            params.append(memory_limit)
            cur.execute(
                f"""
                SELECT
                    memory_id,
                    memory_scope_id,
                    memory_type,
                    entity_type,
                    entity_value,
                    content,
                    source_conversation_id,
                    source_turn_index,
                    importance,
                    status,
                    created_at,
                    updated_at
                FROM invoice_poc_long_term_memories
                WHERE {' AND '.join(clauses)}
                ORDER BY importance DESC, updated_at DESC
                LIMIT %s
                """,
                params,
            )
            rows = cur.fetchall()
    finally:
        conn.close()
    return [_memory_row_to_dict(row) for row in rows]


def search_long_term_memories(
    memory_scope_id: str | None,
    query: str,
    entity_refs: dict[str, str] | None = None,
    embedding: list[float] | None = None,
    limit: int | None = None,
) -> list[LongTermMemory]:
    if not long_term_memory_enabled():
        return []
    scope_id = memory_scope_id or default_memory_scope_id()
    memory_limit = long_term_memory_limit() if limit is None else max(0, min(20, limit))
    if memory_limit <= 0:
        return []
    refs = entity_refs or {}
    exact: list[LongTermMemory] = []
    conn = _connect()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            ref_items = [(kind, value) for kind, value in refs.items() if value]
            if ref_items:
                entity_clauses = []
                params: list[Any] = [scope_id]
                for kind, value in ref_items:
                    entity_clauses.append("(entity_type = %s AND entity_value = %s)")
                    params.extend([kind, value])
                params.append(memory_limit)
                cur.execute(
                    f"""
                    SELECT
                        memory_id,
                        memory_scope_id,
                        memory_type,
                        entity_type,
                        entity_value,
                        content,
                        source_conversation_id,
                        source_turn_index,
                        importance,
                        status,
                        created_at,
                        updated_at
                    FROM invoice_poc_long_term_memories
                    WHERE memory_scope_id = %s
                      AND status = 'active'
                      AND ({' OR '.join(entity_clauses)})
                    ORDER BY importance DESC, updated_at DESC
                    LIMIT %s
                    """,
                    params,
                )
                exact = [_memory_row_to_dict(row) for row in cur.fetchall()]

            remaining = max(0, memory_limit - len(exact))
            if remaining <= 0:
                return exact

            has_vector = _has_vector_column(cur)
            vector_literal = _embedding_vector_literal(embedding)
            if has_vector and vector_literal:
                cur.execute(
                    """
                    SELECT
                        memory_id,
                        memory_scope_id,
                        memory_type,
                        entity_type,
                        entity_value,
                        content,
                        source_conversation_id,
                        source_turn_index,
                        importance,
                        status,
                        created_at,
                        updated_at
                    FROM invoice_poc_long_term_memories
                    WHERE memory_scope_id = %s
                      AND status = 'active'
                      AND embedding_vector IS NOT NULL
                    ORDER BY embedding_vector <=> %s::vector
                    LIMIT %s
                    """,
                    (scope_id, vector_literal, remaining),
                )
                semantic = [_memory_row_to_dict(row) for row in cur.fetchall()]
            else:
                semantic = _fallback_search_memories(cur, scope_id, query, embedding, remaining)
    finally:
        conn.close()

    by_id: dict[int, LongTermMemory] = {}
    for memory in [*exact, *semantic]:
        by_id[memory["memory_id"]] = memory
    return list(by_id.values())[:memory_limit]


def soft_delete_long_term_memory(
    memory_id: int,
    memory_scope_id: str | None = None,
) -> bool:
    scope_id = memory_scope_id or default_memory_scope_id()
    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE invoice_poc_long_term_memories
                SET status = 'deleted', updated_at = NOW()
                WHERE memory_id = %s
                  AND memory_scope_id = %s
                  AND status = 'active'
                """,
                (memory_id, scope_id),
            )
            deleted = cur.rowcount > 0
        conn.commit()
        return deleted
    finally:
        conn.close()


def _fallback_search_memories(
    cur: Any,
    memory_scope_id: str,
    query: str,
    embedding: list[float] | None,
    limit: int,
) -> list[LongTermMemory]:
    cur.execute(
        """
        SELECT
            memory_id,
            memory_scope_id,
            memory_type,
            entity_type,
            entity_value,
            content,
            source_conversation_id,
            source_turn_index,
            embedding,
            importance,
            status,
            created_at,
            updated_at
        FROM invoice_poc_long_term_memories
        WHERE memory_scope_id = %s
          AND status = 'active'
        ORDER BY updated_at DESC
        LIMIT 200
        """,
        (memory_scope_id,),
    )
    rows = cur.fetchall()
    words = set(_safe_words(query))
    scored: list[tuple[float, LongTermMemory]] = []
    for row in rows:
        memory = _memory_row_to_dict(row)
        text = f"{memory.get('entity_value') or ''} {memory['content']}".lower()
        lexical = sum(1.0 for word in words if word in text)
        stored_embedding = row.get("embedding") if hasattr(row, "get") else None
        vector_score = _cosine_similarity(embedding or [], stored_embedding or [])
        score = lexical + vector_score + float(memory["importance"]) * 0.25
        if score > 0 or not words:
            scored.append((score, memory))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [memory for _, memory in scored[:limit]]


def _memory_row_to_dict(row: Any) -> LongTermMemory:
    return {
        "memory_id": int(row["memory_id"]),
        "memory_scope_id": row["memory_scope_id"],
        "memory_type": row["memory_type"],
        "entity_type": row["entity_type"],
        "entity_value": row["entity_value"],
        "content": row["content"],
        "source_conversation_id": row["source_conversation_id"],
        "source_turn_index": int(row["source_turn_index"]) if row["source_turn_index"] is not None else None,
        "importance": float(row["importance"]),
        "status": row["status"],
        "created_at": row["created_at"].isoformat(),
        "updated_at": row["updated_at"].isoformat(),
    }
