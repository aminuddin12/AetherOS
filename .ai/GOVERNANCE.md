# AI Operating Environment (AI-OE) Hub

---
Status: Implemented
Version: 2.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Selamat datang di **AI Operating Environment (AI-OE)** AetherOS. Direktori ini berfungsi sebagai lingkungan operasi terstruktur bagi seluruh model AI yang berkontribusi pada pengembangan repositori ini. Desain AI-OE dibuat simetris dengan **Runtime Platform** Kernel AetherOS.

---

## 🗂️ Indeks Hierarkis Tata Kelola (Hierarchical Navigation Hub)

Model AI wajib mematuhi seluruh berkas di bawah ini berdasarkan tingkat kepentingannya:

### 1. Inisialisasi & Asas Tertinggi (Bootstrap & Constitution)
- **[00_bootstrap/bootstrap.md](00_bootstrap/bootstrap.md)**: Prosedur booting inisiasi sesi AI, daur hidup (*AI Lifecycle*), dan urutan pemuatan konteks sistem.
- **[01_constitution/constitution.md](01_constitution/constitution.md)**: Asas filosofis tertinggi ("Build Organizations, not Agents") dan aturan mutlak yang tidak boleh dilanggar (seperti larangan menyisipkan komentar).

### 2. Peta Konteks & Lokasi (Context Registry & Discovery)
- **[02_context/project_context.md](02_context/project_context.md)**: Ringkasan roadmap aktif, pencapaian milestone, dan rujukan non-duplikasi ke berkas state proyek.
- **[02_context/architecture_context.md](02_context/architecture_context.md)**: Ringkasan arsitektur 5-layer AetherOS dan tabel kesetaraan konseptual antara Runtime Platform dan AI-OE.
- **[02_context/repository_map.md](02_context/repository_map.md)**: Peta tanggung jawab direktori subsistem dan batasan dependensi impor antar folder.
- **[02_context/discovery.md](02_context/discovery.md)**: Protokol untuk mendeteksi letak berkas ADR, RFC, pengujian unit test, dan kontrak domain.

### 3. Protokol Operasi & Mutu (Protocols)
- **[03_protocol/behavior.md](03_protocol/behavior.md)**: Standar perilaku AI (komunikasi, penalaran, eskalasi kritis, dan penolakan instruksi kotor).
- **[03_protocol/execution.md](03_protocol/execution.md)**: Jalur pipa eksekusi use-case (*Execution Pipeline*) dan kriteria Definition of Done (DoD).
- **[03_protocol/review.md](03_protocol/review.md)**: Prosedur audit mandiri dan deteksi penyimpangan desain arsitektur (*Architecture Drift Detection*).
- **[03_protocol/testing.md](03_protocol/testing.md)**: Aturan penulisan unit test dan validasi dokumentasi (pengecekan broken links dan rendering grafis Mermaid).

### 4. Kamus & Hierarki Keputusan (Reference & Decision Hierarchy)
- **[04_reference/terminology.md](04_reference/terminology.md)**: Kamus leksikon resmi dengan definisi tunggal terikat untuk istilah arsitektur.
- **[04_reference/decision_hierarchy.md](04_reference/decision_hierarchy.md)**: Urutan rujukan kebenaran jika terjadi kontradiksi informasi.
- **[04_reference/priority_system.md](04_reference/priority_system.md)**: Matriks prioritas optimasi teknis.
