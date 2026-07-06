---
Status: Deprecated
Reason: Legacy architecture based on multi-agent chatbot framework (Redis, PostgreSQL, Qdrant, FastAPI, LangGraph, PydanticAI) has been replaced by the modular Operating System model (Kernel, Execution Engine, Runtime SDK, Workspace, Storage, Repository, Artifact, Organization).
Superseded By: ADR-0011 through ADR-0027, docs/id/architecture/book.md
Replacement: docs/id/architecture/book.md
---

# Arsitektur Multi-Workspace

Sebuah "OS untuk Organisasi AI" tidak akan lengkap tanpa kemampuan untuk mengelola berbagai proyek dan divisi secara serentak. AetherOS menerapkan **Arsitektur Multi-Workspace** untuk mengisolasi lingkungan eksekusi agen sekaligus mempertahankan kemampuan berbagi pengetahuan.

## 1. Hierarki Organisasi

Struktur data AetherOS dirancang untuk merepresentasikan entitas bisnis berskala besar, yang dapat menampung anak usaha, divisi yang berbeda, hingga ratusan proyek berjalan.

```text
Organization (AetherOS Instance)
│
├── Division (Misal: Software Development)
│   │
│   ├── Project (Misal: ERP System)
│   │   └── Workspace (Misal: ERP Production Workspace)
│   │   └── Workspace (Misal: ERP Staging Workspace)
│   │
│   └── Project (Misal: Mobile App)
│       └── Workspace (Misal: iOS Workspace)
│
└── Division (Misal: Cyber Security)
    │
    └── Project (Misal: Pentest Q3)
        └── Workspace (Misal: Red Team Workspace)
```

## 2. Isolasi dan Sharing Knowledge

Konsep Multi-Workspace membawa tantangan unik: **Bagaimana kita menjaga privasi antar proyek (isolasi) sambil tetap memungkinkan organisasi belajar dari semua proyek (sharing)?**

AetherOS menggunakan konsep **Knowledge Scoping** di dalam *Company Brain*.

### 2.1 Workspace Scoping (Terisolasi Ketat)
- Setiap Workspace memiliki direktori file lokal atau repositori Git-nya sendiri.
- Agen di `Workspace Pentest` tidak dapat melihat, membaca, atau mengeksekusi kode yang ada di `Workspace ERP`.
- Rahasia (Secrets), kredensial, dan env vars dienkripsi per-workspace.

### 2.2 Project Scoping (Berbagi Antar Workspace)
- Aturan (Constitution) yang didefinisikan di tingkat Proyek (misalnya standar *coding style*) akan diturunkan ke `Workspace Staging` maupun `Production`.
- Agen dapat merujuk riwayat PR atau dokumentasi internal proyek secara utuh.

### 2.3 Company Scoping (Pengetahuan Global)
Ini adalah lapisan kecerdasan lintas divisi.
- Jika Agen di divisi Software Development menemukan cara optimal untuk mengonfigurasi Docker, wawasan tersebut diekstraksi ke **Global Knowledge**.
- Ketika Agen di divisi Cyber Security perlu melakukan *review* file Docker, ia akan menggunakan wawasan terbaik (*Best Practice*) dari Global Knowledge.
- **Privacy Filter:** Kernel AetherOS (melalui Memory Engine) akan "membersihkan" (sanitize) data dari informasi sensitif atau spesifik proyek sebelum memasukkannya ke Global Knowledge (mengubah data spesifik menjadi *Pattern* atau *Lesson Learned* abstrak).

## 3. Eksekusi Multi-Tenant

Secara teknis di lapisan Kubernetes / Docker Swarm:
1. Setiap **Workspace** diterjemahkan sebagai satu *sandbox environment* (misalnya pod atau container tersendiri yang dijalankan melalui OpenHands).
2. Agen dapat berpindah konteks (*Context Switching*). Agen yang sama (dengan peran *Senior Backend*) dapat di-assign ke Proyek ERP di pagi hari, dan ditugaskan ke Proyek Mobile App di siang hari, secara dinamis memuat memori yang relevan tanpa tercampur.

---

🔗 **Selanjutnya:** [Siklus Hidup Agen →](../04-agents/agent-lifecycle.md)
