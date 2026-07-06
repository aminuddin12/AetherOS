---
Status: Deprecated
Reason: Legacy architecture based on multi-agent chatbot framework (Redis, PostgreSQL, Qdrant, FastAPI, LangGraph, PydanticAI) has been replaced by the modular Operating System model (Kernel, Execution Engine, Runtime SDK, Workspace, Storage, Repository, Artifact, Organization).
Superseded By: ADR-0011 through ADR-0027, docs/id/architecture/book.md
Replacement: docs/id/architecture/book.md
---

# ADR-0006: Penggunaan OpenTelemetry untuk Traceability

## Konteks
Ketika Agen A memanggil Agen B, dan Agen B mengubah file C, kita memerlukan cara untuk menelusuri keseluruhan rentetan aksi tersebut kembali ke *prompt* awal dari pengguna. Praktik tradisional dengan `logging` Python standar tidak cukup untuk sistem terdistribusi.

## Keputusan
Kita menggunakan standar **OpenTelemetry (OTel)** untuk pelacakan (Traceability) dan observabilitas (*Observability*).

## Konsekuensi Positif
- *Vendor-neutral*. Kita bisa mengirimkan log dan metrik ke Jaeger, Prometheus, Datadog, atau sistem pemantauan apa pun tanpa mengubah kode kernel.
- Konsep *TraceID* dan *SpanID* memecahkan masalah pelacakan antar-agen (lintas *Event Bus*).

## Konsekuensi Negatif
- Instrumentasi (*Instrumentation*) pada kode akan sedikit lebih kompleks karena kita harus menyisipkan *TraceID* pada *header* setiap *event* Redis.
