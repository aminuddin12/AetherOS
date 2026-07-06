# AI-OE Knowledge Index

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Indeks ini memetakan kategori pengetahuan utama di repositori AetherOS ke lokasinya masing-masing untuk mempercepat proses pencarian informasi oleh model AI.

---

## 🗂️ Peta Indeks Pengetahuan (Knowledge Path Map)

| Kategori Pengetahuan | Lokasi Berkas / Folder | Deskripsi Detail |
|---|---|---|
| **Landasan Arsitektur** | [book.md](../docs/id/architecture/book.md) | Penjelasan filosofi organisasi, arah dependensi vertikal, model URI, dan matrix data ownership. |
| **Keputusan Arsitektur** | [docs/id/adr/](../docs/id/adr/) | Kumpulan berkas Architecture Decision Record (ADR) berformat `ADR-XXXX-*.md`. |
| **Log Usulan Fitur** | [docs/id/rfc/](../docs/id/rfc/) | Rancangan dan spesifikasi usulan fitur sistem operasi. |
| **Spesifikasi Runtime** | [docs/id/runtime/](../docs/id/runtime/) | Detail API publik, daur hidup, dan peran masing-masing subsistem OS. |
| **Tata Kelola AI-OE** | [.ai/](ENTRYPOINT.md) | Konstitusi, kebijakan, protokol, dan referensi kerja AI Operating Environment. |
| **Kontrak Domain Publik** | [core/contracts/src/aether_contracts/](../core/contracts/src/aether_contracts/) | Berkas skema DTO (`frozen=True`) dan interface abstrak. |
| **Kode Sumber Aktual** | [AetherOS/](../) | Kode pemrograman fungsional di root repositori. |
| **Pengujian Unit & Integrasi**| [tests/](../tests/) | Berkas pengetesan offline dan in-memory. |
| **Glosarium Istilah** | [terminology.md](05_reference/terminology.md) | Daftar istilah baku yang digunakan secara konsisten dalam repositori. |
