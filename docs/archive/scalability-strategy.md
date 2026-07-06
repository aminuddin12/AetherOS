---
Status: Deprecated
Reason: Legacy architecture based on multi-agent chatbot framework (Redis, PostgreSQL, Qdrant, FastAPI, LangGraph, PydanticAI) has been replaced by the modular Operating System model (Kernel, Execution Engine, Runtime SDK, Workspace, Storage, Repository, Artifact, Organization).
Superseded By: ADR-0011 through ADR-0027, docs/id/architecture/book.md
Replacement: docs/id/architecture/book.md
---

# 08.3 — Strategi Skalabilitas

> Dokumen ini mendeskripsikan strategi skalabilitas AetherOS, termasuk horizontal scaling, metadata pre-filtering, dan performance optimization.

---

## 8.3.1 Scaling Dimensions

```mermaid
graph TD
    subgraph "Horizontal Scaling"
        AGENTS["🤖 Agent Instances<br/>Scale out agen per role"]
        API["🔌 API Gateway<br/>Load balancer + replicas"]
    end

    subgraph "Vertical Scaling"
        DB["🗄️ Database<br/>Larger instance, read replicas"]
        CACHE["⚡ Cache<br/>Larger Redis cluster"]
    end

    subgraph "Data Scaling"
        PART["📊 Partitioning<br/>Time-based table partitions"]
        FILTER["🔍 Pre-filtering<br/>Metadata-based vector search"]
        ARCHIVE["❄️ Archiving<br/>Cold storage for old data"]
    end

    style AGENTS fill:#4299e1,color:#fff
    style DB fill:#336791,color:#fff
    style FILTER fill:#805ad5,color:#fff
```

---

## 8.3.2 Agent Scaling

### Auto-scaling Rules

| Role | Min Instances | Max Instances | Scale Trigger |
|------|---------------|---------------|---------------|
| Manager | 1 | 1 | Tidak di-scale (singleton) |
| Architect | 1 | 2 | Queue depth > 3 tasks |
| Backend | 1 | 5 | Queue depth > 5 tasks |
| Frontend | 1 | 3 | Queue depth > 3 tasks |
| QA | 1 | 3 | Queue depth > 5 tasks |
| Security | 1 | 2 | Queue depth > 3 tasks |
| DevOps | 1 | 2 | Queue depth > 2 tasks |
| Documentation | 1 | 2 | Queue depth > 5 tasks |

### Scaling Flow

```mermaid
sequenceDiagram
    participant MON as 📊 Monitor
    participant EB as 📨 Event Bus
    participant SCALER as 📈 Auto-scaler
    participant DOCKER as 🐳 Docker

    loop Every 30 seconds
        MON->>EB: Check queue depths per consumer group
        EB-->>MON: Queue stats

        alt Queue depth > threshold
            MON->>SCALER: Scale up request
            SCALER->>DOCKER: Start new agent container
            DOCKER-->>SCALER: Container started
            SCALER->>EB: Register new consumer
        else Queue depth < min_threshold AND instances > min
            MON->>SCALER: Scale down request
            SCALER->>EB: Drain consumer
            SCALER->>DOCKER: Stop container (graceful)
        end
    end
```

---

## 8.3.3 Database Scaling

### PostgreSQL

| Strategi | Implementasi | Kapan |
|----------|-------------|-------|
| **Read Replicas** | Streaming replication | Query volume > 1000/s |
| **Table Partitioning** | Monthly partitions untuk audit_logs, tasks | Data > 10M rows |
| **Connection Pooling** | PgBouncer | Concurrent connections > 100 |
| **Index Optimization** | Partial indexes, covering indexes | Query P95 > 100ms |

### Qdrant

| Strategi | Implementasi | Kapan |
|----------|-------------|-------|
| **On-disk Vectors** | Memindahkan HNSW graph ke disk | RAM usage > 80% |
| **Metadata Pre-filtering** | Filter sebelum similarity search | Collection > 1M vectors |
| **Sharding** | Distribusi collection ke multiple nodes | Collection > 10M vectors |
| **Collection Segmentation** | Split ke multiple collections | Cross-project query performance |

---

## 8.3.4 Performance Targets

| Metrik | Target | Acceptable | Degraded |
|--------|--------|------------|----------|
| API response time (P95) | < 200ms | < 500ms | > 1s |
| Task throughput | > 10 tasks/min | > 5 tasks/min | < 2 tasks/min |
| LLM request latency (P95) | < 15s | < 30s | > 45s |
| Event Bus throughput | > 100 msg/s | > 50 msg/s | < 20 msg/s |
| Brain query latency (P95) | < 500ms | < 1s | > 2s |
| Vector search latency (P95) | < 100ms | < 200ms | > 500ms |

---

🔗 **Selanjutnya:** [Spesifikasi API →](../09-interfaces/api-specification.md)

🔗 **Kembali:** [CI/CD Pipeline ←](ci-cd-pipeline.md)
