from __future__ import annotations

import os
from collections.abc import AsyncIterator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from a2a.server import create_a2a_router
from a2a.types import TaskEvent, TaskRequest, TaskState
from agents.host_agent.graph import run_host_graph
from storage.memory_store import (
    default_memory_scope_id,
    delete_conversation,
    list_conversations,
    list_long_term_memories,
    load_conversation_debug_turns,
    soft_delete_long_term_memory,
)
from storage.task_store import add_artifact, add_message, create_task, update_task_state


def _cors_origins() -> list[str]:
    raw = os.getenv("DOXA_CORS_ORIGINS", "http://127.0.0.1:8080,http://localhost:8080")
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


async def stream_handler(request: TaskRequest) -> AsyncIterator[TaskEvent]:
    create_task(
        request.task_id,
        request.session_id,
        request.source_agent,
        request.target_agent,
        TaskState.WORKING,
    )
    add_message(request.task_id, request.message)

    async for event in run_host_graph(request):
        if event.artifact is not None:
            add_artifact(request.task_id, event.artifact)
        update_task_state(request.task_id, event.state)
        yield event


def create_app() -> FastAPI:
    _app = FastAPI(title="HostAgent", version="0.1.0")
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_origins(),
        allow_methods=["DELETE", "GET", "POST", "OPTIONS"],
        allow_headers=["content-type", "accept"],
    )

    @_app.get("/conversations")
    async def conversations(limit: int = 30, memory_scope_id: str | None = None) -> dict:
        scope_id = memory_scope_id or default_memory_scope_id()
        return {"memory_scope_id": scope_id, "conversations": list_conversations(limit, scope_id)}

    @_app.get("/conversations/{conversation_id}/turns")
    async def conversation_turns(
        conversation_id: str,
        limit: int = 50,
        memory_scope_id: str | None = None,
    ) -> dict:
        return {
            "conversation_id": conversation_id,
            "turns": load_conversation_debug_turns(
                conversation_id,
                limit,
                memory_scope_id or default_memory_scope_id(),
            ),
        }

    @_app.delete("/conversations/{conversation_id}")
    async def remove_conversation(
        conversation_id: str,
        memory_scope_id: str | None = None,
    ) -> dict:
        scope_id = memory_scope_id or default_memory_scope_id()
        if not delete_conversation(conversation_id, scope_id):
            raise HTTPException(status_code=404, detail="conversation not found")
        return {"conversation_id": conversation_id, "memory_scope_id": scope_id, "deleted": True}

    @_app.get("/memories")
    async def memories(
        limit: int = 30,
        q: str | None = None,
        memory_scope_id: str | None = None,
    ) -> dict:
        scope_id = memory_scope_id or default_memory_scope_id()
        return {
            "memory_scope_id": scope_id,
            "memories": list_long_term_memories(scope_id, limit, q),
        }

    @_app.delete("/memories/{memory_id}")
    async def remove_memory(memory_id: int, memory_scope_id: str | None = None) -> dict:
        scope_id = memory_scope_id or default_memory_scope_id()
        if not soft_delete_long_term_memory(memory_id, scope_id):
            raise HTTPException(status_code=404, detail="memory not found")
        return {"memory_id": memory_id, "memory_scope_id": scope_id, "deleted": True}

    _app.include_router(create_a2a_router(stream_handler))
    return _app


app = create_app()
