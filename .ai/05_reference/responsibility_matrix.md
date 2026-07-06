# Development Responsibility Matrix

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Dokumen ini mendefinisikan pembagian tanggung jawab peran kognitif (*Development Organization Roles*) selama model AI memproses tugas pengembangan di repositori AetherOS.

---

## 📋 Peran & Tanggung Jawab Kognitif (Role Definition)

Setiap model AI dapat mengasumsikan satu atau beberapa peran berikut selama tahapan daur hidup eksekusi:

### 1. Chief Architect (Otoritas Manusia)
- **Tujuan**: Menetapkan visi utama, memberikan instruksi tugas, menyetujui ADR/RFC, dan melakukan merge akhir.
- **Wewenang**: Otoritas tertinggi di repositori.
- **Larangan**: Tidak ada.

### 2. Architecture Reviewer (Tinjauan Arsitektur)
- **Tujuan**: Menilai keselarasan kode terhadap invariants dan mengaudit *Architecture Drift*.
- **Wewenang**: Meminta pembuatan ADR/RFC baru atau membatalkan implementasi.
- **Larangan**: Dilarang mengabaikan impor horizontal terlarang.
- **Output Wajib**: [review_contract.md](../contracts/review_contract.md).
- **Validasi Wajib**: Kepatuhan dependensi vertikal (ADR-0025) via `import-linter`.

### 3. Implementation Engineer (Implementasi Kode)
- **Tujuan**: Menulis kode sumber bersih, modular, dan terdekopel.
- **Wewenang**: Melakukan penulisan/modifikasi berkas `.py` sesuai Task Contract.
- **Larangan**: Dilarang keras menyisipkan komentar kode `#` bentuk apa pun.
- **Output Wajib**: [task_contract.md](../contracts/task_contract.md) (terisi bagian kode).
- **Validasi Wajib**: Pengetikan static typing (`mypy`) dan format syntax (`ruff`).

### 4. Documentation Engineer (Penyusunan Dokumen)
- **Tujuan**: Memelihara dan mensinkronkan seluruh berkas dokumen Markdown dan spesifikasi runtime.
- **Wewenang**: Membuat/memperbarui spesifikasi arsitektur di bawah `docs/`.
- **Larangan**: Dilarang menyalin isi kode ke dalam dokumen (gunakan referensi dinamis).
- **Output Wajib**: [documentation_contract.md](../contracts/documentation_contract.md).
- **Validasi Wajib**: Broken link scanner dan render Mermaid check.

### 5. Testing Engineer (Penjamin Mutu Tes)
- **Tujuan**: Memastikan fungsionalitas kode teruji secara offline dan in-memory.
- **Wewenang**: Menulis berkas pengujian di bawah folder `tests/`.
- **Larangan**: Dilarang memicu panggilan jaringan live.
- **Output Wajib**: [testing_contract.md](../contracts/testing_contract.md).
- **Validasi Wajib**: pytest coverage minimal (contracts/kernel 100%, execution/SDK 80%).

### 6. Repository Auditor (Audit Kualitas Kode)
- **Tujuan**: Memverifikasi keselarasan kepatuhan mutu repositori.
- **Wewenang**: Memeriksa kelulusan kriteria *Definition of Complete*.
- **Larangan**: Dilarang meloloskan PR yang melanggar invariants arsitektur.
- **Output Wajib**: [delivery_contract.md](../contracts/delivery_contract.md) -> `COMPLETION_MANIFEST.md`.
- **Validasi Wajib**: Post-Delivery Self Audit 6 pertanyaan.
