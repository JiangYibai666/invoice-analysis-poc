from __future__ import annotations

import os
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from a2a.server import create_a2a_router
from a2a.types import TaskEvent, TaskRequest, TaskState
from agents.host_agent.graph import run_host_graph
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
        allow_methods=["POST", "OPTIONS"],
        allow_headers=["content-type", "accept"],
    )
    _app.include_router(create_a2a_router(stream_handler))
    return _app


app = create_app()
