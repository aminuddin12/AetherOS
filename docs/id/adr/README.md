# 🏛️ Architecture Decision Records (ADR)

Ketika AetherOS tumbuh dari kerangka kerja internal menjadi **The Open Agent Operating System**, ratusan kontributor dari berbagai organisasi akan berpartisipasi dalam pembangunannya.

ADR adalah dokumen pendek yang merekam *keputusan penting*, *kapan* keputusan itu dibuat, dan *mengapa* (konteks dan alasannya).

Dengan menyimpan sejarah ini, kita menghindari perdebatan berulang tentang pilihan teknologi yang sudah final (seperti mengapa tidak menggunakan framework X, atau kenapa memilih database Y), serta membantu developer baru memahami jiwa arsitektural proyek.

## Indeks Keputusan (ADR Log)

| ID | Keputusan Arsitektural | Status |
|---|------------------------|--------|
| [ADR-0001](0001-use-langgraph.md) | Penggunaan LangGraph untuk Orkestrasi State Machine | 🟢 Accepted |
| [ADR-0002](0002-use-redis-streams.md) | Penggunaan Redis Streams untuk Event Bus | 🟢 Accepted |
| [ADR-0003](0003-use-qdrant.md) | Penggunaan Qdrant untuk Vector Database | 🟢 Accepted |
| [ADR-0004](0004-use-postgresql.md) | Penggunaan PostgreSQL untuk Structured Ledger & Audit | 🟢 Accepted |
| [ADR-0005](0005-use-fastapi.md) | Penggunaan FastAPI untuk Gateway & API | 🟢 Accepted |
| [ADR-0006](0006-use-opentelemetry.md) | Penggunaan OpenTelemetry untuk Traceability | 🟢 Accepted |
| [ADR-0007](0007-use-pydanticai.md) | Penggunaan PydanticAI untuk Agent Runtime & Validation | 🟢 Accepted |
| [ADR-0008](0008-use-openhands.md) | Penggunaan OpenHands untuk Tool Execution Sandbox | 🟢 Accepted |

*(File draft ADR belum sepenuhnya tertulis dan akan diisi secara bertahap selama siklus pengembangan awal AetherOS).*

## Format ADR
Semua usulan perubahan arsitektural berskala besar yang telah disetujui melalui [RFC](../rfc/README.md) harus dituangkan ke dalam ADR dengan format ringkas:
1. **Konteks:** Apa masalahnya? (Mengapa kita butuh Event Bus?)
2. **Keputusan:** Solusi apa yang diambil? (Menggunakan Redis Streams).
3. **Konsekuensi Positif:** Apa keuntungannya?
4. **Konsekuensi Negatif:** Tantangan teknis apa yang harus kita terima sebagai *trade-off*?
