# 02.2 — Execution Loop (Siklus Eksekusi)

> Dokumen ini mendeskripsikan 7 tahap siklus eksekusi AetherOS secara detail, termasuk error handling, retry policies, dan contoh skenario end-to-end.

---

## 2.2.1 Gambaran Umum

Berbeda dengan sistem linier yang memproses instruksi secara sekuensial, AetherOS beroperasi dalam **feedback loop berkelanjutan**. Setiap instruksi melewati 7 tahap yang saling terhubung, di mana output dari satu siklus menjadi input untuk siklus berikutnya melalui enrichment dari Project Brain.

```mermaid
graph TD
    A["1️⃣ INGESTION<br/>Penerimaan Instruksi"] --> B["2️⃣ ORCHESTRATION<br/>Dekomposisi & Perencanaan"]
    B --> C["3️⃣ DISTRIBUTION<br/>Penyebaran Tugas"]
    C --> D["4️⃣ EXECUTION<br/>Eksekusi Agen"]
    D --> E["5️⃣ VALIDATION<br/>Validasi & Distilasi"]
    E --> F["6️⃣ PERSISTENCE<br/>Penyimpanan Permanen"]
    F --> G["7️⃣ FEEDBACK<br/>Pembaruan Status"]
    G -.->|"Siklus berikutnya<br/>(dengan konteks diperkaya)"| A

    style A fill:#4299e1,color:#fff
    style B fill:#ed8936,color:#fff
    style C fill:#ecc94b,color:#000
    style D fill:#48bb78,color:#fff
    style E fill:#38b2ac,color:#fff
    style F fill:#9f7aea,color:#fff
    style G fill:#ed64a6,color:#fff
```

---

## 2.2.2 Tahap 1: INGESTION — Penerimaan Instruksi

### Deskripsi
Instruksi masuk ke sistem melalui salah satu antarmuka yang tersedia: Web Dashboard, CLI, atau REST API. Pada tahap ini, instruksi mentah divalidasi, diperkaya dengan konteks, dan dikonversi ke format internal.

### Alur Detail

```mermaid
sequenceDiagram
    participant User as 👤 Pengguna
    participant IF as 🔌 Interface<br/>(Dashboard/CLI/API)
    participant VAL as ✅ Input Validator
    participant CTX as 🧠 Context Enricher
    participant ORCH as 🎯 Orchestrator

    User->>IF: Kirim instruksi
    IF->>VAL: Validasi format & autentikasi
    alt Validasi gagal
        VAL-->>IF: Error: Invalid input
        IF-->>User: Tampilkan error
    else Validasi berhasil
        VAL->>CTX: Instruksi tervalidasi
        CTX->>CTX: Query Project Brain untuk konteks relevan
        CTX->>CTX: Attach metadata (user, timestamp, priority)
        CTX->>ORCH: Instruksi + Konteks
    end
```

### Komponen yang Terlibat

| Komponen | Fungsi |
|----------|--------|
| **Input Validator** | Memvalidasi format instruksi, autentikasi pengguna, dan otorisasi akses |
| **Context Enricher** | Mengambil konteks relevan dari Project Brain (riwayat tugas terkait, keputusan arsitektur, dll.) |
| **Metadata Injector** | Menambahkan informasi meta: TraceID, timestamp, user identity, priority level |

### Error Handling

| Error | Aksi |
|-------|------|
| Format instruksi tidak valid | Return error 400 dengan panduan format yang benar |
| Autentikasi gagal | Return error 401, log upaya akses |
| Context Enricher timeout | Lanjutkan tanpa konteks tambahan, tandai sebagai "low-context" |
| Project Brain tidak tersedia | Lanjutkan dengan konteks minimal, alert ke monitoring |

---

## 2.2.3 Tahap 2: ORCHESTRATION — Dekomposisi dan Perencanaan

### Deskripsi
Manager Agent menerima instruksi yang telah diperkaya konteks, lalu mendekomposisinya menjadi rencana kerja terstruktur. Rencana ini disimpan sebagai state dalam LangGraph State Machine.

### Alur Detail

```mermaid
sequenceDiagram
    participant ORCH as 🎯 Orchestrator
    participant MGR as 👔 Manager Agent
    participant LLM as 🧠 LLM
    participant SM as 📋 State Machine
    participant PB as 🗄️ Project Brain

    ORCH->>MGR: Instruksi + Konteks
    MGR->>PB: Query: skill registry, agen tersedia, kapasitas
    PB-->>MGR: Data agen dan kapabilitas
    MGR->>LLM: Instruksi + Konteks + Data agen
    LLM-->>MGR: Rencana dekomposisi (validated by PydanticAI)
    MGR->>SM: Simpan rencana sebagai state graph
    SM->>SM: Inisialisasi checkpoints
    SM-->>MGR: State ID + Task graph
    MGR->>ORCH: Rencana siap didistribusikan
```

### Proses Dekomposisi

Manager Agent memecah instruksi menjadi task graph — sebuah DAG (Directed Acyclic Graph) yang mendefinisikan urutan dan dependensi antar tugas:

```mermaid
graph TD
    PROJ["📋 Instruksi Proyek:<br/>'Bangun REST API untuk manajemen user'"]

    T1["Task 1: Definisi Schema<br/>👤 Architect<br/>Priority: Critical"]
    T2["Task 2: Implementasi Model<br/>👤 Backend<br/>Depends: T1"]
    T3["Task 3: Implementasi Endpoints<br/>👤 Backend<br/>Depends: T1"]
    T4["Task 4: Unit Tests<br/>👤 QA<br/>Depends: T2, T3"]
    T5["Task 5: Security Review<br/>👤 Security<br/>Depends: T3"]
    T6["Task 6: Dokumentasi API<br/>👤 Documentation<br/>Depends: T3"]
    T7["Task 7: Integration Test<br/>👤 QA<br/>Depends: T4, T5"]

    PROJ --> T1
    T1 --> T2
    T1 --> T3
    T2 --> T4
    T3 --> T4
    T3 --> T5
    T3 --> T6
    T4 --> T7
    T5 --> T7

    style PROJ fill:#2b6cb0,color:#fff
    style T1 fill:#e53e3e,color:#fff
    style T7 fill:#48bb78,color:#fff
```

### State Machine Transitions

| State | Kondisi Transisi | State Berikutnya |
|-------|-----------------|------------------|
| `PLANNING` | Rencana dekomposisi selesai dan valid | `DISTRIBUTING` |
| `DISTRIBUTING` | Semua tugas telah di-assign | `EXECUTING` |
| `EXECUTING` | Semua tugas selesai | `VALIDATING` |
| `VALIDATING` | Semua validasi lulus | `PERSISTING` |
| `PERSISTING` | Data tersimpan | `COMPLETED` |
| Any State | Error kritis | `FAILED` |
| Any State | Memerlukan persetujuan manusia | `AWAITING_APPROVAL` |

---

## 2.2.4 Tahap 3: DISTRIBUTION — Penyebaran Tugas

### Deskripsi
Tugas-tugas yang telah didekomposisi disebarkan melalui Event Bus (Redis Streams) ke agen pekerja yang sesuai. Distribusi mempertimbangkan dependensi antar tugas, kapasitas agen, dan prioritas.

### Alur Detail

```mermaid
sequenceDiagram
    participant MGR as 👔 Manager
    participant EB as 📨 Event Bus<br/>(Redis Streams)
    participant CG as 👥 Consumer Group
    participant W1 as 🤖 Architect
    participant W2 as ⚙️ Backend
    participant W3 as 🧪 QA

    MGR->>EB: Publish: TASK_ASSIGNED (Task 1 → Architect)
    EB->>CG: Route ke consumer group "architect"
    CG->>W1: Deliver Task 1
    W1-->>EB: ACK: Task 1 diterima

    Note over MGR,EB: Tunggu Task 1 selesai (dependency)

    W1-->>EB: Publish: TASK_COMPLETED (Task 1)
    EB->>MGR: Notify: Task 1 selesai
    MGR->>EB: Publish: TASK_ASSIGNED (Task 2 → Backend)
    MGR->>EB: Publish: TASK_ASSIGNED (Task 3 → Backend)
    EB->>CG: Route ke consumer group "backend"
    CG->>W2: Deliver Task 2 & 3 (paralel)
```

### Strategi Distribusi

| Strategi | Deskripsi |
|----------|-----------|
| **Dependency-Aware** | Tugas hanya dikirim setelah semua dependensinya selesai |
| **Priority-Based** | Tugas dengan prioritas tinggi didistribusikan lebih dulu |
| **Load-Balanced** | Jika ada multiple instances dari satu peran, tugas dibagi rata |
| **Retry-Enabled** | Jika agen gagal memproses, tugas dikirim ulang ke instansi lain |

---

## 2.2.5 Tahap 4: EXECUTION — Eksekusi Agen

### Deskripsi
Worker Agents mengeksekusi tugas di dalam Shared Workspace menggunakan OpenHands sebagai Tool Execution Layer. Setiap agen bekerja dalam sandbox yang terisolasi dengan akses terbatas sesuai RBAC.

### Alur Detail

```mermaid
sequenceDiagram
    participant Agent as 🤖 Worker Agent
    participant OH as 🔧 OpenHands<br/>(Tool Layer)
    participant WS as 📂 Workspace
    participant LLM as 🧠 LLM
    participant PB as 🗄️ Project Brain
    participant EB as 📨 Event Bus

    Agent->>PB: Query: konteks relevan untuk task
    PB-->>Agent: Konteks (arsitektur, kode existing, aturan)
    Agent->>LLM: Instruksi + Konteks + Tools available
    LLM-->>Agent: Respons: rencana aksi + kode

    loop Setiap aksi dalam rencana
        Agent->>OH: Eksekusi aksi (write file, run command)
        OH->>WS: Operasi file/terminal dalam sandbox
        WS-->>OH: Hasil operasi
        OH-->>Agent: Status: sukses/gagal
    end

    Agent->>WS: Git commit (atomic, dengan TraceID)
    Agent->>EB: Publish: TASK_COMPLETED + artifacts
```

### Sandbox Environment

Setiap agen beroperasi dalam lingkungan yang terisolasi:

| Batasan | Deskripsi |
|---------|-----------|
| **File System** | Akses hanya ke direktori yang diizinkan oleh RBAC |
| **Network** | Dibatasi ke internal services saja (kecuali DevOps) |
| **Execution Time** | Timeout per-task untuk mencegah infinite loops |
| **Resource Limits** | CPU dan memory limits per agen |
| **Git Access** | Hanya dapat commit ke feature branch, bukan main |

---

## 2.2.6 Tahap 5: VALIDATION & DISTILLATION — Validasi dan Distilasi

### Deskripsi
Setelah eksekusi selesai, hasil kerja melewati dua proses: (1) Validasi oleh agen QA dan Security, (2) Distilasi pengetahuan teknis untuk disimpan ke Project Brain.

### Alur Validasi

```mermaid
graph TD
    RESULT["📦 Hasil Eksekusi"] --> QA_CHECK["🧪 QA Agent<br/>Unit Tests + Regression"]
    RESULT --> SEC_CHECK["🔒 Security Agent<br/>Static Analysis + Vulnerability Scan"]

    QA_CHECK -->|Lulus| QA_PASS["✅ QA Passed"]
    QA_CHECK -->|Gagal| QA_FAIL["❌ QA Failed"]
    SEC_CHECK -->|Lulus| SEC_PASS["✅ Security Passed"]
    SEC_CHECK -->|Gagal| SEC_FAIL["❌ Security Failed"]

    QA_PASS --> GATE["🚪 Validation Gate"]
    SEC_PASS --> GATE
    QA_FAIL --> RETRY["🔄 Kirim kembali ke agen<br/>dengan feedback error"]
    SEC_FAIL --> RETRY

    GATE -->|Semua lulus| DISTILL["📋 Knowledge Distillation"]
    RETRY --> RESULT

    DISTILL --> JSON["📄 Structured JSON<br/>(Keputusan, Pola, Aturan)"]
    DISTILL --> EMBED["🔮 Vector Embeddings<br/>(Konteks, Dokumentasi)"]

    style GATE fill:#48bb78,color:#fff
    style DISTILL fill:#e53e3e,color:#fff
```

### Proses Distilasi

Knowledge Extraction Layer memproses output agen dan mengekstraksi:

| Output Distilasi | Format | Penyimpanan |
|-----------------|--------|-------------|
| Keputusan arsitektur | Structured JSON | PostgreSQL |
| Pattern yang digunakan | Structured JSON | PostgreSQL |
| Kode dan implementasi | Vector embedding | Qdrant |
| Reasoning chain | Structured JSON | PostgreSQL |
| Dokumentasi | Vector embedding | Qdrant |

---

## 2.2.7 Tahap 6: PERSISTENCE — Penyimpanan Permanen

### Deskripsi
Data yang telah divalidasi dan didistilasi disimpan secara permanen di Project Brain. PostgreSQL menyimpan data terstruktur (relasional), Qdrant menyimpan embedding vektor, dan Git menyimpan kode sumber.

### Strategi Penyimpanan

```mermaid
graph LR
    subgraph "Data Terstruktur"
        PG["🗄️ PostgreSQL"]
        PG1["Task records"]
        PG2["Audit logs"]
        PG3["Knowledge entries"]
        PG4["Agent profiles"]
        PG --> PG1
        PG --> PG2
        PG --> PG3
        PG --> PG4
    end

    subgraph "Data Vektor"
        QD["🔮 Qdrant"]
        QD1["Code embeddings"]
        QD2["Conversation history"]
        QD3["Meeting memory"]
        QD4["Documentation"]
        QD --> QD1
        QD --> QD2
        QD --> QD3
        QD --> QD4
    end

    subgraph "Kode Sumber"
        GIT["📂 Git"]
        GIT1["Feature branches"]
        GIT2["Atomic commits"]
        GIT3["TraceID in messages"]
        GIT --> GIT1
        GIT --> GIT2
        GIT --> GIT3
    end

    style PG fill:#336791,color:#fff
    style QD fill:#805ad5,color:#fff
    style GIT fill:#f05032,color:#fff
```

### Konsistensi Data

| Mekanisme | Deskripsi |
|-----------|-----------|
| **Transactional Writes** | PostgreSQL menggunakan transaksi ACID untuk menjamin konsistensi |
| **Write-Ahead Logging** | Perubahan dicatat sebelum dieksekusi untuk crash recovery |
| **Dual-Write Prevention** | Menggunakan outbox pattern untuk menghindari inkonsistensi antara PG dan Qdrant |
| **Immutable Records** | Audit logs bersifat append-only, tidak dapat dihapus atau dimodifikasi |

---

## 2.2.8 Tahap 7: FEEDBACK — Pembaruan Status

### Deskripsi
Status terbaru diperbarui ke Dashboard untuk visibilitas manusia. Jika diperlukan intervensi (misalnya HITL checkpoint), sistem menunggu sinyal persetujuan sebelum melanjutkan.

### Jenis Feedback

| Jenis | Target | Aksi |
|-------|--------|------|
| **Progress Update** | Dashboard | Memperbarui progress bar dan task status |
| **Completion Report** | Dashboard + CLI | Menampilkan ringkasan hasil kerja |
| **Approval Request** | Dashboard (HITL) | Membekukan state, menunggu persetujuan manusia |
| **Error Notification** | Dashboard + Alerting | Mengirim alert jika terjadi kegagalan |
| **Cost Report** | Dashboard | Memperbarui konsumsi token dan biaya |

---

## 2.2.9 Retry dan Recovery Policies

```mermaid
graph TD
    FAIL["❌ Task Gagal"] --> CHECK["🔍 Cek Jenis Error"]

    CHECK -->|Transient Error<br/>Network, Timeout| RETRY["🔄 Retry<br/>(max 3x, exponential backoff)"]
    CHECK -->|LLM Rate Limit| FALLBACK["🔀 Fallback ke<br/>Provider Lain"]
    CHECK -->|Validation Error| FEEDBACK_LOOP["💬 Kirim feedback<br/>ke agen untuk perbaikan"]
    CHECK -->|Critical Error<br/>Data corruption| HALT["🛑 Halt + Alert<br/>Manusia"]

    RETRY -->|Berhasil| CONTINUE["✅ Lanjutkan"]
    RETRY -->|Gagal 3x| ESCALATE["⬆️ Eskalasi ke<br/>Manager Agent"]
    FALLBACK --> CONTINUE
    FEEDBACK_LOOP -->|Max 2 retry| ESCALATE
    ESCALATE --> HALT

    style FAIL fill:#e53e3e,color:#fff
    style CONTINUE fill:#48bb78,color:#fff
    style HALT fill:#742a2a,color:#fff
```

### Retry Configuration

| Parameter | Nilai Default | Deskripsi |
|-----------|--------------|-----------|
| `max_retries` | 3 | Jumlah maksimal percobaan ulang |
| `initial_backoff` | 1 detik | Waktu tunggu awal sebelum retry |
| `backoff_multiplier` | 2 | Pengali waktu tunggu (exponential) |
| `max_backoff` | 60 detik | Waktu tunggu maksimal |
| `feedback_max_retries` | 2 | Maksimal percobaan perbaikan oleh agen |
| `task_timeout` | 300 detik | Timeout per-task sebelum dianggap gagal |

---

## 2.2.10 Contoh Skenario End-to-End

### Skenario: "Bangun endpoint registrasi user dengan validasi email"

```mermaid
sequenceDiagram
    participant User as 👤 Developer
    participant Dash as 🖥️ Dashboard
    participant MGR as 👔 Manager
    participant ARC as 📐 Architect
    participant BKD as ⚙️ Backend
    participant QA as 🧪 QA
    participant SEC as 🔒 Security
    participant PB as 🗄️ Project Brain

    Note over User,PB: TAHAP 1: INGESTION
    User->>Dash: "Bangun endpoint registrasi user dengan validasi email"
    Dash->>MGR: Instruksi + konteks proyek

    Note over User,PB: TAHAP 2: ORCHESTRATION
    MGR->>MGR: Dekomposisi menjadi 4 sub-task
    MGR->>PB: Simpan task graph

    Note over User,PB: TAHAP 3: DISTRIBUTION
    MGR->>ARC: Task 1: Definisi schema User & endpoint spec
    ARC-->>MGR: Schema selesai (Pydantic model + OpenAPI spec)

    MGR->>BKD: Task 2: Implementasi endpoint + validasi email
    BKD-->>MGR: Kode selesai (controller + service + tests)

    Note over User,PB: TAHAP 4: EXECUTION (paralel)
    MGR->>QA: Task 3: Jalankan unit tests + regression
    MGR->>SEC: Task 4: Security review (injection, credential leak)

    Note over User,PB: TAHAP 5: VALIDATION
    QA-->>MGR: ✅ 12/12 tests passed
    SEC-->>MGR: ✅ No vulnerabilities found

    Note over User,PB: TAHAP 6: PERSISTENCE
    MGR->>PB: Simpan: keputusan arsitektur, kode, test results, audit log

    Note over User,PB: TAHAP 7: FEEDBACK
    MGR->>Dash: ✅ Endpoint registrasi selesai (4 tasks, 2m 34s)
    Dash->>User: Tampilkan ringkasan + link ke kode
```

---

🔗 **Selanjutnya:** [Arsitektur Event-Driven →](event-driven-architecture.md)

🔗 **Kembali:** [Gambaran Umum Sistem ←](system-overview.md)
