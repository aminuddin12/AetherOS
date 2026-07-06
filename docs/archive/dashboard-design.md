---
Status: Deprecated
Reason: Legacy architecture based on multi-agent chatbot framework (Redis, PostgreSQL, Qdrant, FastAPI, LangGraph, PydanticAI) has been replaced by the modular Operating System model (Kernel, Execution Engine, Runtime SDK, Workspace, Storage, Repository, Artifact, Organization).
Superseded By: ADR-0011 through ADR-0027, docs/id/architecture/book.md
Replacement: docs/id/architecture/book.md
---

# 09.3 — Desain Dashboard

> Dokumen ini mendeskripsikan desain Web Dashboard AetherOS untuk monitoring, manajemen, dan Human Approval Interface.

---

## 9.3.1 Dashboard Overview

Dashboard AetherOS berfungsi sebagai **pusat komando visual** bagi manusia untuk memantau, mengontrol, dan berinteraksi dengan organisasi AI.

### Halaman Utama

| Halaman | Fungsi |
|---------|--------|
| **Overview** | Ringkasan real-time: agen aktif, tasks, cost, health |
| **Projects** | Manajemen proyek: buat, lihat, arsipkan |
| **Tasks** | Monitoring tugas: status, progress, logs |
| **Agents** | Status agen: health, workload, performance |
| **Approvals** | HITL interface: review, approve, deny |
| **Knowledge** | Browser Project Brain: search, explore |
| **Analytics** | Dashboard biaya, token, performance |
| **Audit** | Audit trail: search, filter, trace |
| **Settings** | Konfigurasi: providers, budgets, HITL levels |

---

## 9.3.2 Komponen Dashboard

### Overview Page

```mermaid
graph TD
    subgraph "Overview Dashboard"
        subgraph "Status Bar"
            SB1["🟢 System: Healthy"]
            SB2["🤖 Agents: 8/8 Active"]
            SB3["📝 Tasks: 12 Running"]
            SB4["💰 Cost Today: $23.45"]
        end

        subgraph "Active Tasks"
            AT["📋 Real-time task list<br/>with progress bars"]
        end

        subgraph "Agent Status Grid"
            AG["🤖 Grid of agent cards<br/>with health indicators"]
        end

        subgraph "Pending Approvals"
            PA["⚠️ HITL requests<br/>requiring human action"]
        end

        subgraph "Cost Chart"
            CC["📈 Token usage<br/>over time"]
        end
    end
```

### Approval Interface (HITL)

| Komponen | Deskripsi |
|----------|-----------|
| **Request Card** | Ringkasan: agen peminta, tipe aksi, severity |
| **Detail Panel** | Penjelasan lengkap: apa yang akan dilakukan, resource yang terpengaruh |
| **Risk Assessment** | Penilaian risiko otomatis: low/medium/high/critical |
| **Rollback Plan** | Rencana pembatalan jika terjadi masalah |
| **Diff View** | Preview perubahan (kode, config, schema) |
| **Action Buttons** | Approve / Deny (dengan field alasan) |
| **History** | Riwayat keputusan sebelumnya untuk referensi |

### Real-time Features

| Feature | Teknologi | Deskripsi |
|---------|-----------|-----------|
| Task progress | WebSocket | Real-time update progress bar |
| Agent status | WebSocket | Live health indicators |
| Log streaming | WebSocket | Live log output dari task yang berjalan |
| Notifications | WebSocket + Push | Alert untuk approval requests dan errors |
| Cost ticker | WebSocket | Real-time cost accumulation |

---

## 9.3.3 Trace Explorer

Fitur untuk menelusuri jejak instruksi dari awal hingga akhir:

```mermaid
graph LR
    INPUT["👤 Instruksi:<br/>'Bangun REST API users'"]
    INPUT --> TRACE["🔍 TraceID:<br/>aether-2026-001"]
    TRACE --> TIMELINE["📊 Timeline View"]

    TIMELINE --> E1["00:00 - API Gateway received"]
    TIMELINE --> E2["00:01 - Manager decomposed (4 tasks)"]
    TIMELINE --> E3["00:03 - Architect: schema.py created"]
    TIMELINE --> E4["00:15 - Backend: users.py implemented"]
    TIMELINE --> E5["00:25 - QA: 12/12 tests passed"]
    TIMELINE --> E6["00:28 - Security: no issues found"]
    TIMELINE --> E7["00:30 - Completed"]
```

---

🔗 **Selanjutnya:** [Marketplace API →](marketplace-api.md)

🔗 **Kembali:** [Referensi CLI ←](cli-reference.md)
