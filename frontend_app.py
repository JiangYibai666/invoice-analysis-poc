from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi import Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


FRONTEND_DIR = Path(__file__).resolve().parent / "doxa-agent-frontend"


app = FastAPI(title="Doxa Invoice Agent Frontend", version="0.1.0")


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.head("/")
async def index_head() -> Response:
    return Response(media_type="text/html")


@app.get("/DoxaApp.dc.html")
async def doxa_app() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "DoxaApp.dc.html")


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="frontend-static")
