# 📂 Deprecated & Legacy Documentation Archive

Indeks ini memuat dokumen-dokumen lama (*legacy*) dari fase rancangan awal AetherOS yang telah dinyatakan **Deprecated**. 

## Mengapa Dokumen Ini Diarsipkan?
AetherOS telah bertransisi penuh dari **Kerangka Kerja Multi-Agen Chatbot (Redis/PostgreSQL/Qdrant/LangGraph)** ke arah **Sistem Operasi Agen Modular (Kernel, Execution, SDK, Workspace, Storage, Repository, Artifact, Organization)**. Seluruh logika asinkron bertumpu pada interaksi langsung melintasi Runtime SDK Facade, bukan melalui Event Bus Redis eksternal atau graph LangGraph.

Dokumen-dokumen di bawah ini disimpan murni untuk **catatan sejarah (historical record)** dan tidak mencerminkan implementasi kode saat ini.

---

## Indeks Dokumen Terdepresiasi

### 1. Dokumen Arsitektur Lama (Legacy Architecture)
- **[system-overview.md](system-overview.md)**: Gambaran arsitektur lama berbasis API FastAPI dan orkestrasi LangGraph.
- **[execution-loop.md](execution-loop.md)**: Siklus 7 tahap eksekusi berbasis Redis.
- **[event-driven-architecture.md](event-driven-architecture.md)**: Arsitektur event broker dengan Redis Streams.
- **[state-machine-orchestration.md](state-machine-orchestration.md)**: Integrasi dengan LangGraph.
- **[memory-architecture.md](memory-architecture.md)**: Memori jangka pendek dan panjang berbasis Qdrant.
- **[postgresql-schema.md](postgresql-schema.md)**: DDL untuk ledger terstruktur yang belum digunakan.
- **[qdrant-vector-design.md](qdrant-vector-design.md)**: Struktur koleksi vektor semantik.

### 2. Dokumen Agen Lama (Legacy Agents)
- **[agent-catalog.md](agent-catalog.md)**, **[agent-framework.md](agent-framework.md)**, **[agent-communication.md](agent-communication.md)**, **[agent-lifecycle.md](agent-lifecycle.md)**, **[agent-reputation.md](agent-reputation.md)**: Rancangan multi-agen spesialis yang saat ini ditangguhkan sampai Milestone 5 (Agent Runtime) dimulai.
- **[rbac-and-permissions.md](rbac-and-permissions.md)**: Otorisasi versi awal.
- **[ai-constitution.md](ai-constitution.md)**: Konstitusi aturan versi awal (diarsipkan, akan dirancang ulang di Milestone 8).

### 3. Integrasi & Tooling Lama (Legacy Tools)
- **[openhands-integration.md](openhands-integration.md)**: Abstraksi eksekusi sandbox versi awal.
- **[skill-library.md](skill-library.md)**: Pustaka skill/tool versi awal.
- **[plugin-sdk.md](plugin-sdk.md)**, **[marketplace-api.md](marketplace-api.md)**: Distribusi plugin versi awal.

### 4. Keputusan Arsitektural Lama (Legacy ADRs)
- **[0001-use-langgraph.md](0001-use-langgraph.md)**: Keputusan menggunakan LangGraph (Batal, digantikan model CQRS & Pipeline).
- **[0002-use-redis-streams.md](0002-use-redis-streams.md)**: Keputusan menggunakan Redis Streams (Batal, digantikan Runtime SDK).
- **[0003-use-qdrant.md](0003-use-qdrant.md)**: Keputusan menggunakan Qdrant (Batal, penulisan memori dilewatkan ke Artifact Runtime).
- **[0004-use-postgresql.md](0004-use-postgresql.md)**: Keputusan menggunakan PostgreSQL (Batal).
- **[0005-use-fastapi.md](0005-use-fastapi.md)**: Keputusan menggunakan FastAPI (Ditangguhkan).
- **[0006-use-opentelemetry.md](0006-use-opentelemetry.md)**: Keputusan menggunakan OpenTelemetry (Ditangguhkan).
- **[0007-use-pydanticai.md](0007-use-pydanticai.md)**: Keputusan menggunakan PydanticAI (Ditangguhkan).
- **[0008-use-openhands.md](0008-use-openhands.md)**: Keputusan menggunakan OpenHands (Ditangguhkan).

### 5. Glosarium Lama
- **[glossary.md](glossary.md)**: Daftar definisi lama yang mengandung banyak istilah Redis, LangGraph, dan DB. Digantikan oleh [docs/id/glossary/index.md](../glossary/index.md).
