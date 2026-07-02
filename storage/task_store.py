from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

from a2a.types import Artifact, Message, TaskState

load_dotenv()

SCHEMA_PATH = Path(__file__).with_name("schema.sql")

_TASK_DB_PARAMS: dict[str, Any] = {
    "host": os.getenv("TASK_DB_HOST", "localhost"),
    "port": int(os.getenv("TASK_DB_PORT", "5432")),
    "user": os.getenv("TASK_DB_USER", "postgres"),
    "password": os.getenv("TASK_DB_PASSWORD", "postgres"),
    "dbname": os.getenv("TASK_DB_NAME", "postgres"),
}


def _connect() -> psycopg2.extensions.connection:
    conn = psycopg2.connect(**_TASK_DB_PARAMS)
    conn.autocommit = False
    return conn


def init_db() -> None:
    """Create task-store tables if they do not exist."""
    sql = SCHEMA_PATH.read_text(encoding="utf-8")
    conn = _connect()
    try:
        with conn.cursor() as cur:
            for statement in sql.split(";"):
                stmt = statement.strip()
                if stmt:
                    cur.execute(stmt)
        conn.commit()
    finally:
        conn.close()


def create_session(
    session_id: str,
    user_query: str,
    conversation_id: str | None = None,
    turn_index: int | None = None,
) -> None:
    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO invoice_poc_sessions
                    (session_id, conversation_id, turn_index, user_query)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (session_id) DO UPDATE
                    SET conversation_id = COALESCE(EXCLUDED.conversation_id, invoice_poc_sessions.conversation_id),
                        turn_index = COALESCE(EXCLUDED.turn_index, invoice_poc_sessions.turn_index),
                        user_query = EXCLUDED.user_query
                """,
                (session_id, conversation_id, turn_index, user_query),
            )
        conn.commit()
    finally:
        conn.close()


def finalize_session(session_id: str, final_report: dict) -> None:
    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE invoice_poc_sessions
                SET final_report = %s, completed_at = NOW()
                WHERE session_id = %s
                """,
                (json.dumps(final_report, ensure_ascii=True), session_id),
            )
        conn.commit()
    finally:
        conn.close()


def create_task(
    task_id: str,
    session_id: str,
    source_agent: str,
    target_agent: str,
    state: TaskState,
) -> None:
    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO invoice_poc_tasks
                    (task_id, session_id, source_agent, target_agent, state)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (task_id) DO UPDATE
                    SET state = EXCLUDED.state, updated_at = NOW()
                """,
                (task_id, session_id, source_agent, target_agent, state.value),
            )
        conn.commit()
    finally:
        conn.close()


def update_task_state(task_id: str, state: TaskState) -> None:
    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE invoice_poc_tasks
                SET state = %s, updated_at = NOW()
                WHERE task_id = %s
                """,
                (state.value, task_id),
            )
        conn.commit()
    finally:
        conn.close()


def add_message(task_id: str, message: Message) -> None:
    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO invoice_poc_messages (message_id, task_id, role, parts_json)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (message_id) DO NOTHING
                """,
                (
                    message.message_id,
                    task_id,
                    message.role,
                    json.dumps(
                        [p.model_dump(mode="json") for p in message.parts],
                        ensure_ascii=True,
                    ),
                ),
            )
        conn.commit()
    finally:
        conn.close()


def add_artifact(task_id: str, artifact: Artifact) -> None:
    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO invoice_poc_artifacts (artifact_id, task_id, name, parts_json)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (artifact_id) DO NOTHING
                """,
                (
                    artifact.artifact_id,
                    task_id,
                    artifact.name,
                    json.dumps(
                        [p.model_dump(mode="json") for p in artifact.parts],
                        ensure_ascii=True,
                    ),
                ),
            )
        conn.commit()
    finally:
        conn.close()
