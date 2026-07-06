# 07.1 — Model Keamanan

> Dokumen ini mendeskripsikan model keamanan AetherOS, termasuk threat model, attack surface, mitigasi, dan security review pipeline.

---

## 7.1.1 Prinsip Keamanan

| Prinsip | Implementasi |
|---------|-------------|
| **Security by Default** | Keamanan bukan fitur opsional — terintegrasi di setiap layer |
| **Zero Trust** | Tidak ada agen yang secara implisit dipercaya |
| **Least Privilege** | Setiap agen hanya memiliki akses minimal yang diperlukan |
| **Defense in Depth** | Multiple layers keamanan: RBAC → Sandbox → Review → Audit |
| **Automated Review** | Setiap kode yang dihasilkan AI wajib melewati security review otomatis |

---

## 7.1.2 Threat Model

### Attack Surface

```mermaid
graph TD
    subgraph "External Threats"
        T1["🌐 API Injection<br/>Manipulasi instruksi melalui API"]
        T2["🔓 Credential Exposure<br/>API keys dalam kode yang dihasilkan"]
        T3["📦 Supply Chain<br/>Dependency vulnerabilities"]
    end

    subgraph "Internal Threats (AI-specific)"
        T4["🤖 Prompt Injection<br/>Agen dimanipulasi melalui data"]
        T5["🧠 Hallucination Exploit<br/>LLM menghasilkan kode berbahaya"]
        T6["⬆️ Privilege Escalation<br/>Agen mencoba mengakses di luar RBAC"]
        T7["💾 Data Exfiltration<br/>Agen mengirim data ke luar"]
        T8["🔄 Agent Collusion<br/>Agen berkolaborasi melewati kontrol"]
    end

    subgraph "Infrastructure Threats"
        T9["🗄️ Database Breach<br/>Akses tidak sah ke Project Brain"]
        T10["📨 Event Bus Poisoning<br/>Injeksi event berbahaya"]
        T11["🐳 Container Escape<br/>Keluar dari sandbox"]
    end

    style T4 fill:#e53e3e,color:#fff
    style T5 fill:#e53e3e,color:#fff
    style T6 fill:#ed8936,color:#fff
```

### Risk Assessment Matrix

| Threat | Likelihood | Impact | Risk Level | Mitigasi Utama |
|--------|-----------|--------|------------|----------------|
| Prompt Injection | Tinggi | Tinggi | 🔴 Critical | Input sanitization, PydanticAI validation |
| Credential Exposure | Tinggi | Tinggi | 🔴 Critical | Automated secret scanning |
| Hallucination Exploit | Sedang | Tinggi | 🟠 High | Schema enforcement, cross-agent validation |
| Privilege Escalation | Sedang | Tinggi | 🟠 High | RBAC enforcement at runtime |
| Supply Chain Attack | Sedang | Sedang | 🟡 Medium | Dependency scanning, lockfile enforcement |
| Data Exfiltration | Rendah | Tinggi | 🟡 Medium | Network isolation, egress monitoring |
| Container Escape | Rendah | Tinggi | 🟡 Medium | Hardened containers, seccomp profiles |
| Event Bus Poisoning | Rendah | Sedang | 🟢 Low | Message authentication, schema validation |

---

## 7.1.3 Security Layers

```mermaid
graph TD
    subgraph "Layer 1: Input Validation"
        L1["✅ API input sanitization<br/>✅ Instruction validation<br/>✅ Authentication & Authorization"]
    end

    subgraph "Layer 2: Agent Isolation"
        L2["🔐 RBAC enforcement<br/>🏗️ Sandboxed execution (OpenHands)<br/>🌐 Network isolation"]
    end

    subgraph "Layer 3: Output Validation"
        L3["📋 PydanticAI schema enforcement<br/>🧪 Anti-hallucination checks<br/>🔍 Code quality gates"]
    end

    subgraph "Layer 4: Automated Review"
        L4["🔒 Security Agent scanning<br/>🔑 Secret detection<br/>📦 Dependency vulnerability check"]
    end

    subgraph "Layer 5: Human Oversight"
        L5["👤 HITL Checkpoint Gates<br/>👔 Manager merge approval<br/>📊 Audit log review"]
    end

    L1 --> L2 --> L3 --> L4 --> L5

    style L1 fill:#4299e1,color:#fff
    style L2 fill:#48bb78,color:#fff
    style L3 fill:#ed8936,color:#fff
    style L4 fill:#e53e3e,color:#fff
    style L5 fill:#805ad5,color:#fff
```

---

## 7.1.4 Automated Security Review Pipeline

### Pipeline Flow

```mermaid
flowchart TD
    CODE["💻 Kode yang Dihasilkan Agen"]

    CODE --> STATIC["🔍 Static Analysis<br/>(bandit, semgrep)"]
    CODE --> SECRET["🔑 Secret Scanning<br/>(detect-secrets, gitleaks)"]
    CODE --> DEP["📦 Dependency Check<br/>(safety, trivy)"]
    CODE --> PATTERN["🧩 Pattern Matching<br/>(custom rules)"]

    STATIC --> MERGE["📊 Merge Results"]
    SECRET --> MERGE
    DEP --> MERGE
    PATTERN --> MERGE

    MERGE --> ASSESS{"Severity?"}

    ASSESS -->|"Critical/High"| BLOCK["🛑 Block Merge<br/>Notify Manager + Dev"]
    ASSESS -->|"Medium"| FLAG["⚠️ Flag for Review<br/>Allow merge with warning"]
    ASSESS -->|"Low/None"| PASS["✅ Pass<br/>Allow merge"]

    BLOCK --> FIX["🔧 Agen memperbaiki<br/>(auto-fix jika memungkinkan)"]
    FIX --> CODE

    style CODE fill:#4299e1,color:#fff
    style BLOCK fill:#e53e3e,color:#fff
    style PASS fill:#48bb78,color:#fff
```

### Jenis Pemindaian

| Pemindaian | Tool | Target |
|------------|------|--------|
| **SQL Injection** | semgrep, bandit | Raw SQL queries, ORM misuse |
| **XSS** | semgrep | User input rendered tanpa sanitization |
| **SSRF** | semgrep | URL dari user input tanpa validasi |
| **Hardcoded Secrets** | detect-secrets, gitleaks | API keys, passwords, tokens |
| **Insecure Deserialization** | bandit | pickle.loads, yaml.load |
| **Path Traversal** | semgrep | File ops dengan user-controlled path |
| **Dependency CVEs** | safety, trivy | Known vulnerabilities di dependencies |
| **Insecure Defaults** | Custom rules | DEBUG=True, weak crypto, etc. |

---

## 7.1.5 Secret Management

| Aspek | Implementasi |
|-------|-------------|
| **Storage** | Environment variables atau secret manager (Vault) |
| **Rotation** | Otomatis rotate API keys setiap 90 hari |
| **Access** | Agen mengakses secrets melalui runtime injection, bukan hardcode |
| **Detection** | Pre-commit hook + CI pipeline scanning |
| **Response** | Jika secret terdeteksi dalam kode: auto-revoke, alert, block merge |

---

🔗 **Selanjutnya:** [Audit & Kepatuhan →](audit-and-compliance.md)

🔗 **Kembali:** [Integrasi OpenHands ←](../06-skills-and-tools/openhands-integration.md)
