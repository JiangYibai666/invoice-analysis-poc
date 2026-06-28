from __future__ import annotations

import json
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi import Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


FRONTEND_DIR = Path(__file__).resolve().parent / "doxa-agent-frontend"
DEFAULT_HOST_AGENT_URL = "http://127.0.0.1:10000"


app = FastAPI(title="Doxa Invoice Agent Frontend", version="0.1.0")


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.head("/")
async def index_head() -> Response:
    return Response(media_type="text/html")


@app.get("/config.js")
async def config_js() -> Response:
    config = {
        "hostAgentUrl": os.getenv("HOST_AGENT_URL", DEFAULT_HOST_AGENT_URL),
        "defaultMode": os.getenv("DOXA_FRONTEND_MODE", "live"),
    }
    body = f"window.DOXA_CONFIG = {json.dumps(config, ensure_ascii=True)};"
    return Response(
        content=body,
        media_type="application/javascript",
        headers={"Cache-Control": "no-store"},
    )


@app.get("/DoxaApp.dc.html")
async def doxa_app() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "DoxaApp.dc.html")


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="frontend-static")
