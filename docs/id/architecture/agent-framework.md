# 04.1 — Framework Agen

> Dokumen ini mendeskripsikan framework agen AetherOS berbasis PydanticAI, termasuk runtime lifecycle, schema validation, error handling, dan pencegahan halusinasi.

---

## 4.1.1 PydanticAI sebagai Agent Runtime

PydanticAI dipilih sebagai runtime agen karena kemampuannya memberlakukan **strict type-checking** pada input dan output LLM. Ini adalah pertahanan utama terhadap halusinasi model yang dapat merusak state sistem.

### Mengapa PydanticAI?

| Kebutuhan | Solusi PydanticAI |
|-----------|-------------------|
| Output LLM harus terstruktur | Pydantic schema enforcement pada setiap respons |
| Mencegah format yang tidak diharapkan | Validasi otomatis, reject jika tidak sesuai schema |
| Multi-model support | Built-in support untuk OpenAI, Anthropic, Ollama |
| Tool calling | Structured tool definitions dengan parameter validation |
| Retry on failure | Built-in retry logic untuk respons yang gagal validasi |

---

## 4.1.2 Agent Lifecycle

```mermaid
statediagram-v2
    [*] --> INITIALIZING
    INITIALIZING --> LOADING_CONTEXT : Load from Project Brain
    LOADING_CONTEXT --> READY : Context loaded
    READY --> EXECUTING : Task received
    EXECUTING --> REASONING : LLM processing
    REASONING --> TOOL_CALLING : Tool action needed
    TOOL_CALLING --> REASONING : Tool result received
    REASONING --> VALIDATING : Response generated
    VALIDATING --> EXECUTING : Validation failed (retry)
    VALIDATING --> DISTILLING : Validation passed
    DISTILLING --> REPORTING : Knowledge extracted
    REPORTING --> READY : Task completed
    REPORTING --> TERMINATED : Shutdown signal
    EXECUTING --> ERROR_HANDLING : Error occurred
    ERROR_HANDLING --> EXECUTING : Recoverable, retry
    ERROR_HANDLING --> TERMINATED : Unrecoverable
    TERMINATED --> [*]
```

### Detail Setiap Fase

| Fase | Durasi | Aksi |
|------|--------|------|
| **INITIALIZING** | ~100ms | Inisialisasi runtime, load konfigurasi, register ke Event Bus |
| **LOADING_CONTEXT** | ~500ms-2s | Query Project Brain untuk konteks relevan, build system prompt |
| **READY** | Idle | Menunggu task dari Event Bus, health check berkala |
| **EXECUTING** | Varies | Memproses task, memanggil LLM, menggunakan tools |
| **REASONING** | ~1-30s | LLM memproses instruksi dan menghasilkan respons |
| **TOOL_CALLING** | ~100ms-5s | Eksekusi tool (file ops, git ops, dll.) via OpenHands |
| **VALIDATING** | ~50ms | PydanticAI memvalidasi output terhadap schema |
| **DISTILLING** | ~1-5s | Knowledge Extraction Layer memproses output |
| **REPORTING** | ~100ms | Publish hasil ke Event Bus, update state machine |
| **ERROR_HANDLING** | ~100ms-10s | Evaluasi error, keputusan retry atau escalate |
| **TERMINATED** | ~100ms | Cleanup resources, deregister dari Event Bus |

---

## 4.1.3 Schema Validation

### Input Schema

Setiap agen menerima input yang divalidasi terhadap schema Pydantic:

| Field | Tipe | Required | Deskripsi |
|-------|------|----------|-----------|
| `task_id` | UUID | ✅ | Identifier tugas |
| `project_id` | UUID | ✅ | Identifier proyek |
| `trace_id` | str | ✅ | OpenTelemetry TraceID |
| `instruction` | str | ✅ | Instruksi spesifik untuk agen |
| `context` | TaskContext | ✅ | Konteks dari Project Brain |
| `constraints` | TaskConstraints | ❌ | Batasan (timeout, token budget, dll.) |
| `dependencies_output` | dict | ❌ | Output dari task dependen |

### Output Schema

Output agen juga divalidasi sebelum diterima sistem:

| Field | Tipe | Required | Deskripsi |
|-------|------|----------|-----------|
| `task_id` | UUID | ✅ | Identifier tugas |
| `status` | Enum | ✅ | completed, failed, needs_review |
| `result` | TaskResult | ✅ | Hasil eksekusi |
| `artifacts` | list[Artifact] | ❌ | File yang dihasilkan/dimodifikasi |
| `reasoning_chain` | list[ReasoningStep] | ✅ | Langkah-langkah berpikir |
| `knowledge_extracted` | list[KnowledgeEntry] | ❌ | Pengetahuan yang diekstraksi |
| `metrics` | ExecutionMetrics | ✅ | Token usage, execution time |

### Validasi Multi-layer

```mermaid
graph TD
    LLM_OUT["🧠 LLM Raw Output"] --> L1["Layer 1: Format Validation<br/>Apakah output berupa JSON valid?"]
    L1 -->|Gagal| RETRY1["🔄 Retry dengan instruksi format"]
    L1 -->|Lulus| L2["Layer 2: Schema Validation<br/>Apakah sesuai Pydantic schema?"]
    L2 -->|Gagal| RETRY2["🔄 Retry dengan error detail"]
    L2 -->|Lulus| L3["Layer 3: Semantic Validation<br/>Apakah konten masuk akal?"]
    L3 -->|Gagal| RETRY3["🔄 Retry dengan feedback"]
    L3 -->|Lulus| ACCEPT["✅ Output Diterima"]

    RETRY1 -->|Max 3x| ESCALATE["⬆️ Escalate ke Manager"]
    RETRY2 -->|Max 3x| ESCALATE
    RETRY3 -->|Max 2x| ESCALATE

    style LLM_OUT fill:#ed8936,color:#fff
    style ACCEPT fill:#48bb78,color:#fff
    style ESCALATE fill:#e53e3e,color:#fff
```

---

## 4.1.4 Pencegahan Halusinasi

### Strategi Anti-Halusinasi

| Strategi | Implementasi |
|----------|-------------|
| **Schema Enforcement** | PydanticAI memvalidasi setiap field output |
| **Grounded Context** | Agen hanya menerima konteks faktual dari Project Brain |
| **Tool Verification** | Output tool (file existence, test results) diverifikasi oleh runtime |
| **Confidence Scoring** | Agen melaporkan confidence score, low-confidence di-flag |
| **Cross-Agent Verification** | Hasil agen satu diverifikasi oleh agen lain (QA, Security) |
| **Deterministic Tools** | Operasi file dan Git bersifat deterministik, verifiable |

### Mekanisme Deteksi Halusinasi

```mermaid
graph TD
    OUT["📤 Agent Output"]

    OUT --> C1{"File paths<br/>yang disebutkan<br/>ada di workspace?"}
    C1 -->|Tidak| H1["🚨 Halusinasi: File path"]

    OUT --> C2{"Function/class<br/>yang direferensi<br/>ada di codebase?"}
    C2 -->|Tidak| H2["🚨 Halusinasi: Code reference"]

    OUT --> C3{"Output sesuai<br/>dengan task<br/>yang diminta?"}
    C3 -->|Tidak| H3["🚨 Halusinasi: Off-topic"]

    OUT --> C4{"Metric klaim<br/>(test passed, etc.)<br/>dapat diverifikasi?"}
    C4 -->|Tidak| H4["🚨 Halusinasi: False claims"]

    C1 -->|Ya| OK1["✅"]
    C2 -->|Ya| OK2["✅"]
    C3 -->|Ya| OK3["✅"]
    C4 -->|Ya| OK4["✅"]

    H1 --> REJECT["❌ Reject + Retry"]
    H2 --> REJECT
    H3 --> REJECT
    H4 --> REJECT

    style REJECT fill:#e53e3e,color:#fff
```

---

## 4.1.5 Tool Integration

### Tool Definition

Setiap agen memiliki akses ke set tools yang terdefinisi dan dibatasi oleh RBAC:

| Tool | Fungsi | Agen yang Diizinkan |
|------|--------|---------------------|
| `read_file` | Baca file di workspace | Semua |
| `write_file` | Tulis/modifikasi file | Backend, Frontend, DevOps, Docs |
| `run_command` | Eksekusi terminal command | Backend, QA, DevOps |
| `git_commit` | Commit ke feature branch | Semua (kecuali Manager) |
| `git_diff` | Lihat perubahan | Semua |
| `search_code` | Pencarian di codebase | Semua |
| `query_brain` | Query Project Brain | Semua |
| `run_tests` | Jalankan test suite | QA |
| `security_scan` | Jalankan security scanner | Security |
| `deploy` | Deploy ke environment | DevOps (Level 3 HITL) |

### Tool Execution Flow

```mermaid
sequenceDiagram
    participant Agent as 🤖 Agent
    participant Runtime as ⚙️ PydanticAI Runtime
    participant RBAC as 🔐 RBAC Check
    participant OH as 🔧 OpenHands
    participant WS as 📂 Workspace

    Agent->>Runtime: Request tool: write_file("/api/users.py", content)
    Runtime->>RBAC: Cek permission: agent=backend, tool=write_file, path=/api/
    
    alt Permission denied
        RBAC-->>Runtime: ❌ Denied
        Runtime-->>Agent: Error: insufficient permissions
    else Permission granted
        RBAC-->>Runtime: ✅ Granted
        Runtime->>OH: Execute: write_file
        OH->>WS: Write file dalam sandbox
        WS-->>OH: Success
        OH-->>Runtime: Result: file written
        Runtime-->>Agent: Tool result
    end
```

---

## 4.1.6 Agent Configuration

### Per-Agent Configuration

| Parameter | Deskripsi | Default |
|-----------|-----------|---------|
| `model_preference` | Preferensi LLM (best, fast, cheap) | "best" |
| `max_tokens_per_request` | Batas token per request ke LLM | 4096 |
| `max_retries` | Maksimal retry pada validation failure | 3 |
| `task_timeout` | Timeout per task | 300s |
| `context_window_budget` | Alokasi token untuk konteks | 30% |
| `tools_enabled` | Daftar tools yang aktif | Per-role |
| `allowed_directories` | Direktori yang dapat diakses | Per-role |
| `temperature` | Kreativitas LLM | 0.1 (low) |

---

🔗 **Selanjutnya:** [Katalog Agen →](agent-catalog.md)

🔗 **Kembali:** [Desain Vektor Qdrant ←](../03-project-brain/qdrant-vector-design.md)
