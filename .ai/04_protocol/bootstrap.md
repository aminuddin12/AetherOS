# AI Bootstrap Protocol

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Protokol ini mendefinisikan sekuens inisialisasi kognitif AI secara deterministik untuk pemuatan konteks proyek sebelum mulai memproses instruksi.

---

## 🚦 AI Boot sequence Phases

Model AI wajib mengeksekusi 6 fase berikut secara berurutan:

### Phase 1: Load Constitution
- **Objective**: Memuat konstitusi repositori dan batasan arsitektur mutlak.
- **Required Input**: `01_constitution/repository_constitution.md` dan `01_constitution/ai_constitution.md`.
- **Expected Output**: Kepatuhan terhadap aturan Absolute Zero Comments dan arah dependensi.
- **Success Criteria**: AI memuat dan menyetujui semua aturan konstitusi.
- **Failure Handling**: Jika berkas konstitusi hilang, cari di fallback `/docs/id/getting-started/quickstart.md`. Jika tetap gagal, batalkan eksekusi.
- **Escalation Rule**: LEVEL 4 (Stop).
- **Next Step**: Phase 2.

### Phase 2: Load Invariants & Context
- **Objective**: Memahami arsitektur abadi dan identitas filosofis organisasi AetherOS.
- **Required Input**: `01_constitution/invariants.md`, `02_context/organizational_context.md`, dan `02_context/project_context.md`.
- **Expected Output**: Pemahaman mengapa subsistem Organisasi mendahului Agen.
- **Success Criteria**: Resolusi konteks organisasi lengkap.
- **Failure Handling**: Muat `docs/id/architecture/book.md`.
- **Escalation Rule**: LEVEL 3 (ADR required).
- **Next Step**: Phase 3.

### Phase 3: Resolve Project Memory
- **Objective**: Memuat status milstone aktif dan memori perkembangan harian.
- **Required Input**: `02_context/repository_memory.md` dan `repository_manifest.md`.
- **Expected Output**: Pemetaan milstone aktif (saat ini M3.7 completed / M4 active).
- **Success Criteria**: AI memetakan matrix pembekuan subsistem (*Architecture Freeze Matrix*).
- **Failure Handling**: Baca `ROADMAP.md` di root folder.
- **Escalation Rule**: LEVEL 2 (Uncertainty).
- **Next Step**: Phase 4.

### Phase 4: Load Discovery Rules & Maps
- **Objective**: Memetakan struktur direktori konkret dan aturan penemuan berkas.
- **Required Input**: `02_context/repository_map.md` dan `02_context/discovery.md`.
- **Expected Output**: AI mengetahui batas modul dan letak ADR/RFC/Tests.
- **Success Criteria**: Pemetaan folder selesai tanpa tebak-tebakan.
- **Failure Handling**: Pindai struktur direktori root menggunakan pencarian direktori.
- **Escalation Rule**: LEVEL 3 (ADR required).
- **Next Step**: Phase 5.

### Phase 5: Resolve Capabilities & Role
- **Objective**: Mengaktifkan kemampuan kognitif yang diperlukan dan mencocokkan peran AI.
- **Required Input**: `05_reference/capability_registry.md` dan `05_reference/responsibility_matrix.md`.
- **Expected Output**: Aktivasi peran (seperti *Implementation Engineer*).
- **Success Criteria**: AI mencatat kapabilitas aktif untuk tugas bersangkutan.
- **Failure Handling**: Aktifkan mode dasar *Implementation* dan *Testing* secara default.
- **Escalation Rule**: LEVEL 1 (AI continues).
- **Next Step**: Phase 6.

### Phase 6: Initialize Task Contract
- **Objective**: Menerima instruksi Chief Architect dan mengubahnya menjadi kontrak formal.
- **Required Input**: `contracts/task_contract.md`.
- **Expected Output**: Dokumen Task Contract terisi lengkap.
- **Success Criteria**: Pembentukan Task Contract selesai.
- **Failure Handling**: Hentikan eksekusi, minta penjelasan Chief Architect.
- **Escalation Rule**: LEVEL 4 (Stop).
- **Next Step**: Mulai eksekusi tugas di bawah status daur hidup `PLANNING`.
