# AI Operating Environment (AI-OE) Hub

---
Status: Implemented
Version: 2.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Selamat datang di **AI Operating Environment (AI-OE)** AetherOS. Direktori ini berfungsi sebagai lingkungan operasi terstruktur bagi seluruh model AI yang berkontribusi pada pengembangan repositori ini. Desain AI-OE dibuat simetris dengan **Runtime Platform** Kernel AetherOS.

> [!IMPORTANT]
> Setiap model AI yang baru masuk ke repositori wajib memulai pemuatan sesi dengan membaca **[ENTRYPOINT.md](ENTRYPOINT.md)** (Bootloader) sebagai langkah pertama.

---

## 🗂️ Indeks Hierarkis Tata Kelola (Hierarchical Navigation Hub)

Model AI wajib mematuhi seluruh berkas di bawah ini berdasarkan lapis tanggung jawabnya:

### 1. Lapisan Konstitusi (Constitution Layer)
Aturan dasar abadi arsitektur sistem dan batas etika kerja:
- **[01_constitution/repository_constitution.md](01_constitution/repository_constitution.md)**: Konstitusi repositori yang mengikat manusia dan AI (Absolute Zero Comments, dll).
- **[01_constitution/ai_constitution.md](01_constitution/ai_constitution.md)**: Aturan etika perilaku kognitif khusus bagi agen AI.
- **[01_constitution/invariants.md](01_constitution/invariants.md)**: Daftar *Architectural Invariants* abadi AetherOS.

### 2. Lapisan Kebijakan & Kontrak (Policy & Contracts Layer)
Aturan mutu statis yang membatasi modifikasi berkas:
- **[03_policy/architecture.md](03_policy/architecture.md)**: Kebijakan vertikal isolasi dan resolusi kapabilitas.
- **[03_policy/documentation.md](03_policy/documentation.md)**: Kebijakan standarisasi metadata dokumen Markdown.
- **[03_policy/testing.md](03_policy/testing.md)**: Kebijakan target cakupan uji coba offline & in-memory.
- **[03_policy/security.md](03_policy/security.md)**: Kebijakan sandbox dan perlindungan token.
- **[03_policy/quality.md](03_policy/quality.md)**: Kebijakan kelayakan merge dan static check gates.
- **[03_policy/review.md](03_policy/review.md)**: Kebijakan peninjauan arsitektural dan penolakan drift.
- **[contracts/](contracts/)**: Folder templat kontrak formal kerja kaku (Task, Review, Docs, Testing, Delivery).

### 3. Lapisan Konteks & Pengetahuan (Context & Knowledge Layer)
Pemahaman kognitif mengenai sejarah dan peta repositori:
- **[02_context/organizational_context.md](02_context/organizational_context.md)**: Orientasi filosofis mengapa organisasi mendahului agen kognitif.
- **[02_context/project_context.md](02_context/project_context.md)**: Peta orientasi status milestone dan rujukan dinamis.
- **[02_context/repository_map.md](02_context/repository_map.md)**: Navigasi batas tugas folder dan kepemilikan kapabilitas.
- **[02_context/discovery.md](02_context/discovery.md)**: Protokol pencarian berkas ADR, RFC, dan tests.
- **[02_context/repository_memory.md](02_context/repository_memory.md)**: Log memori status hidup dan risiko arsitektural aktif.
- **[repository_manifest.md](repository_manifest.md)**: Matrix status pembekuan subsistem (*Architecture Freeze Matrix*).
- **[knowledge_index.md](knowledge_index.md)**: Jalur cepat temuan referensi.
- **[NEXT_TASK_STATE.md](NEXT_TASK_STATE.md)**: Berkas status *relay/estafet* otonom antar-AI.

### 4. Lapisan Protokol & Siklus Hidup (Protocols Layer)
Jalur alur kerja operasional dinamis:
- **[04_protocol/bootstrap.md](04_protocol/bootstrap.md)**: Protokol booting inisiasi sesi AI secara deterministik.
- **[04_protocol/discovery.md](04_protocol/discovery.md)**: Protokol operasional pencarian berkas.
- **[04_protocol/execution.md](04_protocol/execution.md)**: Pipa pengerjaan 9-tahap dan Post-Delivery Self Audit.
- **[04_protocol/validation.md](04_protocol/validation.md)**: Protokol pengujian kode dan dokumen Markdown.
- **[04_protocol/change_governance.md](04_protocol/change_governance.md)**: Pipa perubahan terpilah berdasarkan klasifikasi.
- **[04_protocol/delivery.md](04_protocol/delivery.md)**: Protokol penyerahan hasil kerja dan manifest kognitif.
- **[definition_of_complete.md](definition_of_complete.md)**: Kriteria universal kelayakan penyerahan tugas.

### 5. Lapisan Validasi & Tata Kelola (Validation & Governance)
Referensi istilah baku dan pelacak keputusan taktis harian:
- **[05_reference/terminology.md](05_reference/terminology.md)**: Leksikon glosarium istilah arsitektur baku.
- **[05_reference/decision_hierarchy.md](05_reference/decision_hierarchy.md)**: Tangga kebenaran rujukan informasi.
- **[05_reference/priority_system.md](05_reference/priority_system.md)**: Matriks prioritas optimasi teknis.
- **[05_reference/responsibility_matrix.md](05_reference/responsibility_matrix.md)**: Pembagian tanggung jawab peran kognitif AI.
- **[05_reference/capability_registry.md](05_reference/capability_registry.md)**: Registri kapabilitas kognitif AI yang aktif.
- **[05_reference/repository_health.md](05_reference/repository_health.md)**: Indikator kesehatan kualitas repositori.
- **[05_reference/decision_log.md](05_reference/decision_log.md)**: Riwayat perekam keputusan taktis mikro harian.
