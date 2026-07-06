---
Status: Deprecated
Reason: Legacy architecture based on multi-agent chatbot framework (Redis, PostgreSQL, Qdrant, FastAPI, LangGraph, PydanticAI) has been replaced by the modular Operating System model (Kernel, Execution Engine, Runtime SDK, Workspace, Storage, Repository, Artifact, Organization).
Superseded By: ADR-0011 through ADR-0027, docs/id/architecture/book.md
Replacement: docs/id/architecture/book.md
---

# 01 — Visi, Filosofi, dan Prinsip Desain

> *"The Open Agent Operating System. Build Organizations, not Agents."*

---

## 1.1 Latar Belakang dan Konteks Industri

Industri AI saat ini menghadapi paradoks fundamental: semakin canggih model LLM yang digunakan, semakin besar pula ketergantungan organisasi terhadap vendor tunggal. Ketika sebuah perusahaan membangun seluruh alur kerja di atas satu model — misalnya GPT-4 atau Claude — pengetahuan yang dihasilkan selama proses pengembangan tersimpan dalam format yang terikat pada konteks sesi model tersebut. Jika model diganti, diperbarui, atau penyedia mengubah kebijakan, organisasi kehilangan akses ke pengetahuan tersebut.

AetherOS lahir dari pemahaman bahwa **pengetahuan organisasi harus menjadi entitas mandiri** — terpisah dari mesin komputasi yang memprosesnya. Sama seperti sistem operasi tradisional yang mengabstraksi hardware dari software, AetherOS mengabstraksi model LLM dari aset intelektual yang dihasilkannya.

### Masalah yang Diselesaikan

```mermaid
mindmap
  root((Masalah Industri AI))
    Vendor Lock-in
      Ketergantungan pada satu penyedia LLM
      Migrasi model memerlukan rekonstruksi pengetahuan
      Risiko perubahan kebijakan vendor
    Knowledge Loss
      Pengetahuan terkurung dalam sesi ephemeral
      Context window terbatas dan tidak persisten
      Tidak ada mekanisme transfer pengetahuan antar model
    Koordinasi Multi-Agent
      Tidak ada standar komunikasi antar agen
      Konflik aksi tanpa mekanisme resolusi
      Observabilitas rendah terhadap proses AI
    Governance Gap
      Tidak ada audit trail untuk keputusan AI
      Kurangnya kontrol manusia atas tindakan kritikal
      Keamanan kode yang dihasilkan AI tidak terjamin
```

---

## 1.2 Visi

**AetherOS adalah "The Open Agent Operating System" — sebuah platform open-source revolusioner yang menjadi fondasi generik bagi berbagai bentuk organisasi otonom (AI Organizations) dengan kedaulatan pengetahuan penuh.**

Sebagai OS Generik, AetherOS tidak terbatas pada perusahaan software. Kernel inti AetherOS dapat menjalankan berbagai *Distribution Packs* seperti:
- **Software Company Pack**
- **Cyber Security Pack**
- **Marketing Agency Pack**
- **Research Laboratory Pack**
- **Legal Assistant Pack**

Visi ini mengandung tiga elemen kunci:

| Elemen | Deskripsi |
|--------|-----------|
| **Open-Source** | Seluruh kode sumber tersedia secara terbuka, memastikan transparansi, auditabilitas, dan kontribusi komunitas global. Tidak ada komponen proprietary yang menyebabkan lock-in. |
| **Multi-Agent Orchestration** | Bukan satu agen monolitik, melainkan organisasi dari agen-agen spesialis yang bekerja secara kolaboratif — masing-masing dengan peran, kemampuan, dan batasan akses yang jelas. |
| **Kedaulatan Pengetahuan** | Pengetahuan yang dihasilkan selama proses kerja sepenuhnya dimiliki oleh organisasi, tersimpan dalam format terstruktur yang tidak bergantung pada model LLM manapun. |

### Analogi Sistem Operasi

```mermaid
graph LR
    subgraph "Sistem Operasi Tradisional"
        HW["🖥️ Hardware<br/>(CPU, RAM, GPU)"] --> OS["⚙️ OS<br/>(Linux, Windows)"]
        OS --> APP["📱 Applications<br/>(Software)"]
    end

    subgraph "AetherOS"
        LLM["🧠 LLM<br/>(GPT, Claude, Ollama)"] --> AOS["⚙️ AetherOS<br/>(Orchestrator)"]
        AOS --> AGENT["🤖 Agents<br/>(Worker Units)"]
    end

    style HW fill:#4a5568,color:#fff
    style LLM fill:#4a5568,color:#fff
    style OS fill:#2b6cb0,color:#fff
    style AOS fill:#2b6cb0,color:#fff
    style APP fill:#2f855a,color:#fff
    style AGENT fill:#2f855a,color:#fff
```

Sama seperti OS mengabstraksi hardware sehingga aplikasi tidak perlu tahu detail CPU yang digunakan, AetherOS mengabstraksi LLM sehingga agen tidak perlu tahu model mana yang memproses instruksinya.

---

## 1.3 Misi

**Mencapai Model Agnosticism total melalui Company Brain — sebuah sumber kebenaran permanen dan kecerdasan kolektif yang memastikan pengetahuan organisasi tetap utuh dan berkembang, meskipun model LLM atau agen di bawahnya berganti.**

### Misi Operasional

1. **Memisahkan Pengetahuan dari Komputasi** — Setiap wawasan yang dihasilkan oleh LLM diekstraksi, distrukturisasi, dan disimpan dalam Company Brain sebelum sesi berakhir.
2. **Menstandarisasi Kolaborasi Multi-Agent** — Menyediakan protokol komunikasi, validasi, dan serah terima tugas yang konsisten antar agen.
3. **Menjamin Tata Kelola AI** — Setiap tindakan agen memiliki jejak audit, dan tindakan kritikal memerlukan persetujuan manusia.
4. **Mengdemokratisasi Akses** — Sebagai platform open-source, AetherOS memastikan bahwa organisasi kecil maupun besar dapat membangun perusahaan AI yang mandiri.

---

## 1.4 Prinsip Desain Inti — Empat Pilar Arsitektural

AetherOS beroperasi pada empat pilar arsitektural yang tidak dapat dikompromikan. Setiap keputusan teknis dalam sistem harus lulus uji terhadap keempat pilar ini.

### Pilar 1: LLM Agnostic

```mermaid
graph TD
    subgraph "Lapisan Abstraksi"
        ROUTER["🔀 Provider Router"]
    end

    subgraph "Penyedia LLM (Dapat Dipertukarkan)"
        OAI["OpenAI<br/>GPT-4o, o1"]
        ANT["Anthropic<br/>Claude 3.5/4"]
        OLL["Ollama<br/>Llama, Mistral"]
        GEM["Google<br/>Gemini"]
        CUS["Custom<br/>Fine-tuned Models"]
    end

    subgraph "Sistem AetherOS"
        MGR["Manager Agent"]
        ARC["Architect Agent"]
        BKD["Backend Agent"]
    end

    MGR --> ROUTER
    ARC --> ROUTER
    BKD --> ROUTER
    ROUTER --> OAI
    ROUTER --> ANT
    ROUTER --> OLL
    ROUTER --> GEM
    ROUTER --> CUS

    style ROUTER fill:#e53e3e,color:#fff
```

**Definisi:** LLM diperlakukan sebagai *mesin komputasi sementara* — sebuah resource yang dapat diganti kapan saja tanpa mempengaruhi fungsionalitas sistem.

**Implikasi Arsitektural:**
- Tidak ada kode yang memanggil API LLM secara langsung. Semua panggilan melewati Provider Router.
- Output LLM divalidasi oleh PydanticAI sebelum diterima sistem, sehingga format respons tidak bergantung pada kekhasan model tertentu.
- Automatic Fallback memastikan kegagalan satu provider tidak menghentikan operasi.

**Mengapa Ini Penting:**
- Menghilangkan vendor lock-in
- Memungkinkan optimasi biaya (model murah untuk tugas sederhana, model canggih untuk tugas kompleks)
- Melindungi dari risiko discontinuation atau perubahan kebijakan vendor

---

### Pilar 2: Persistence First

**Definisi:** Pengetahuan tidak boleh terkurung dalam konteks sesi LLM yang *ephemeral*. AetherOS menerapkan **Knowledge Extraction Layer** yang secara aktif mengekstraksi wawasan terstruktur dari setiap respons LLM sebelum dikomit ke dalam Company Brain.

**Mekanisme:**

```mermaid
sequenceDiagram
    participant Agent as 🤖 Agent
    participant LLM as 🧠 LLM
    participant KEL as 📋 Knowledge<br/>Extraction Layer
    participant PB as 🗄️ Company Brain

    Agent->>LLM: Kirim instruksi + konteks
    LLM-->>Agent: Respons (kode, analisis, keputusan)
    Agent->>KEL: Kirim respons mentah
    KEL->>KEL: Ekstraksi entitas terstruktur
    KEL->>KEL: Klasifikasi jenis pengetahuan
    KEL->>KEL: Konversi ke format JSON standar
    KEL->>PB: Simpan ke PostgreSQL (terstruktur)
    KEL->>PB: Simpan ke Qdrant (embedding vektor)
    Note over PB: Pengetahuan tersimpan<br/>permanen & model-agnostic
```

**Jenis Pengetahuan yang Diekstraksi:**

| Kategori | Contoh | Penyimpanan |
|----------|--------|-------------|
| Keputusan Arsitektur | "Menggunakan event sourcing untuk audit trail" | PostgreSQL |
| Aturan Bisnis | "Diskon hanya berlaku untuk pembelian > 100 unit" | PostgreSQL |
| Pola Kode | Implementasi pattern, boilerplate | Qdrant |
| Konteks Percakapan | Riwayat diskusi teknis | Qdrant |
| Spesifikasi Teknis | Schema API, definisi tipe | PostgreSQL |
| Reasoning Chain | Langkah-langkah berpikir agen | PostgreSQL |

---

### Pilar 3: Reactive & Event-Driven

**Definisi:** Seluruh komunikasi antar komponen menggunakan pola asinkron untuk menjamin skalabilitas dan ketahanan sistem terhadap kegagalan komponen individu.

**Arsitektur Event-Driven:**

```mermaid
graph LR
    subgraph "Producers"
        MGR["Manager Agent"]
        DASH["Dashboard"]
        CLI["CLI"]
    end

    subgraph "Event Bus (Redis Streams)"
        EB["📨 Redis Streams<br/>Consumer Groups"]
    end

    subgraph "Consumers"
        ARC["Architect Agent"]
        BKD["Backend Agent"]
        FE["Frontend Agent"]
        QA["QA Agent"]
        SEC["Security Agent"]
    end

    MGR -->|TASK_ASSIGNED| EB
    DASH -->|USER_COMMAND| EB
    CLI -->|CLI_COMMAND| EB
    EB -->|consume| ARC
    EB -->|consume| BKD
    EB -->|consume| FE
    EB -->|consume| QA
    EB -->|consume| SEC

    style EB fill:#d69e2e,color:#000
```

**Keuntungan:**
- **Decoupled:** Agen tidak perlu mengetahui lokasi atau status agen lain
- **Resilient:** Jika satu agen gagal, pesan tetap ada di stream untuk diproses ulang
- **Scalable:** Menambah instansi agen baru hanya memerlukan pendaftaran consumer baru
- **Observable:** Setiap event tercatat dan dapat di-trace

---

### Pilar 4: Traceability

**Definisi:** Setiap perubahan pada state sistem atau kode sumber harus memiliki jejak audit yang jelas, menghubungkan keputusan agen dengan Reasoning Chain yang menyebabkannya.

**Rantai Pelacakan:**

```mermaid
graph TD
    UI["👤 Instruksi Manusia<br/>via Dashboard/CLI"]
    TRACE["🔍 TraceID: aether-2026-001"]
    DEC["📋 Dekomposisi Tugas<br/>oleh Manager Agent"]
    TASK["📝 Task Assignment<br/>via Event Bus"]
    EXEC["⚡ Eksekusi Agen<br/>+ Reasoning Chain"]
    CODE["💻 Perubahan Kode<br/>di workspace/"]
    AUDIT["📊 Audit Log<br/>di PostgreSQL"]
    GIT["🔀 Git Commit<br/>dengan TraceID"]

    UI --> TRACE
    TRACE --> DEC
    DEC --> TASK
    TASK --> EXEC
    EXEC --> CODE
    EXEC --> AUDIT
    CODE --> GIT

    style TRACE fill:#805ad5,color:#fff
```

**Komponen Traceability:**

| Komponen | Fungsi | Penyimpanan |
|----------|--------|-------------|
| TraceID | Identifier unik per instruksi | OpenTelemetry |
| Reasoning Chain | Dokumentasi langkah berpikir agen | PostgreSQL |
| Audit Log | Catatan setiap aksi sistem | PostgreSQL |
| Git History | Riwayat perubahan kode | Git Repository |
| Event Stream | Log komunikasi antar agen | Redis Streams |

---

## 1.5 Value Proposition

### Untuk Berbagai Industri (Distributions)
- **Software Company:** Otomatisasi siklus hidup SDLC, code review, dan testing.
- **Cyber Security:** Orkestrasi agen pentester, analis malware, dan tim respons insiden.
- **Research Lab:** Sintesis literatur massal, ekstraksi data eksperimen, dan penulisan paper.

### Untuk Startup & Organisasi
- Memulai dengan tim AI yang terstruktur tanpa perlu merekrut banyak pekerja manual.
- Mengurangi biaya operasional melalui multi-provider routing dan cost analytics.
- Memastikan DNA dan pengetahuan organisasi terus berkembang secara otonom (Organizational Intelligence).

### Untuk Enterprise
- Audit trail lengkap untuk setiap keputusan AI — memenuhi compliance requirement
- Human-in-the-loop workflow untuk tindakan kritikal
- Skalabilitas horizontal untuk menangani proyek skala besar

### Untuk Komunitas Open-Source
- Platform yang sepenuhnya transparan dan auditable
- Plugin marketplace untuk kontribusi dan distribusi kemampuan baru
- Standar terbuka untuk interoperabilitas agen AI

---

## 1.6 Differentiator vs Solusi Existing

| Aspek | AetherOS | AutoGPT / CrewAI | LangChain Agents | Custom Solutions |
|-------|----------|-------------------|------------------|-----------------|
| Model Agnosticism | ✅ Total | ⚠️ Parsial | ⚠️ Parsial | ❌ Biasanya single-model |
| Persistent Knowledge | ✅ Company Brain | ❌ Session-based | ❌ Session-based | ⚠️ Ad-hoc |
| Event-Driven Comms | ✅ Redis Streams | ❌ Sequential | ❌ Sequential | ⚠️ Varies |
| Full Audit Trail | ✅ OpenTelemetry | ❌ Minimal | ⚠️ Basic logging | ❌ Biasanya tidak ada |
| HITL Workflow | ✅ Checkpoint Gates | ❌ Tidak ada | ⚠️ Basic | ⚠️ Custom |
| Agent RBAC | ✅ Fine-grained | ❌ Tidak ada | ❌ Tidak ada | ⚠️ Custom |
| Cost Analytics | ✅ Per-agent, per-project | ❌ Tidak ada | ⚠️ Basic | ❌ Biasanya tidak ada |

---

## 1.7 Filosofi Pengembangan

### "Pengetahuan di Atas Segalanya"

Setiap keputusan arsitektur dalam AetherOS harus menjawab pertanyaan: **"Apakah ini melindungi dan memperkaya pengetahuan organisasi?"**

Jika jawabannya tidak, keputusan tersebut perlu dipertimbangkan ulang.

### "Manusia sebagai Pengarah, AI sebagai Pelaksana"

AetherOS tidak bertujuan menggantikan manusia. Sistem ini dirancang agar manusia tetap memegang kendali strategis — menentukan tujuan, menyetujui tindakan kritikal, dan mengaudit hasil — sementara agen AI menangani eksekusi teknis.

### "Transparansi Radikal"

Setiap proses berpikir AI harus dapat ditelusuri. Tidak ada "black box" dalam AetherOS. Reasoning Chain memastikan bahwa manusia dapat memahami mengapa sebuah keputusan dibuat, bukan hanya apa keputusannya.

---

🔗 **Selanjutnya:** [Gambaran Umum Arsitektur Sistem →](../02-architecture/system-overview.md)
