---
Status: Deprecated
Reason: Legacy architecture based on multi-agent chatbot framework (Redis, PostgreSQL, Qdrant, FastAPI, LangGraph, PydanticAI) has been replaced by the modular Operating System model (Kernel, Execution Engine, Runtime SDK, Workspace, Storage, Repository, Artifact, Organization).
Superseded By: ADR-0011 through ADR-0027, docs/id/architecture/book.md
Replacement: docs/id/architecture/book.md
---

# 03.1 — Arsitektur Memori

> Dokumen ini mendeskripsikan desain memori AetherOS, termasuk pembagian Short-term dan Long-term memory, proses distilasi pengetahuan, dan mekanisme sinkronisasi.

---

## 3.1.1 Filosofi Memori AetherOS

Memori dalam AetherOS dirancang berdasarkan analogi memori manusia:

| Memori Manusia | AetherOS | Karakteristik |
|----------------|----------|---------------|
| **Working Memory** | Graph State (LangGraph) | Kapasitas terbatas, aktif selama tugas berjalan, cepat diakses |
| **Short-term Memory** | Redis Cache | Kapasitas sedang, bertahan selama sesi, akses cepat |
| **Long-term Memory** | Project Brain (PG + Qdrant) | Kapasitas tak terbatas, permanen, akses terindeks |
| **Episodic Memory** | Meeting Memory (Qdrant) | Rekaman interaksi dan konteks percakapan |
| **Semantic Memory** | Knowledge Base (PG + Qdrant) | Fakta, aturan, dan pola yang terabstraksi |

---

## 3.1.2 Arsitektur Tiga Lapis

```mermaid
graph TD
    subgraph "Layer 1: Working Memory (In-Process)"
        WM["📝 LangGraph Graph State<br/>Lifetime: Durasi tugas<br/>Kapasitas: Context window LLM<br/>Penyimpanan: RAM"]
    end

    subgraph "Layer 2: Session Memory (Shared Cache)"
        SM["⚡ Redis Cache<br/>Lifetime: Durasi sesi<br/>Kapasitas: Dikonfigurasi (default 1GB)<br/>Penyimpanan: Redis"]
    end

    subgraph "Layer 3: Persistent Memory (Project Brain)"
        PM_PG["🗄️ PostgreSQL<br/>Lifetime: Permanen<br/>Kapasitas: Tak terbatas<br/>Data: Terstruktur"]
        PM_QD["🔮 Qdrant<br/>Lifetime: Permanen<br/>Kapasitas: Tak terbatas<br/>Data: Vektor"]
    end

    WM -->|"Distilasi<br/>(setiap akhir task)"| SM
    SM -->|"Commit<br/>(setiap akhir sesi)"| PM_PG
    SM -->|"Indexing<br/>(setiap akhir sesi)"| PM_QD
    PM_PG -->|"Context Injection<br/>(awal task baru)"| WM
    PM_QD -->|"Semantic Retrieval<br/>(awal task baru)"| WM

    style WM fill:#4299e1,color:#fff
    style SM fill:#ed8936,color:#fff
    style PM_PG fill:#336791,color:#fff
    style PM_QD fill:#805ad5,color:#fff
```

---

## 3.1.3 Working Memory — LangGraph Graph State

### Fungsi
Menyimpan konteks aktif selama satu tugas sedang dieksekusi oleh agen. Ini adalah memori "sadar" — informasi yang langsung relevan dengan tugas yang sedang dikerjakan.

### Isi Working Memory

| Data | Deskripsi | Sumber |
|------|-----------|--------|
| Task specification | Definisi tugas yang sedang dikerjakan | State Machine |
| Injected context | Konteks relevan dari Project Brain | Knowledge Retrieval |
| Current code state | Status kode di workspace saat ini | Workspace Git |
| Reasoning chain | Langkah-langkah berpikir agen sejauh ini | Agent runtime |
| Tool outputs | Hasil eksekusi tool (file read, command output) | OpenHands |
| Intermediate results | Hasil sementara dari langkah-langkah sebelumnya | Agent runtime |

### Lifecycle

```mermaid
sequenceDiagram
    participant PB as 🗄️ Project Brain
    participant WM as 📝 Working Memory
    participant Agent as 🤖 Agent
    participant KEL as 📋 Knowledge<br/>Extraction

    Note over WM: 1. INISIALISASI
    PB->>WM: Context Injection (konteks relevan)
    WM->>WM: Load task specification

    Note over WM: 2. AKTIF (selama eksekusi)
    loop Setiap langkah reasoning
        Agent->>WM: Update reasoning chain
        Agent->>WM: Simpan tool outputs
        Agent->>WM: Simpan intermediate results
    end

    Note over WM: 3. DISTILASI (akhir task)
    WM->>KEL: Kirim seluruh working memory
    KEL->>KEL: Ekstraksi pengetahuan terstruktur
    KEL->>PB: Simpan ke Long-term Memory

    Note over WM: 4. CLEANUP
    WM->>WM: Clear working memory
```

### Batasan dan Manajemen

| Constraint | Strategi |
|------------|----------|
| Context window terbatas | Sliding window: hanya pertahankan konteks paling relevan |
| Token budget | Alokasikan token: 30% konteks, 50% reasoning, 20% output |
| Memory overflow | Evict konteks lama, pertahankan yang paling baru dan relevan |

---

## 3.1.4 Session Memory — Redis Cache

### Fungsi
Menyimpan data yang perlu dibagikan antar agen selama satu sesi kerja, tetapi tidak perlu disimpan secara permanen.

### Data yang Disimpan

| Key Pattern | Data | TTL |
|-------------|------|-----|
| `session:{id}:context` | Konteks sesi yang dibagikan | 24 jam |
| `session:{id}:agent:{role}:state` | State terakhir agen | 24 jam |
| `task:{id}:cache` | Cache hasil intermediari | 1 jam |
| `lock:{resource}` | Distributed locks | 5 menit |
| `rate:{provider}:{agent}` | Rate limiting counters | 1 menit |

---

## 3.1.5 Long-term Memory — Project Brain

### Dual Storage Strategy

```mermaid
graph LR
    subgraph "Keputusan: Di mana menyimpan?"
        DATA["📦 Data Baru"]
        CHECK{"Apakah data<br/>terstruktur dan<br/>dapat di-query<br/>dengan SQL?"}
    end

    CHECK -->|Ya| PG["🗄️ PostgreSQL<br/>• Keputusan arsitektur<br/>• Task records<br/>• Audit logs<br/>• Agent profiles<br/>• Knowledge entries"]
    CHECK -->|Tidak| QD["🔮 Qdrant<br/>• Code embeddings<br/>• Conversation history<br/>• Meeting transcripts<br/>• Documentation chunks<br/>• Pattern library"]

    PG -->|"ID reference"| LINK["🔗 Cross-reference<br/>via foreign key"]
    QD -->|"metadata.pg_id"| LINK

    style PG fill:#336791,color:#fff
    style QD fill:#805ad5,color:#fff
    style LINK fill:#48bb78,color:#fff
```

🔗 Detail PostgreSQL: [Skema PostgreSQL →](postgresql-schema.md)

🔗 Detail Qdrant: [Desain Vektor Qdrant →](qdrant-vector-design.md)

---

## 3.1.6 Proses Distilasi Pengetahuan

### Knowledge Extraction Layer (KEL)

Proses distilasi adalah mekanisme inti yang memastikan pengetahuan tidak hilang saat sesi berakhir. KEL berjalan di akhir setiap siklus tugas.

```mermaid
flowchart TD
    INPUT["📥 Input: Working Memory<br/>(reasoning chain, tool outputs, results)"]

    INPUT --> CLASSIFY["🏷️ Klasifikasi Pengetahuan"]

    CLASSIFY --> ARCH["📐 Architectural Decision<br/>Keputusan tentang desain sistem"]
    CLASSIFY --> RULE["📏 Business Rule<br/>Aturan domain bisnis"]
    CLASSIFY --> PATTERN["🔄 Code Pattern<br/>Pola implementasi yang berulang"]
    CLASSIFY --> CONTEXT["💬 Conversational Context<br/>Konteks diskusi dan intent"]
    CLASSIFY --> SPEC["📋 Technical Spec<br/>Spesifikasi API, schema, contract"]
    CLASSIFY --> REASON["🧠 Reasoning Chain<br/>Proses berpikir dan justifikasi"]

    ARCH --> JSON1["📄 Structured JSON"]
    RULE --> JSON1
    SPEC --> JSON1
    REASON --> JSON1

    PATTERN --> EMBED["🔮 Vector Embedding"]
    CONTEXT --> EMBED

    JSON1 --> PG["🗄️ PostgreSQL"]
    EMBED --> QD["🔮 Qdrant"]

    style INPUT fill:#4299e1,color:#fff
    style CLASSIFY fill:#ed8936,color:#fff
    style PG fill:#336791,color:#fff
    style QD fill:#805ad5,color:#fff
```

### Format Output Distilasi

Setiap entry pengetahuan yang dihasilkan KEL mengikuti format standar:

| Field | Tipe | Deskripsi |
|-------|------|-----------|
| `knowledge_id` | UUID | Identifier unik |
| `project_id` | UUID | Proyek yang menghasilkan |
| `category` | Enum | Kategori pengetahuan |
| `title` | String | Judul ringkas |
| `content` | JSON | Konten terstruktur |
| `source_task_id` | UUID | Task yang menghasilkan pengetahuan ini |
| `source_agent` | String | Agen yang menghasilkan |
| `confidence` | Float | Tingkat kepercayaan (0.0 - 1.0) |
| `tags` | List | Tag untuk pencarian |
| `created_at` | Timestamp | Waktu pembuatan |
| `supersedes` | UUID | Jika ini menggantikan entry lama |

---

## 3.1.7 Context Injection — Retrieval untuk Agen Baru

### Skenario

Ketika agen baru memulai tugas, ia memerlukan konteks dari riwayat proyek. Context Injection mengambil pengetahuan relevan dari Project Brain dan menyuntikkannya ke Working Memory.

### Alur Context Injection

```mermaid
sequenceDiagram
    participant Agent as 🤖 New Agent
    participant CR as 🔍 Context Retriever
    participant PG as 🗄️ PostgreSQL
    participant QD as 🔮 Qdrant
    participant WM as 📝 Working Memory

    Agent->>CR: Request context untuk task
    CR->>PG: Query: keputusan arsitektur relevan
    CR->>QD: Semantic search: kode dan konteks terkait
    PG-->>CR: Structured knowledge entries
    QD-->>CR: Relevant embeddings + similarity scores

    CR->>CR: Ranking dan filtering
    CR->>CR: Deduplikasi
    CR->>CR: Token budget allocation

    CR->>WM: Injeksi konteks terstruktur
    WM->>Agent: Konteks siap digunakan
```

### Strategi Retrieval

| Strategi | Deskripsi |
|----------|-----------|
| **Keyword matching** | Cocokkan kata kunci dari task description dengan knowledge entries |
| **Semantic search** | Cari embedding terdekat di Qdrant menggunakan cosine similarity |
| **Recency bias** | Berikan bobot lebih tinggi pada pengetahuan terbaru |
| **Relevance filtering** | Filter berdasarkan project_id, kategori, dan tags |
| **Token budgeting** | Batasi total konteks agar tidak melebihi alokasi token |

---

## 3.1.8 Sinkronisasi Memori

### Outbox Pattern

Untuk menjamin konsistensi antara PostgreSQL dan Qdrant, AetherOS menggunakan Outbox Pattern:

```mermaid
sequenceDiagram
    participant KEL as 📋 KEL
    participant PG as 🗄️ PostgreSQL
    participant OUTBOX as 📤 Outbox Table
    participant WORKER as 🔄 Sync Worker
    participant QD as 🔮 Qdrant

    KEL->>PG: BEGIN TRANSACTION
    KEL->>PG: INSERT knowledge_entry
    KEL->>OUTBOX: INSERT outbox_event (type: INDEX_VECTOR)
    KEL->>PG: COMMIT TRANSACTION

    Note over OUTBOX,WORKER: Async processing

    WORKER->>OUTBOX: Poll for unprocessed events
    OUTBOX-->>WORKER: Pending events
    WORKER->>QD: Index vector embedding
    QD-->>WORKER: Success
    WORKER->>OUTBOX: Mark as processed
```

### Conflict Resolution

| Konflik | Strategi |
|---------|----------|
| Duplicate knowledge entry | Merge berdasarkan timestamp terbaru |
| Contradicting entries | Simpan keduanya, tandai sebagai "conflicting", escalate ke Manager |
| Stale context injection | TTL-based invalidation, verifikasi terhadap state terkini |
| Storage failure | Retry dengan exponential backoff, fallback ke queue |

---

🔗 **Selanjutnya:** [Skema PostgreSQL →](postgresql-schema.md)

🔗 **Kembali:** [Orkestrasi State Machine ←](../02-architecture/state-machine-orchestration.md)
