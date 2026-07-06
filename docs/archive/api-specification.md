---
Status: Deprecated
Reason: Legacy architecture based on multi-agent chatbot framework (Redis, PostgreSQL, Qdrant, FastAPI, LangGraph, PydanticAI) has been replaced by the modular Operating System model (Kernel, Execution Engine, Runtime SDK, Workspace, Storage, Repository, Artifact, Organization).
Superseded By: ADR-0011 through ADR-0027, docs/id/architecture/book.md
Replacement: docs/id/architecture/book.md
---

# 09.1 — Spesifikasi API

> Dokumen ini mendeskripsikan REST API AetherOS yang dibangun dengan FastAPI, termasuk endpoint, authentication, dan OpenAPI specification.

---

## 9.1.1 API Overview

| Aspek | Detail |
|-------|--------|
| **Framework** | FastAPI |
| **Protocol** | REST (HTTP/1.1 + HTTP/2) |
| **Format** | JSON |
| **Authentication** | API Key + JWT |
| **Rate Limiting** | Per-key, configurable |
| **Versioning** | URL-based (`/api/v1/`) |
| **Documentation** | Auto-generated OpenAPI (Swagger) |

---

## 9.1.2 Endpoint Catalog

### Projects

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `GET` | `/api/v1/projects` | Daftar semua proyek |
| `POST` | `/api/v1/projects` | Buat proyek baru |
| `GET` | `/api/v1/projects/{id}` | Detail proyek |
| `PATCH` | `/api/v1/projects/{id}` | Update proyek |
| `DELETE` | `/api/v1/projects/{id}` | Arsipkan proyek (soft delete) |
| `GET` | `/api/v1/projects/{id}/stats` | Statistik proyek |

### Instructions (Task Submission)

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `POST` | `/api/v1/projects/{id}/instructions` | Kirim instruksi baru |
| `GET` | `/api/v1/projects/{id}/instructions` | Daftar instruksi |
| `GET` | `/api/v1/instructions/{id}` | Detail instruksi + status |
| `DELETE` | `/api/v1/instructions/{id}` | Batalkan instruksi |

### Tasks

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `GET` | `/api/v1/projects/{id}/tasks` | Daftar tasks per proyek |
| `GET` | `/api/v1/tasks/{id}` | Detail task |
| `GET` | `/api/v1/tasks/{id}/logs` | Log eksekusi task |
| `GET` | `/api/v1/tasks/{id}/artifacts` | Artifacts yang dihasilkan |
| `POST` | `/api/v1/tasks/{id}/retry` | Retry task yang gagal |

### Agents

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `GET` | `/api/v1/agents` | Daftar agen dan status |
| `GET` | `/api/v1/agents/{id}` | Detail agen |
| `GET` | `/api/v1/agents/{id}/stats` | Statistik agen |
| `POST` | `/api/v1/agents/{id}/restart` | Restart agen |

### Approvals (HITL)

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `GET` | `/api/v1/approvals/pending` | Daftar approval yang pending |
| `GET` | `/api/v1/approvals/{id}` | Detail approval request |
| `POST` | `/api/v1/approvals/{id}/approve` | Setujui aksi |
| `POST` | `/api/v1/approvals/{id}/deny` | Tolak aksi |

### Knowledge (Project Brain)

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `GET` | `/api/v1/projects/{id}/knowledge` | Daftar knowledge entries |
| `GET` | `/api/v1/knowledge/{id}` | Detail knowledge entry |
| `POST` | `/api/v1/projects/{id}/knowledge/search` | Semantic search |
| `GET` | `/api/v1/projects/{id}/knowledge/stats` | Statistik knowledge base |

### Analytics

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `GET` | `/api/v1/analytics/costs` | Cost analytics (filters: project, agent, date range) |
| `GET` | `/api/v1/analytics/tokens` | Token usage analytics |
| `GET` | `/api/v1/analytics/performance` | Performance metrics |
| `GET` | `/api/v1/analytics/agents` | Agent performance comparison |

### Audit

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `GET` | `/api/v1/audit/logs` | Query audit logs (filters: project, agent, action, date) |
| `GET` | `/api/v1/audit/trace/{trace_id}` | Ambil seluruh log per trace |

### System

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `GET` | `/api/v1/system/health` | System health check |
| `GET` | `/api/v1/system/config` | Current configuration |
| `GET` | `/api/v1/system/providers` | Status LLM providers |

---

## 9.1.3 Authentication

### API Key Authentication

| Header | Format |
|--------|--------|
| `Authorization` | `Bearer {api_key}` |
| `X-Project-ID` | `{project_uuid}` (opsional, untuk scoping) |

### JWT Token (untuk Dashboard)

| Endpoint | Method | Deskripsi |
|----------|--------|-----------|
| `/api/v1/auth/login` | POST | Login, return JWT |
| `/api/v1/auth/refresh` | POST | Refresh JWT token |
| `/api/v1/auth/logout` | POST | Invalidate token |

---

## 9.1.4 Response Format

### Success Response

| Field | Tipe | Deskripsi |
|-------|------|-----------|
| `status` | string | "success" |
| `data` | object/array | Data yang diminta |
| `meta` | object | Pagination, total count, dll. |

### Error Response

| Field | Tipe | Deskripsi |
|-------|------|-----------|
| `status` | string | "error" |
| `error` | object | Error details |
| `error.code` | string | Error code |
| `error.message` | string | Human-readable message |
| `error.details` | object | Additional error context |

### HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET/PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Missing/invalid credentials |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource conflict |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

---

## 9.1.5 Rate Limiting

| Tier | Requests/min | Burst |
|------|-------------|-------|
| Free | 60 | 10 |
| Standard | 300 | 50 |
| Enterprise | 1000 | 100 |

---

## 9.1.6 WebSocket API (Real-time)

| Endpoint | Deskripsi |
|----------|-----------|
| `ws://host/api/v1/ws/tasks/{project_id}` | Real-time task status updates |
| `ws://host/api/v1/ws/agents` | Real-time agent status |
| `ws://host/api/v1/ws/approvals` | Real-time approval notifications |
| `ws://host/api/v1/ws/logs/{task_id}` | Live log streaming |

---

🔗 **Selanjutnya:** [Referensi CLI →](cli-reference.md)

🔗 **Kembali:** [Strategi Skalabilitas ←](../08-operations/scalability-strategy.md)
