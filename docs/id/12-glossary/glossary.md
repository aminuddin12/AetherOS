# 12 — Glosarium

> Kamus istilah teknis yang digunakan dalam dokumentasi AetherOS.

---

## A

| Istilah | Definisi |
|---------|----------|
| **ADR (Architecture Decision Record)** | Dokumen historis yang merekam keputusan arsitektural penting beserta konteks dan alasannya. |
| **Agent** | Entitas otonom berbasis LLM yang memiliki peran, kemampuan, dan batasan akses spesifik dalam organisasi AetherOS. |
| **Agent Handover** | Mekanisme serah terima tugas dan konteks dari satu agen ke agen lain melalui Event Bus. |
| **AI Constitution** | Sekumpulan aturan sistem berbasis YAML yang mengatur batas etika, kebijakan, dan operasional seluruh agen AI. |
| **AI Kernel** | Lapisan abstraksi utama (OS Layer) yang memisahkan agen dari infrastruktur (event, memori, akses). |
| **API Router** | Lapisan abstraksi yang mengarahkan request ke penyedia LLM yang tepat berdasarkan preferensi, ketersediaan, dan biaya. |
| **Atomic Commit** | Operasi Git commit yang bersifat all-or-nothing — berhasil sepenuhnya atau gagal sepenuhnya tanpa state parsial. |
| **Audit Log** | Catatan permanen dari setiap aksi yang dilakukan oleh agen atau sistem, disimpan secara append-only di PostgreSQL. |
| **Automatic Fallback** | Mekanisme otomatis untuk mengalihkan request ke provider LLM alternatif ketika provider utama gagal. |

## B

| Istilah | Definisi |
|---------|----------|
| **Backpressure** | Mekanisme untuk mengelola beban berlebih pada Event Bus dengan memperlambat atau menghentikan produksi pesan. |

## C

| Istilah | Definisi |
|---------|----------|
| **Checkpoint Gate** | Titik dalam alur kerja di mana state machine membekukan eksekusi dan menunggu input manusia sebelum melanjutkan. |
| **Company Brain** | Sumber kebenaran permanen dan memori kolektif tingkat organisasi (menggantikan konsep Project Brain). |
| **Consumer Group** | Fitur Redis Streams yang memungkinkan multiple instances agen berbagi beban pemrosesan pesan. |
| **Context Injection** | Proses mengambil pengetahuan relevan dari Project Brain dan menyuntikkannya ke Working Memory agen sebelum eksekusi tugas. |
| **Context Window** | Batas jumlah token yang dapat diproses oleh LLM dalam satu request. |
| **Cost Analytics** | Sistem pelacakan biaya penggunaan token LLM secara granular per proyek, per agen, dan per tugas. |

## D

| Istilah | Definisi |
|---------|----------|
| **DAG (Directed Acyclic Graph)** | Struktur data graph yang digunakan untuk merepresentasikan task graph — tugas dan dependensi antar tugas tanpa siklus. |
| **Dead Letter Queue (DLQ)** | Antrian khusus untuk pesan yang gagal diproses setelah jumlah maksimal percobaan. |
| **Distillation** | Proses mengekstraksi dan merangkum pengetahuan terstruktur dari output kerja agen untuk disimpan ke Company Brain. |

## E

| Istilah | Definisi |
|---------|----------|
| **Embedding** | Representasi numerik (vektor) dari teks yang menangkap makna semantik, digunakan untuk similarity search di Qdrant. |
| **Event Bus** | Infrastruktur komunikasi asinkron berbasis Redis Streams yang menghubungkan semua komponen AetherOS. |
| **Event-Driven Architecture** | Pola arsitektur di mana komponen berkomunikasi melalui event, bukan pemanggilan langsung. |
| **Execution Loop** | Siklus 7 tahap yang dijalankan untuk setiap instruksi: Ingestion → Orchestration → Distribution → Execution → Validation → Persistence → Feedback. |

## H

| Istilah | Definisi |
|---------|----------|
| **Hallucination** | Ketika LLM menghasilkan output yang tidak akurat, tidak konsisten, atau berbahaya — termasuk menyebutkan file atau fungsi yang tidak ada. |
| **HITL (Human-in-the-Loop)** | Mekanisme yang memungkinkan manusia mengintervensi, meninjau, atau menyetujui tindakan AI pada titik-titik kritikal. |
| **HNSW (Hierarchical Navigable Small World)** | Algoritma indeks yang digunakan Qdrant untuk pencarian approximate nearest neighbor yang efisien. |

## I

| Istilah | Definisi |
|---------|----------|
| **Immutable Ledger** | Catatan yang tidak dapat diubah atau dihapus setelah ditulis — prinsip penyimpanan data di PostgreSQL AetherOS. |

## K

| Istilah | Definisi |
|---------|----------|
| **Knowledge Extraction Layer (KEL)** | Komponen yang secara aktif mengekstraksi wawasan terstruktur dari respons LLM sebelum disimpan ke Company Brain. |

## L

| Istilah | Definisi |
|---------|----------|
| **LangGraph** | Library Python untuk membangun stateful, graph-based workflows — digunakan AetherOS sebagai state machine engine. |
| **LLM (Large Language Model)** | Model bahasa berskala besar (GPT-4, Claude, Llama) yang digunakan sebagai mesin komputasi oleh agen. |
| **LLM Agnostic** | Prinsip di mana sistem tidak bergantung pada satu model atau penyedia LLM tertentu. |
| **Long-term Memory** | Pengetahuan yang disimpan secara permanen di Company Brain (PostgreSQL + Qdrant). |

## M

| Istilah | Definisi |
|---------|----------|
| **Meeting Memory** | Subsistem khusus untuk merekam, merangkum, dan menyimpan konteks dari interaksi manusia-AI. |
| **Model Agnosticism** | Kemampuan sistem beroperasi dengan model LLM apapun tanpa perubahan arsitektur. |

## O

| Istilah | Definisi |
|---------|----------|
| **OpenHands** | Tool Execution Layer yang menyediakan sandbox terisolasi untuk operasi file dan terminal oleh agen. |
| **OpenTelemetry** | Standar observabilitas vendor-neutral untuk distributed tracing, metrics, dan logging. |
| **Organizational Intelligence** | Kemampuan sistem belajar dari pengalaman kolektif organisasi untuk mengotomatisasi kebijakan baru secara dinamis. |
| **Outbox Pattern** | Pola desain untuk menjamin konsistensi antara dua penyimpanan data (PostgreSQL dan Qdrant). |

## P

| Istilah | Definisi |
|---------|----------|
| **PEL (Pending Entry List)** | Daftar pesan di Redis Streams yang telah dideliveri ke consumer tetapi belum di-acknowledge. |
| **Persistence First** | Prinsip bahwa pengetahuan harus disimpan secara permanen sebelum sesi berakhir. |
| **Plugin** | Bundel ekstensi (skills + configurations) yang dapat diinstal dari marketplace. |
| **Plugin SDK** | Kumpulan spesifikasi antarmuka untuk membuat ekstensi agen, tool, memory, dan API pada AetherOS. |
| **Provider Router** | Komponen yang mengabstraksi dan mengarahkan request ke berbagai penyedia LLM. |
| **PydanticAI** | Framework Python yang memberlakukan strict type-checking pada input/output agen. |

## Q

| Istilah | Definisi |
|---------|----------|
| **Qdrant** | Database vektor yang digunakan untuk menyimpan dan mencari embedding semantik dalam Company Brain. |

## R

| Istilah | Definisi |
|---------|----------|
| **RAG (Retrieval-Augmented Generation)** | Teknik di mana LLM menerima konteks yang diambil dari knowledge base sebelum menghasilkan respons. |
| **RBAC (Role-Based Access Control)** | Sistem kontrol akses berdasarkan peran agen — membatasi akses ke tools, direktori, dan aksi. |
| **Reasoning Chain** | Dokumentasi langkah-langkah berpikir agen sebelum mengambil tindakan — memungkinkan traceability dan debugging. |
| **Redis Streams** | Fitur Redis yang menyediakan persistent, append-only log — digunakan sebagai backbone Event Bus. |
| **RFC (Request for Comments)** | Dokumen usulan fitur atau perubahan arsitektural berskala besar untuk didiskusikan oleh komunitas. |

## S

| Istilah | Definisi |
|---------|----------|
| **Schema Enforcement** | Mekanisme PydanticAI yang memvalidasi setiap output LLM terhadap schema yang telah didefinisikan. |
| **Semantic Retrieval** | Pencarian berdasarkan makna (bukan kata kunci eksak) menggunakan vector similarity di Qdrant. |
| **Short-term Memory** | Konteks aktif selama satu tugas, disimpan dalam LangGraph Graph State. |
| **Skill** | Unit fungsionalitas atomik yang dapat dipanggil oleh agen — lebih kompleks dari tool, dapat di-register dinamis. |
| **State Machine** | Abstraksi yang mendefinisikan state valid dan transisi antar state — diimplementasikan dengan LangGraph. |

## T

| Istilah | Definisi |
|---------|----------|
| **Task Graph** | DAG yang merepresentasikan dekomposisi instruksi menjadi tugas-tugas dengan dependensi. |
| **Tool** | Operasi dasar yang dapat dieksekusi agen (read file, run command) — lebih sederhana dari skill. |
| **TraceID** | Identifier unik OpenTelemetry yang menghubungkan semua event dan aksi dalam satu alur instruksi. |
| **Traceability** | Prinsip bahwa setiap perubahan harus dapat dilacak ke keputusan dan reasoning chain yang menyebabkannya. |

## V

| Istilah | Definisi |
|---------|----------|
| **Vendor Lock-in** | Ketergantungan pada satu penyedia teknologi yang menyulitkan migrasi — dihindari oleh AetherOS melalui LLM Agnosticism. |

## W

| Istilah | Definisi |
|---------|----------|
| **Worker Agent** | Agen pelaksana (non-Manager) yang mengeksekusi tugas spesifik: Architect, Backend, Frontend, QA, Security, DevOps, Documentation. |
| **Working Memory** | Memori aktif selama eksekusi tugas — konteks yang langsung digunakan oleh agen, disimpan di LangGraph Graph State. |
| **Workspace** | Shared volume (Git repository) di mana agen membaca dan menulis file kode sumber. |

---

🔗 **Kembali:** [Roadmap Pengembangan ←](../11-roadmap/development-phases.md)

🔗 **Index:** [README ←](../README.md)
