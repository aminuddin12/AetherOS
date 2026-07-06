# Task Contract Template

---
Status: Template
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Sebelum melakukan modifikasi kode sumber, isilah templat kontrak tugas berikut untuk disepakati bersama Chief Architect.

---

## 📋 Detail Kontrak Penugasan (Task Assignment Details)

### 1. Informasi Dasar
- **Task ID**: [Misal: TASK-0024]
- **Task Title**: [Judul Penugasan]
- **Objective**: [Tujuan utama dari fungsionalitas/logic yang akan ditambahkan]

### 2. Konteks Arsitektur & Intensi
- **Architectural Intent**: [Menerangkan secara mendalam maksud arsitektural di balik pengerjaan ini, misal: menjaga kemurnian kernel dengan menyisipkan layer isolasi]
- **Non-Goals**:
  - [Daftar batasan hal yang sengaja dikeluarkan untuk menghindari perluasan cakupan kerja / scope creep]
  - [Dilarang memodifikasi interface inti]
- **Architectural Invariants Affected**: [Invarian mana saja yang terlibat, misal: Kernel Independence]

### 3. Analisis Dampak Repositori (Repository Impact Analysis)
AI wajib mengklasifikasikan perubahan dan menjawab pertanyaan dampak berikut sebelum coding:

- **Change Classification**: [Architecture Change | Structural Change | Behavior Change | Documentation | Refactoring]
- **Affected Runtime**: [Subsistem mana saja yang terpengaruh]
- **Affected Contracts**: [Apakah merubah file di core/contracts/? Ya/Tidak]
- **Affected Public API**: [Apakah mengubah signature publik di runtime/? Ya/Tidak]
- **Affected Documentation**: [Daftar file spesifikasi docs/ yang wajib diperbarui]
- **Affected Tests**: [Daftar file unit test baru/lama yang wajib dirubah/dijalankan]
- **Migration Required**: [Ya/Tidak]
- **Backward Compatible**: [Ya/Tidak]

### 4. Input & Expected Outputs
- **Inputs**: [Konteks awal, variabel, file input]
- **Expected Outputs**: [Kode sumber fungsional bebas komentar, unit tests, update dokumentasi]

### 5. Required Validation & Completion Criteria
- **Required Validation**: [Sebutkan alat bantu uji coba, misal: pytest, import-linter]
- **Completion Criteria**: [Kriteria kelayakan khusus tugas ini sesuai Definition of Complete]
