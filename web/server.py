# AetherOS Web Server (M10: Aether Studio)
# Web interface for monitoring Organization Runtime and Company Brain

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import asyncio
import json
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "runtime" / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))
sys.path.insert(0, str(Path(__file__).parent.parent / "storage" / "src"))

from aether_runtime.sdk import AetherRuntime
from aether_runtime.context.context import RuntimeContext
from aether_runtime.session.session import RuntimeSession
from aether_runtime.middleware.pipeline import MiddlewarePipeline
from aether_storage import start_persistence, stop_persistence

runtime_instance: Optional[AetherRuntime] = None
persistence_instance = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize AetherRuntime and persistence on startup and shut them down on shutdown."""
    global runtime_instance, persistence_instance
    try:
        persistence_instance = await start_persistence()
    except Exception as e:
        print(f"Failed to initialize persistence: {e}")
    try:
        context = RuntimeContext()
        session = RuntimeSession(context)
        pipeline = MiddlewarePipeline()
        runtime_instance = AetherRuntime(context, session, pipeline)
        await runtime_instance.start()
    except Exception as e:
        print(f"Failed to initialize runtime: {e}")
    yield
    if runtime_instance:
        await runtime_instance.stop()
    if persistence_instance:
        await stop_persistence()


app = FastAPI(
    title="AetherOS",
    description="AetherOS AI Operating Environment - Web Interface",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def index():
    """Serve the main dashboard."""
    html_file = Path(__file__).parent / "static" / "index.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(), status_code=200)
    return HTMLResponse(content="<h1>AetherOS</h1><p>UI not found</p>")


@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "runtime": "initialized" if runtime_instance else "not-initialized",
        "version": "1.0.0"
    }


@app.get("/api/capabilities")
async def get_capabilities():
    """Get runtime capabilities."""
    if not runtime_instance:
        raise HTTPException(status_code=503, detail="Runtime not initialized")
    caps = await runtime_instance.capabilities()
    return JSONResponse(content=caps)


@app.get("/api/manifest")
async def get_manifest():
    """Get runtime manifest."""
    if not runtime_instance:
        raise HTTPException(status_code=503, detail="Runtime not initialized")
    manifest = await runtime_instance.manifest()
    return JSONResponse(content=manifest.model_dump())


@app.get("/api/status")
async def get_status():
    """Get system status."""
    return {
        "runtime": "initialized" if runtime_instance else "not-initialized",
        "services": {
            "postgres": "healthy",
            "redis": "healthy", 
            "qdrant": "healthy"
        },
        "timestamp": asyncio.get_event_loop().time()
    }


class KnowledgeQuery(BaseModel):
    query: str
    limit: int = 10


@app.post("/api/knowledge/query")
async def query_knowledge(query: KnowledgeQuery):
    """Query Company Brain."""
    if not runtime_instance:
        raise HTTPException(status_code=503, detail="Runtime not initialized")
    try:
        result = runtime_instance.knowledge.query(query.query, limit=query.limit)
        return JSONResponse(content={
            "query": query.query,
            "results": [r.model_dump() for r in result]
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/workflow/list")
async def list_workflows():
    """List workflows."""
    if not runtime_instance:
        raise HTTPException(status_code=503, detail="Runtime not initialized")
    try:
        workflows = runtime_instance.workflow.list()
        return JSONResponse(content={"workflows": workflows})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/provider/list")
async def list_providers():
    """List providers."""
    if not runtime_instance:
        raise HTTPException(status_code=503, detail="Runtime not initialized")
    try:
        providers = runtime_instance.provider_router.list_providers()
        return JSONResponse(content={"providers": providers})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
