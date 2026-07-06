---
Status: Deprecated
Reason: Legacy architecture based on multi-agent chatbot framework (Redis, PostgreSQL, Qdrant, FastAPI, LangGraph, PydanticAI) has been replaced by the modular Operating System model (Kernel, Execution Engine, Runtime SDK, Workspace, Storage, Repository, Artifact, Organization).
Superseded By: ADR-0011 through ADR-0027, docs/id/architecture/book.md
Replacement: docs/id/architecture/book.md
---

# 02.1 — Gambaran Umum Arsitektur Sistem

> Dokumen ini mendeskripsikan arsitektur global AetherOS, termasuk technology stack, dependency graph, dan diagram arsitektural.

---

## 2.1.1 Arsitektur Tingkat Tinggi (C4 — Context Level)

AetherOS beroperasi sebagai lapisan orkestrator antara manusia (pengguna) dan penyedia LLM, dengan Project Brain sebagai fondasi pengetahuan persisten.

```mermaid
graph TB
    subgraph "Aktor Eksternal"
        USER["👤 Pengguna<br/>(Developer / PM)"]
        GIT_EXT["🌐 Git Remote<br/>(GitHub/GitLab)"]
    end

    subgraph "AetherOS Platform"
        subgraph "Interface Layer"
            DASH["🖥️ Web Dashboard"]
            CLI_APP["⌨️ CLI Application"]
            API_GW["🔌 API Gateway<br/>(FastAPI)"]
        end

        subgraph "Orchestration Layer"
            ORCH["🎯 Orchestrator<br/>(LangGraph State Machine)"]
            EB["📨 Event Bus<br/>(Redis Streams)"]
        end

        subgraph "Agent Layer"
            MGR["👔 Manager"]
            ARC["📐 Architect"]
            BKD["⚙️ Backend"]
            FE["🎨 Frontend"]
            QA["🧪 QA"]
            SEC["🔒 Security"]
            DEV["🚀 DevOps"]
            DOC["📝 Documentation"]
        end

        subgraph "Intelligence Layer"
            ROUTER["🔀 Provider Router"]
            VALID["✅ PydanticAI<br/>Schema Validator"]
        end

        subgraph "Persistence Layer"
            PG["🗄️ PostgreSQL<br/>(Immutable Ledger)"]
            QD["🔮 Qdrant<br/>(Vector Memory)"]
            WS["📂 Workspace<br/>(Git Volume)"]
        end
    end

    subgraph "LLM Providers"
        OAI["OpenAI"]
        ANT["Anthropic"]
        OLL["Ollama"]
        GEM["Google AI"]
    end

    USER --> DASH
    USER --> CLI_APP
    DASH --> API_GW
    CLI_APP --> API_GW
    API_GW --> ORCH
    ORCH --> EB
    EB --> MGR
    EB --> ARC
    EB --> BKD
    EB --> FE
    EB --> QA
    EB --> SEC
    EB --> DEV
    EB --> DOC
    MGR --> ROUTER
    ARC --> ROUTER
    BKD --> ROUTER
    FE --> ROUTER
    QA --> ROUTER
    SEC --> ROUTER
    DEV --> ROUTER
    DOC --> ROUTER
    ROUTER --> VALID
    VALID --> OAI
    VALID --> ANT
    VALID --> OLL
    VALID --> GEM
    MGR --> PG
    ARC --> PG
    BKD --> WS
    FE --> WS
    QA --> WS
    SEC --> WS
    DEV --> WS
    DOC --> WS
    ORCH --> PG
    ORCH --> QD
    WS --> GIT_EXT

    style ORCH fill:#2b6cb0,color:#fff
    style EB fill:#d69e2e,color:#000
    style ROUTER fill:#e53e3e,color:#fff
    style PG fill:#2f855a,color:#fff
    style QD fill:#805ad5,color:#fff
```

---

## 2.1.2 Arsitektur Berlapis (Layered Architecture)

AetherOS terdiri dari 5 lapisan utama yang saling berkomunikasi secara hierarkis:

```mermaid
graph TD
    subgraph "Layer 1: Interface Layer"
        L1["Web Dashboard | CLI | REST API"]
    end

    subgraph "Layer 2: Orchestration Layer"
        L2["LangGraph State Machine | Event Bus (Redis Streams)"]
    end

    subgraph "Layer 3: Agent Layer"
        L3["Manager | Architect | Backend | Frontend | QA | Security | DevOps | Docs"]
    end

    subgraph "Layer 4: Intelligence Layer"
        L4["Provider Router | PydanticAI Validator | Knowledge Extraction Layer"]
    end

    subgraph "Layer 5: Persistence Layer"
        L5["PostgreSQL | Qdrant | Git Workspace"]
    end

    L1 --> L2
    L2 --> L3
    L3 --> L4
    L4 --> L5

    style L1 fill:#4299e1,color:#fff
    style L2 fill:#ed8936,color:#fff
    style L3 fill:#48bb78,color:#fff
    style L4 fill:#ed64a6,color:#fff
    style L5 fill:#9f7aea,color:#fff
```

### Deskripsi Setiap Lapisan

| Layer | Nama | Tanggung Jawab |
|-------|------|----------------|
| **1** | Interface Layer | Menerima instruksi dari pengguna melalui berbagai antarmuka (Dashboard, CLI, API). Menerjemahkan input manusia menjadi format yang dapat diproses oleh orchestrator. |
| **2** | Orchestration Layer | Mengelola siklus hidup tugas melalui state machine. Mendistribusikan tugas ke agen melalui event bus. Mengimplementasikan checkpoint gates untuk HITL. |
| **3** | Agent Layer | Eksekusi tugas spesifik berdasarkan peran. Setiap agen memiliki kemampuan, batasan akses, dan skill set yang terdefinisi. |
| **4** | Intelligence Layer | Mengabstraksi penyedia LLM, memvalidasi output, dan mengekstraksi pengetahuan dari respons LLM sebelum disimpan. |
| **5** | Persistence Layer | Menyimpan semua data secara permanen. PostgreSQL untuk data terstruktur, Qdrant untuk embedding vektor, Git untuk kode sumber. |

---

## 2.1.3 Technology Stack

### Stack Utama

| Komponen | Teknologi | Versi | Justifikasi Pemilihan |
|----------|-----------|-------|----------------------|
| **Runtime Language** | Python | 3.12+ | Ekosistem AI/ML terlengkap, type hinting matang, async native |
| **Orchestration** | LangGraph | Latest | State machine bawaan, checkpoint support, graph-based workflow |
| **Agent Runtime** | PydanticAI | v2.0+ | Strict schema enforcement, mencegah halusinasi merusak state |
| **Message Broker** | Redis | 7.2+ | Streams untuk event bus, pub/sub, consumer groups, low-latency |
| **Vector DB** | Qdrant | 1.8+ | Metadata filtering, payload indexing, horizontal scaling |
| **Relational DB** | PostgreSQL | 16+ | ACID compliance, JSONB support, mature ecosystem |
| **API Framework** | FastAPI | Latest | Async-first, OpenAPI auto-generation, dependency injection |
| **Containerization** | Docker | Latest | Isolasi agen, reproducibility, orchestration |
| **Observability** | OpenTelemetry | Latest | Vendor-neutral tracing, metrics, dan logging |
| **Tool Execution** | OpenHands | Latest | Sandboxed file operations dan terminal execution |

### Dependency Graph

```mermaid
graph TD
    PY["Python 3.12+"] --> PYDANTIC["PydanticAI v2.0+"]
    PY --> LANGGRAPH["LangGraph"]
    PY --> FASTAPI["FastAPI"]
    PY --> OTEL["OpenTelemetry SDK"]

    PYDANTIC --> AGENTS["Agent Runtime"]
    LANGGRAPH --> STATE["State Machine"]
    FASTAPI --> API["API Gateway"]

    AGENTS --> ROUTER["Provider Router"]
    ROUTER --> OPENAI["openai-python"]
    ROUTER --> ANTHROPIC["anthropic-python"]
    ROUTER --> OLLAMA["ollama-python"]

    STATE --> REDIS["Redis 7.2+"]
    REDIS --> EB["Event Bus"]
    REDIS --> CACHE["Cache Layer"]

    AGENTS --> PG["PostgreSQL 16+"]
    AGENTS --> QD["Qdrant 1.8+"]
    AGENTS --> OH["OpenHands"]

    PG --> SQLALCHEMY["SQLAlchemy"]
    PG --> ALEMBIC["Alembic<br/>(Migrations)"]
    QD --> QDRANT_CLIENT["qdrant-client"]

    style PY fill:#3776ab,color:#fff
    style REDIS fill:#dc382d,color:#fff
    style PG fill:#336791,color:#fff
    style QD fill:#805ad5,color:#fff
```

---

## 2.1.4 Struktur Direktori Proyek

```
aetheros/
├── core/              # Logic inti sistem
│   ├── engine.py      # Runtime engine utama
│   ├── config.py      # Konfigurasi global
│   ├── events.py      # Event definitions dan handlers
│   └── router.py      # Provider router utama
│
├── agents/            # Definisi dan logika agen
│   ├── base.py        # Base agent class (PydanticAI)
│   ├── manager.py     # Manager agent
│   ├── architect.py   # Architect agent
│   ├── backend.py     # Backend agent
│   ├── frontend.py    # Frontend agent
│   ├── qa.py          # QA agent
│   ├── security.py    # Security agent
│   ├── devops.py      # DevOps agent
│   └── docs.py        # Documentation agent
│
├── providers/         # Abstraksi penyedia LLM
│   ├── base.py        # Base provider interface
│   ├── openai.py      # OpenAI adapter
│   ├── anthropic.py   # Anthropic adapter
│   ├── ollama.py      # Ollama adapter
│   └── fallback.py    # Fallback logic
│
├── memory/            # Manajemen memori
│   ├── short_term.py  # LangGraph state (in-session)
│   ├── long_term.py   # Project Brain interface
│   └── distiller.py   # Knowledge extraction pipeline
│
├── brain/             # Integrasi database
│   ├── postgres/      # Schema, queries, migrations
│   ├── qdrant/        # Collections, indexing, search
│   └── sync.py        # Sinkronisasi antar storage
│
├── skills/            # Reusable toolset
│   ├── registry.py    # Skill registry
│   ├── file_ops.py    # File operations
│   ├── git_ops.py     # Git operations
│   └── code_ops.py    # Code analysis
│
├── tools/             # Integrasi eksekutor
│   ├── openhands.py   # OpenHands integration
│   └── sandbox.py     # Sandbox environment
│
├── api/               # FastAPI endpoints
│   ├── main.py        # Application entry point
│   ├── routes/        # Route definitions
│   ├── middleware/     # Auth, CORS, rate limiting
│   └── schemas/       # Request/Response schemas
│
├── dashboard/         # Web dashboard
│   ├── src/           # Frontend source
│   └── public/        # Static assets
│
├── workspace/         # Shared Git volume
│   └── .git/          # Git repository
│
├── plugins/           # Extension system
│   ├── loader.py      # Plugin loader
│   └── marketplace/   # Marketplace integration
│
├── docs/              # Dokumentasi
│   ├── id/            # Bahasa Indonesia
│   └── en/            # English
│
├── tests/             # Test suite
│   ├── unit/          # Unit tests
│   ├── integration/   # Integration tests
│   └── e2e/           # End-to-end tests
│
├── docker/            # Docker configurations
│   ├── Dockerfile     # Main Dockerfile
│   └── compose.yml    # Docker Compose
│
├── pyproject.toml     # Project configuration
└── README.md          # Project README
```

---

## 2.1.5 Data Flow Overview

```mermaid
flowchart TD
    subgraph "Input"
        A["👤 Instruksi Pengguna"]
    end

    subgraph "Processing"
        B["🔌 API Gateway"]
        C["🎯 Orchestrator"]
        D["📨 Event Bus"]
        E["🤖 Agent Pool"]
        F["🔀 Provider Router"]
        G["🧠 LLM"]
    end

    subgraph "Validation"
        H["✅ PydanticAI Validation"]
        I["🧪 QA Agent"]
        J["🔒 Security Agent"]
    end

    subgraph "Storage"
        K["📋 Knowledge Extraction"]
        L["🗄️ PostgreSQL"]
        M["🔮 Qdrant"]
        N["📂 Git Workspace"]
    end

    subgraph "Output"
        O["📊 Dashboard Update"]
        P["📝 Dokumentasi"]
    end

    A --> B --> C --> D --> E
    E --> F --> G --> H
    H --> E
    E --> I --> J
    J --> K
    K --> L
    K --> M
    E --> N
    C --> O
    E --> P

    style C fill:#2b6cb0,color:#fff
    style D fill:#d69e2e,color:#000
    style H fill:#48bb78,color:#fff
    style K fill:#e53e3e,color:#fff
```

---

## 2.1.6 Prinsip Arsitektural

| Prinsip | Implementasi |
|---------|-------------|
| **Separation of Concerns** | Setiap layer memiliki tanggung jawab tunggal yang jelas |
| **Single Source of Truth** | Project Brain (PostgreSQL + Qdrant) adalah satu-satunya sumber kebenaran |
| **Fail-Safe Design** | Automatic fallback, dead letter queues, retry mechanisms |
| **Horizontal Scalability** | Setiap komponen dapat di-scale secara independen |
| **Security by Default** | RBAC, sandboxed execution, automated security review |
| **Observable by Design** | OpenTelemetry tracing di setiap komponen |

---

🔗 **Selanjutnya:** [Execution Loop →](execution-loop.md)

🔗 **Kembali:** [Visi & Filosofi ←](../01-vision/philosophy-and-principles.md)
