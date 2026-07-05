# 10 — Git Workflow

> Dokumen ini mendeskripsikan Git workflow AetherOS, termasuk branching strategy, atomic commits, workspace volume management, dan pull request validation.

---

## 10.1 Workspace Architecture

Folder `workspace/` adalah **shared volume** yang di-mount ke semua agent containers. Volume ini dikelola sebagai Git repository.

```mermaid
graph TD
    subgraph "Agent Containers"
        BKD["⚙️ Backend Agent"]
        FE["🎨 Frontend Agent"]
        QA["🧪 QA Agent"]
        SEC["🔒 Security Agent"]
    end

    subgraph "Shared Volume"
        WS["📁 workspace/<br/>(Git Repository)"]
        MAIN["🔒 main branch<br/>(protected)"]
        FB1["🔀 feature/task-001"]
        FB2["🔀 feature/task-002"]
        FB3["🔀 feature/task-003"]
    end

    BKD -->|"write to"| FB1
    FE -->|"write to"| FB2
    QA -->|"read from"| FB1
    QA -->|"read from"| FB2
    SEC -->|"read from"| FB1

    WS --> MAIN
    WS --> FB1
    WS --> FB2
    WS --> FB3

    style MAIN fill:#e53e3e,color:#fff
    style WS fill:#f05032,color:#fff
```

---

## 10.2 Branching Strategy

### Branch Types

| Branch | Pattern | Lifetime | Created By | Merged By |
|--------|---------|----------|------------|-----------|
| `main` | `main` | Permanen | — | Manager (setelah approval) |
| `feature` | `feature/task-{id}` | Per-task | Orchestrator | Manager |
| `hotfix` | `hotfix/{description}` | Per-fix | Manager | Manager |
| `release` | `release/v{version}` | Per-release | DevOps | DevOps (HITL) |

### Branch Rules

| Rule | Deskripsi |
|------|-----------|
| **main is protected** | Tidak ada direct push ke main |
| **Feature branches from main** | Semua feature branch dibuat dari main |
| **One branch per task** | Setiap task memiliki branch sendiri |
| **Merge via PR only** | Penggabungan hanya melalui pull request |
| **Delete after merge** | Branch dihapus setelah merge |
| **No force push** | Force push tidak diizinkan di branch manapun |

---

## 10.3 Atomic Commits

### Commit Convention

Setiap commit oleh agen mengikuti format standar:

```
[{agent_role}] {type}: {description}

TraceID: {trace_id}
TaskID: {task_id}
Agent: {agent_role}#{agent_instance}
```

### Commit Types

| Type | Deskripsi |
|------|-----------|
| `feat` | Fitur baru |
| `fix` | Bug fix |
| `refactor` | Refactoring tanpa perubahan fungsional |
| `test` | Penambahan atau modifikasi test |
| `docs` | Perubahan dokumentasi |
| `schema` | Perubahan schema atau migrasi |
| `config` | Perubahan konfigurasi |
| `security` | Perbaikan keamanan |

### Contoh

```
[backend] feat: implement user registration endpoint

TraceID: aether-2026-001
TaskID: task-abc-123
Agent: backend#1
```

---

## 10.4 Pull Request Workflow

```mermaid
sequenceDiagram
    participant Agent as 🤖 Worker Agent
    participant GIT as 📂 Git
    participant QA as 🧪 QA Agent
    participant SEC as 🔒 Security Agent
    participant MGR as 👔 Manager Agent
    participant MAIN as 🔒 main branch

    Agent->>GIT: Create feature branch
    Agent->>GIT: Atomic commits (1-N)
    Agent->>GIT: Push to feature branch
    Agent->>MGR: Request merge review

    par Paralel Review
        MGR->>QA: Trigger QA review
        MGR->>SEC: Trigger Security review
    end

    QA->>QA: Run tests, check coverage
    QA-->>MGR: ✅ QA Passed (coverage: 85%)

    SEC->>SEC: Static analysis, secret scan
    SEC-->>MGR: ✅ Security Passed (no issues)

    MGR->>MGR: Review task completion
    MGR->>GIT: Merge PR to main
    GIT->>MAIN: Fast-forward merge
    GIT->>GIT: Delete feature branch
```

### PR Merge Requirements

| Requirement | Deskripsi |
|-------------|-----------|
| QA Passed | Semua tests lulus, coverage >= threshold |
| Security Passed | Tidak ada vulnerability critical/high |
| Manager Approved | Manager Agent menyetujui kualitas dan kelengkapan |
| No Conflicts | Tidak ada merge conflict dengan main |
| Atomic | Setiap PR menyelesaikan satu task lengkap |

---

## 10.5 Conflict Resolution

### File Locking

```mermaid
sequenceDiagram
    participant A1 as 🤖 Agent A
    participant LOCK as 🔒 Lock Manager<br/>(Redis)
    participant A2 as 🤖 Agent B

    A1->>LOCK: Lock: api/users.py
    LOCK-->>A1: ✅ Lock acquired

    A2->>LOCK: Lock: api/users.py
    LOCK-->>A2: ❌ Lock denied (held by Agent A)
    A2->>A2: Wait + backoff

    A1->>A1: Write to file
    A1->>LOCK: Release: api/users.py
    LOCK-->>A1: ✅ Released

    A2->>LOCK: Lock: api/users.py
    LOCK-->>A2: ✅ Lock acquired
```

### Merge Conflict Resolution

| Strategi | Kapan Digunakan |
|----------|-----------------|
| **Auto-resolve** | Non-overlapping changes (different sections of file) |
| **Agent retry** | Same section, send both versions to agent for merge |
| **Manager decision** | Complex conflicts, escalate to Manager |
| **HITL** | Critical files (config, schema), escalate to human |

---

## 10.6 Git Hooks

| Hook | Timing | Action |
|------|--------|--------|
| `pre-commit` | Sebelum commit | Validasi format, check secrets, lint |
| `commit-msg` | Saat commit | Validasi format commit message |
| `pre-push` | Sebelum push | Run quick tests, check branch rules |
| `post-merge` | Setelah merge | Notify Dashboard, update Project Brain |

---

🔗 **Selanjutnya:** [Roadmap Pengembangan →](../11-roadmap/development-phases.md)

🔗 **Kembali:** [Marketplace API ←](../09-interfaces/marketplace-api.md)
