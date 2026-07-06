# AetherOS Roadmap

AetherOS telah berevolusi dari sekadar "AI Agent Framework" menjadi **Open Agent Operating System**. Roadmap berikut merangkum evolusi arsitektur dan fungsionalitas menuju ekosistem organisasi digital yang sepenuhnya berdaulat.

---

## Operating System Layer (Completed)

Layer fondasi ini membangun infrastruktur *low-level* AetherOS yang independen dari konsep AI, bertindak murni sebagai Sistem Operasi.

- ✅ **Milestone 0: Core Contracts** (Data structures, Pydantic schemas, BaseContract)
- ✅ **Milestone 1: Kernel** (Dependency Injection, Dispatcher, Metrics, Pipeline, State, Registry)
- ✅ **Milestone 2: Execution Engine** (Thread, Worker, Queue, Strategy, Timeout, Retry, Pool)
- ✅ **Milestone 2.5: Engineering Hardening** (Testing, Architecture Validation, Compatibility, CI/CD, OSS Governance)
- ✅ **Milestone 2.6: Developer Runtime (CLI)** (Aether CLI, Dynamic Formatter, Architecture Introspection)

---

## The Bridge (Next)

Menjembatani fondasi *low-level* (Kernel) dengan *frontends* dan *Organization Layer*.

- ⏳ **Milestone 2.7: Internal Runtime API** 
  - Standarisasi antarmuka untuk seluruh interaksi dengan Kernel.
  - CLI, GUI (Aether Studio), dan REST API akan mengonsumsi layer Runtime API yang sama.

---

## Organization Layer (Future)

Lapisan di mana AI, manusia, dan instrumen digital dirakit menjadi satu entitas operasional.

- ⏳ **Milestone 3: Workspace Core Runtime**
  - Implementasi *Workspace Lifecycle*, *Repository*, *Branch*, *Commit*, *Artifact*, dan *Filesystem*.
  - Pemisahan model domain dari servis (tanpa AI).
  
- ⏳ **Milestone 3.5: Workspace Services Runtime**
  - Integrasi layanan *Workspace*: *Git*, *Watcher*, *Indexer*, *Search*, *Snapshot*, *Workspace Events*, *Cache*.

- ⏳ **Milestone 4: Knowledge Runtime** (Mantan "Memory Engine")
  - Membangun memori organisasi: *Knowledge, Policy, Lesson, Company DNA, Standards, Patterns, Predictions, Recommendations, Embeddings*.
  
- ⏳ **Milestone 5: Provider Runtime**
  - Abstraksi layanan kapabilitas: *LLM, Embedding, Vision, Speech, Image, Video, OCR, Search, Browser, Filesystem*.
  - Provider bukan entitas AI, melainkan driver kapabilitas.

- ⏳ **Milestone 6: Tool Runtime**
  - Mesin untuk manajemen, eksekusi, dan keamanan *Tools*.

- ⏳ **Milestone 7: Extension Runtime** (Mantan "Plugin SDK")
  - Runtime modular untuk memperluas fungsi AetherOS melalui: *Command, Provider, Tool, Dashboard, Distribution, Workflow, CLI, Studio, SDK*.

- ⏳ **Milestone 8: Organization Runtime**
  - Struktur operasional: *CEO, CTO, Engineering, QA, Security, DevOps, Finance, HR, Marketing, Research*.
  - Mengelola *Worker* (AI) sebagai bagian integral dari departemen.

- ⏳ **Milestone 9: Distribution Runtime**
  - Kemampuan instalasi organisasi prasetel (Packaged Distributions).
  - Contoh: `aether install software-company`, `aether install cybersecurity`, `aether install marketing`.
