# Testing Protocol

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Protokol ini mendefinisikan seluruh pengujian dan validasi wajib yang harus dijalankan sebelum kode Anda dinyatakan siap untuk di-deploy ke staging/produksi atau digabungkan ke cabang utama (*main branch*).

---

## 🚦 Tipe Validasi Wajib (Validation Types)

| Tipe Validasi | Alat Bantu (Tool) | Perintah Eksekusi | Batas Kelulusan (Quality Gate) |
|---|---|---|---|
| **Unit Testing** | `pytest` | `PYTHONPATH=core/kernel:organization/src:workspace-app/src:artifact/src:repository/src:storage/src:workspace/src:runtime/src uv run python3 -m pytest <path_to_tests>` | Lulus 100% tanpa error. Berjalan offline & in-memory. |
| **Linting & Formatting** | `ruff` | `uv run ruff check .` | Bersih dari isu sintaksis dan import yang tidak efisien. |
| **Type Checking** | `mypy` / `pyright` | `uv run mypy .` | Lulus tipe data ketat (*strict type checks*). |
| **Dependency Linter** | `import-linter` | `uv run import-linter check` | Menjamin kepatuhan arah dependensi vertikal (ADR-0025). |
| **Vulnerability Check** | `safety` / `bandit` | `uv run bandit -r core/` | Bersih dari masalah keamanan (*low-risk/high-risk vulnerability*). |

---

## 🔒 Aturan Pengujian Unit (Testing Guidelines)

1. **Uji Coba Offline**: Seluruh pengetesan dilarang bergantung pada koneksi internet atau pemanggilan API LLM (OpenAI, Gemini, dll) eksternal secara aktif. Gunakan mock/stub.
2. **Uji Coba Tanpa Database Aktif**: Dilarang mewajibkan koneksi Redis, PostgreSQL, atau Qdrant aktif untuk unit test subsistem. Pengujian harus berjalan *in-memory* memanfaatkan adapter tiruan (*Mock/Memory Adapters*).
3. **Cakupan Tes Kritis (Critical Coverage)**: Modul Contracts, Kernel, dan Execution memiliki target cakupan pengujian minimal **100%**. Penggunaan stubs generator sangat disarankan untuk mencapai kriteria ini.
