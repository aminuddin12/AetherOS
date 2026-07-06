---
Status: Deprecated
Reason: Legacy architecture based on multi-agent chatbot framework (Redis, PostgreSQL, Qdrant, FastAPI, LangGraph, PydanticAI) has been replaced by the modular Operating System model (Kernel, Execution Engine, Runtime SDK, Workspace, Storage, Repository, Artifact, Organization).
Superseded By: ADR-0011 through ADR-0027, docs/id/architecture/book.md
Replacement: docs/id/architecture/book.md
---

# 04.3 — Komunikasi Antar Agen

> Dokumen ini mendeskripsikan protokol komunikasi antar agen, mekanisme serah terima tugas, Reasoning Chain, dan resolusi konflik.

---

## 4.3.1 Protokol Komunikasi

Agen dalam AetherOS **tidak berkomunikasi secara langsung**. Semua komunikasi melewati Event Bus (Redis Streams), memastikan decoupling total.

```mermaid
graph LR
    A1["🤖 Agent A"] -->|"Publish event"| EB["📨 Event Bus<br/>(Redis Streams)"]
    EB -->|"Consume event"| A2["🤖 Agent B"]
    A2 -->|"Publish result"| EB
    EB -->|"Consume result"| A1

    style EB fill:#dc382d,color:#fff
```

### Message Protocol

Setiap pesan antar agen mengikuti format standar:

| Field | Tipe | Deskripsi |
|-------|------|-----------|
| `message_id` | UUID | Identifier unik pesan |
| `correlation_id` | UUID | ID untuk menghubungkan request-response |
| `trace_id` | string | OpenTelemetry TraceID |
| `source_agent` | string | Agen pengirim |
| `target_role` | string | Peran agen tujuan |
| `message_type` | Enum | task_assignment, task_result, information_request, handover |
| `priority` | Enum | critical, high, normal, low |
| `payload` | JSON | Data spesifik per tipe pesan |
| `timestamp` | ISO 8601 | Waktu pengiriman |
| `ttl` | integer | Time-to-live dalam detik |
| `requires_ack` | bool | Apakah memerlukan acknowledgment |

---

## 4.3.2 Pola Komunikasi

### Request-Response (via Event Bus)

```mermaid
sequenceDiagram
    participant MGR as 👔 Manager
    participant EB as 📨 Event Bus
    participant BKD as ⚙️ Backend

    MGR->>EB: TASK_ASSIGNED (correlation_id: abc-123)
    EB->>BKD: Deliver task
    BKD->>BKD: Eksekusi task
    BKD->>EB: TASK_COMPLETED (correlation_id: abc-123)
    EB->>MGR: Deliver result
    Note over MGR: Cocokkan correlation_id<br/>untuk menghubungkan<br/>request-response
```

### Fan-out (Satu ke Banyak)

```mermaid
sequenceDiagram
    participant MGR as 👔 Manager
    participant EB as 📨 Event Bus
    participant QA as 🧪 QA
    participant SEC as 🔒 Security
    participant DOC as 📝 Docs

    MGR->>EB: TASK_ASSIGNED (target: qa)
    MGR->>EB: TASK_ASSIGNED (target: security)
    MGR->>EB: TASK_ASSIGNED (target: docs)

    par Paralel Execution
        EB->>QA: Deliver task
        EB->>SEC: Deliver task
        EB->>DOC: Deliver task
    end

    QA->>EB: TASK_COMPLETED
    SEC->>EB: TASK_COMPLETED
    DOC->>EB: TASK_COMPLETED
    EB->>MGR: All results
```

### Pipeline (Berurutan)

```mermaid
sequenceDiagram
    participant ARC as 📐 Architect
    participant EB as 📨 Event Bus
    participant BKD as ⚙️ Backend
    participant QA as 🧪 QA

    ARC->>EB: TASK_COMPLETED (spec ready)
    EB->>BKD: Trigger: implement spec
    BKD->>BKD: Implement
    BKD->>EB: TASK_COMPLETED (code ready)
    EB->>QA: Trigger: test code
    QA->>QA: Test
    QA->>EB: TASK_COMPLETED (test results)
```

---

## 4.3.3 Agent Handover Protocol

### Kapan Handover Terjadi

| Skenario | Dari | Ke | Trigger |
|----------|------|-----|---------|
| Spec selesai, mulai implementasi | Architect | Backend | TASK_COMPLETED |
| Implementasi selesai, mulai testing | Backend | QA | TASK_COMPLETED |
| Kode selesai, review keamanan | Backend | Security | TASK_COMPLETED |
| Semua validasi lulus, deploy | Manager | DevOps | All validations passed |
| Agen gagal, reassign | Worker (gagal) | Worker (baru) | TASK_FAILED + max_retries |

### Handover Data Package

Saat serah terima, agen pengirim menyiapkan paket data yang berisi:

| Data | Deskripsi |
|------|-----------|
| `task_context` | Konteks lengkap tugas |
| `artifacts_produced` | Daftar file yang dihasilkan/dimodifikasi |
| `decisions_made` | Keputusan yang dibuat selama eksekusi |
| `dependencies_resolved` | Dependensi yang telah diselesaikan |
| `warnings` | Peringatan atau catatan untuk agen penerima |
| `reasoning_chain` | Langkah-langkah berpikir yang mengarah ke hasil |

### Alur Handover

```mermaid
sequenceDiagram
    participant A1 as 🤖 Agent Pengirim
    participant EB as 📨 Event Bus
    participant PB as 🗄️ Project Brain
    participant A2 as 🤖 Agent Penerima

    A1->>PB: Simpan artifacts + reasoning chain
    A1->>EB: Publish HANDOVER event
    Note over EB: Event berisi:<br/>- task_id<br/>- handover_package<br/>- next_action

    EB->>A2: Deliver HANDOVER
    A2->>PB: Load konteks tambahan
    A2->>A2: Merge konteks + handover package
    A2->>A2: Mulai eksekusi
    A2->>EB: ACK: Handover diterima
```

---

## 4.3.4 Reasoning Chain

### Struktur

Setiap agen wajib mendokumentasikan langkah-langkah berpikir dalam Reasoning Chain. Ini memungkinkan traceability dan debugging.

| Field | Tipe | Deskripsi |
|-------|------|-----------|
| `step_number` | integer | Urutan langkah |
| `action` | string | Aksi yang dilakukan |
| `rationale` | string | Justifikasi untuk aksi ini |
| `input` | JSON | Input yang digunakan |
| `output` | JSON | Output yang dihasilkan |
| `confidence` | float | Tingkat kepercayaan (0.0 - 1.0) |
| `alternatives_considered` | list | Alternatif yang dipertimbangkan |
| `timestamp` | ISO 8601 | Waktu langkah |

### Contoh Reasoning Chain

```mermaid
graph TD
    S1["Step 1: Analisis Instruksi<br/>Rationale: Pahami requirement<br/>Confidence: 0.95"]
    S2["Step 2: Query Project Brain<br/>Rationale: Cek arsitektur existing<br/>Confidence: 0.90"]
    S3["Step 3: Pilih Design Pattern<br/>Rationale: Repository pattern cocok<br/>Alternatives: Active Record, DAO<br/>Confidence: 0.85"]
    S4["Step 4: Implementasi<br/>Rationale: Ikuti spec Architect<br/>Confidence: 0.90"]
    S5["Step 5: Self-Test<br/>Rationale: Validasi sebelum submit<br/>Confidence: 0.95"]

    S1 --> S2 --> S3 --> S4 --> S5

    style S1 fill:#4299e1,color:#fff
    style S3 fill:#ed8936,color:#fff
    style S5 fill:#48bb78,color:#fff
```

---

## 4.3.5 Resolusi Konflik

### Jenis Konflik

| Konflik | Contoh | Strategi |
|---------|--------|----------|
| **File Conflict** | Dua agen memodifikasi file yang sama | File locking + antrian berbasis timestamp |
| **Design Conflict** | Architect dan Backend tidak setuju tentang pattern | Escalate ke Manager |
| **Resource Conflict** | Dua agen memerlukan resource yang sama | Backoff + queue |
| **Output Conflict** | QA dan Security memberikan verdict berbeda | Manager membuat keputusan akhir |
| **Priority Conflict** | Dua task urgent bersaing untuk satu agen | Manager re-prioritize |

### Alur Resolusi

```mermaid
graph TD
    CONFLICT["⚡ Konflik Terdeteksi"]
    CONFLICT --> AUTO{"Dapat diselesaikan<br/>secara otomatis?"}

    AUTO -->|Ya: File lock, queue| RESOLVE_AUTO["🤖 Resolusi Otomatis<br/>Timestamp-based priority"]
    AUTO -->|Tidak: Design disagreement| ESCALATE["⬆️ Escalate ke Manager"]

    ESCALATE --> MGR{"Manager<br/>dapat memutuskan?"}
    MGR -->|Ya| RESOLVE_MGR["👔 Manager Decision<br/>Berdasarkan project goals"]
    MGR -->|Tidak: Terlalu kompleks| HITL["👤 HITL Checkpoint<br/>Manusia memutuskan"]

    RESOLVE_AUTO --> LOG["📊 Log resolusi"]
    RESOLVE_MGR --> LOG
    HITL --> LOG

    style CONFLICT fill:#e53e3e,color:#fff
    style RESOLVE_AUTO fill:#48bb78,color:#fff
    style RESOLVE_MGR fill:#4299e1,color:#fff
    style HITL fill:#805ad5,color:#fff
```

---

🔗 **Selanjutnya:** [RBAC & Permissions →](rbac-and-permissions.md)

🔗 **Kembali:** [Katalog Agen ←](agent-catalog.md)
