# 05 — Provider Router dan Manajemen Model

> Dokumen ini mendeskripsikan Multi-provider API Router, automatic fallback, cost & token analytics, dan strategi pemilihan model.

---

## 5.1 Arsitektur Provider Router

Provider Router adalah lapisan abstraksi yang memungkinkan AetherOS menggunakan berbagai penyedia LLM tanpa mengubah kode agen.

```mermaid
graph TD
    subgraph "Agent Layer"
        A1["🤖 Agent Request<br/>model_preference: 'best'"]
    end

    subgraph "Provider Router"
        ROUTER["🔀 Smart Router"]
        SELECTOR["📊 Model Selector<br/>(preference + availability + cost)"]
        VALIDATOR["✅ PydanticAI<br/>Response Validator"]
        FALLBACK["🔄 Fallback Logic"]
        ANALYTICS["📈 Cost & Token<br/>Analytics"]
    end

    subgraph "LLM Providers"
        P1["OpenAI<br/>GPT-4o, GPT-4o-mini, o1"]
        P2["Anthropic<br/>Claude 4, Claude 3.5 Sonnet"]
        P3["Ollama (Local)<br/>Llama 3, Mistral, CodeLlama"]
        P4["Google AI<br/>Gemini 2.5 Pro, Flash"]
        P5["Custom<br/>Fine-tuned models"]
    end

    A1 --> ROUTER
    ROUTER --> SELECTOR
    SELECTOR --> P1
    SELECTOR --> P2
    SELECTOR --> P3
    SELECTOR --> P4
    SELECTOR --> P5
    P1 --> VALIDATOR
    P2 --> VALIDATOR
    P3 --> VALIDATOR
    P4 --> VALIDATOR
    P5 --> VALIDATOR
    VALIDATOR -->|Sukses| A1
    VALIDATOR -->|Gagal| FALLBACK
    FALLBACK --> SELECTOR
    ROUTER --> ANALYTICS

    style ROUTER fill:#e53e3e,color:#fff
    style SELECTOR fill:#4299e1,color:#fff
    style FALLBACK fill:#ed8936,color:#fff
```

---

## 5.2 Model Selection Strategy

### Preference Modes

| Mode | Kriteria Utama | Use Case |
|------|---------------|----------|
| **best** | Kualitas reasoning tertinggi | Manager decisions, complex architecture, security review |
| **fast** | Latensi terendah | Boilerplate generation, formatting, documentation |
| **cheap** | Biaya per token terendah | Batch processing, simple transformations |
| **local** | Prioritas model lokal (Ollama) | Offline mode, data sensitivity |
| **specific** | Model tertentu yang diminta | Ketika task memerlukan model spesifik |

### Model Tier Mapping

| Tier | OpenAI | Anthropic | Google | Ollama |
|------|--------|-----------|--------|--------|
| **Tier 1 (Best)** | o1, GPT-4o | Claude 4 Opus | Gemini 2.5 Pro | — |
| **Tier 2 (Good)** | GPT-4o-mini | Claude 3.5 Sonnet | Gemini 2.5 Flash | Llama 3 70B |
| **Tier 3 (Fast)** | GPT-4o-mini | Claude 3.5 Haiku | Gemini Flash | Llama 3 8B |
| **Tier 4 (Cheap)** | GPT-4o-mini | Claude 3.5 Haiku | Gemini Flash | Mistral 7B |

### Selection Algorithm

```mermaid
flowchart TD
    REQ["📥 Agent Request<br/>preference + task type"]

    REQ --> CHECK_PREF{"Mode?"}

    CHECK_PREF -->|best| TIER1["Pilih dari Tier 1"]
    CHECK_PREF -->|fast| TIER3["Pilih dari Tier 3"]
    CHECK_PREF -->|cheap| TIER4["Pilih dari Tier 4"]
    CHECK_PREF -->|local| OLLAMA["Pilih dari Ollama"]
    CHECK_PREF -->|specific| DIRECT["Gunakan model yang diminta"]

    TIER1 --> AVAIL{"Provider<br/>available?"}
    TIER3 --> AVAIL
    TIER4 --> AVAIL
    OLLAMA --> AVAIL
    DIRECT --> AVAIL

    AVAIL -->|Ya| SEND["📤 Kirim request"]
    AVAIL -->|Tidak| DOWN_TIER["⬇️ Coba tier di bawahnya"]
    DOWN_TIER --> AVAIL

    SEND --> RESULT{"Sukses?"}
    RESULT -->|Ya| DONE["✅ Return response"]
    RESULT -->|429/500/timeout| FALLBACK["🔄 Fallback"]
    FALLBACK --> AVAIL

    style DONE fill:#48bb78,color:#fff
    style FALLBACK fill:#ed8936,color:#fff
```

---

## 5.3 Automatic Fallback

### Trigger Fallback

| Trigger | Deskripsi | Fallback Action |
|---------|-----------|-----------------|
| HTTP 429 | Rate limit exceeded | Pindah ke provider lain di tier yang sama |
| HTTP 500/502/503 | Server error | Pindah ke provider lain + retry |
| Timeout (>30s) | Request timeout | Pindah ke provider lain |
| Validation failure | Output tidak sesuai schema | Retry dengan provider yang sama (max 3x), lalu pindah |
| Provider maintenance | Scheduled downtime | Otomatis gunakan provider alternatif |
| Budget exceeded | Cost limit per proyek tercapai | Downgrade ke tier lebih murah |

### Fallback Chain

```mermaid
graph LR
    PRIMARY["1️⃣ Primary Provider<br/>(sesuai preference)"]
    SECONDARY["2️⃣ Secondary Provider<br/>(tier yang sama)"]
    TERTIARY["3️⃣ Tertiary Provider<br/>(tier di bawahnya)"]
    LOCAL["4️⃣ Local Fallback<br/>(Ollama)"]
    FAIL["❌ Task Failed<br/>(escalate ke Manager)"]

    PRIMARY -->|gagal| SECONDARY
    SECONDARY -->|gagal| TERTIARY
    TERTIARY -->|gagal| LOCAL
    LOCAL -->|gagal| FAIL

    style PRIMARY fill:#48bb78,color:#fff
    style SECONDARY fill:#4299e1,color:#fff
    style TERTIARY fill:#ed8936,color:#fff
    style LOCAL fill:#9f7aea,color:#fff
    style FAIL fill:#e53e3e,color:#fff
```

### Context Preservation selama Fallback

| Aspek | Strategi |
|-------|----------|
| System prompt | Dipertahankan identik |
| Conversation history | Dipertahankan lengkap |
| Tool definitions | Disesuaikan dengan format provider baru |
| Output schema | Tetap sama (PydanticAI mengabstraksi) |
| Reasoning chain | Dipertahankan, tambahkan note tentang fallback |

---

## 5.4 Cost & Token Analytics

### Tracking Granularity

```mermaid
graph TD
    TOTAL["💰 Total Cost"]

    TOTAL --> PROJ["📁 Per Project"]
    TOTAL --> PROV["🏢 Per Provider"]
    TOTAL --> TIME["📅 Per Time Period"]

    PROJ --> PROJ_AGENT["🤖 Per Agent"]
    PROJ --> PROJ_TASK["📝 Per Task"]

    PROJ_AGENT --> DETAIL["📊 Detail:<br/>• Input tokens<br/>• Output tokens<br/>• Total cost<br/>• Average latency<br/>• Failure rate"]

    style TOTAL fill:#e53e3e,color:#fff
    style DETAIL fill:#48bb78,color:#fff
```

### Metrik yang Dilacak

| Metrik | Granularity | Deskripsi |
|--------|-------------|-----------|
| `input_tokens` | Per request | Jumlah token input |
| `output_tokens` | Per request | Jumlah token output |
| `total_cost_usd` | Per request | Biaya dalam USD |
| `latency_ms` | Per request | Latensi respons |
| `success_rate` | Per provider/day | Persentase request sukses |
| `fallback_count` | Per provider/day | Jumlah fallback yang terjadi |
| `cache_hit_rate` | Per provider/day | Persentase cache hits |

### Budget Management

| Parameter | Deskripsi | Default |
|-----------|-----------|---------|
| `project_daily_budget` | Batas biaya harian per proyek | $50 |
| `project_monthly_budget` | Batas biaya bulanan per proyek | $1,000 |
| `agent_hourly_budget` | Batas biaya per jam per agen | $5 |
| `alert_threshold` | Persentase budget untuk alert | 80% |
| `auto_downgrade_threshold` | Persentase budget untuk auto-downgrade tier | 90% |
| `hard_stop_threshold` | Persentase budget untuk menghentikan request | 100% |

### Budget Enforcement Flow

```mermaid
flowchart TD
    REQ["📤 LLM Request"]
    CHECK["💰 Budget Check"]

    REQ --> CHECK
    CHECK -->|"< 80% budget"| NORMAL["✅ Normal: Proses sesuai preference"]
    CHECK -->|"80-90% budget"| ALERT["⚠️ Alert: Kirim warning ke Dashboard"]
    CHECK -->|"90-100% budget"| DOWNGRADE["⬇️ Downgrade: Paksa ke tier murah"]
    CHECK -->|"> 100% budget"| STOP["🛑 Stop: Reject request, notify Manager"]

    ALERT --> NORMAL
    DOWNGRADE --> PROCESS["📤 Proses dengan tier murah"]

    style NORMAL fill:#48bb78,color:#fff
    style ALERT fill:#ecc94b,color:#000
    style DOWNGRADE fill:#ed8936,color:#fff
    style STOP fill:#e53e3e,color:#fff
```

---

## 5.5 Response Caching

### Cache Strategy

| Strategi | Deskripsi |
|----------|-----------|
| **Exact match cache** | Request identik (hash dari prompt + model) menggunakan cached response |
| **Semantic cache** | Request serupa (cosine similarity > 0.95) menggunakan cached response |
| **TTL-based invalidation** | Cache entry dihapus setelah TTL (default: 1 jam) |
| **Project-scoped** | Cache dipartisi per proyek untuk menghindari context leakage |

### Cache Configuration

| Parameter | Nilai Default | Deskripsi |
|-----------|--------------|-----------|
| `cache_enabled` | true | Enable/disable caching |
| `cache_ttl` | 3600s | Time-to-live untuk cache entry |
| `semantic_cache_threshold` | 0.95 | Minimum similarity untuk semantic cache hit |
| `cache_max_size` | 1000 entries | Maksimal entry dalam cache |
| `cache_backend` | Redis | Storage backend |

---

## 5.6 Provider Configuration

### Per-Provider Settings

| Setting | Deskripsi |
|---------|-----------|
| `api_key` | API key (encrypted at rest) |
| `base_url` | Base URL untuk API |
| `max_concurrent` | Maksimal request bersamaan |
| `rate_limit_rpm` | Rate limit requests per menit |
| `rate_limit_tpm` | Rate limit tokens per menit |
| `timeout` | Request timeout |
| `retry_count` | Jumlah retry sebelum fallback |
| `enabled` | Enable/disable provider |
| `priority` | Prioritas default (1 = tertinggi) |

---

🔗 **Selanjutnya:** [Skill Library →](../06-skills-and-tools/skill-library.md)

🔗 **Kembali:** [RBAC & Permissions ←](../04-agents/rbac-and-permissions.md)
