# Aether Studio (M10) - Web Interface

Aether Studio is the official web dashboard for AetherOS. It provides a browser-accessible view of the Runtime, Company Brain, Workflow Runtime, Provider Router, and Execution Engine.

## Access

After starting the stack, open:

```
http://localhost:8000
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Dashboard UI (HTML) |
| GET | `/api/health` | Health check |
| GET | `/api/status` | System status (runtime + services) |
| GET | `/api/capabilities` | Registered runtime capabilities |
| GET | `/api/manifest` | Runtime manifest |
| POST | `/api/knowledge/query` | Query Company Brain |
| GET | `/api/workflow/list` | List workflows |
| GET | `/api/provider/list` | List providers |

## Local Development

```bash
.venv/bin/pip install -r web/requirements.txt
PYTHONPATH=runtime/src:core .venv/bin/python3 web/server.py
```

Then open http://localhost:8000

## Docker (recommended)

```bash
docker compose up -d
```

The `aetheros` service builds from `Dockerfile.dev` and runs `web/server.py` automatically. Health checks are configured on `/api/health`.

## Architecture

```
Browser → FastAPI (web/server.py) → AetherRuntime (facade) → Core Kernel / Execution Engine
```

The web layer never imports `core.kernel` or `core.execution` directly; it goes through the Runtime SDK Anti-Corruption Layer as required by the Runtime Specification (docs/id/architecture/runtime-specification.md).
