# Review Contract Template

---
Status: Template
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Laporan kontrak peninjauan ini wajib diisi oleh model AI pada fase `REVIEWING` untuk membuktikan kelayakan arsitektur kode.

---

## 📋 Tinjauan Mutu Arsitektur (Architectural Review Outcomes)

- **Audit Date**: [Tanggal Audit]
- **Target Files**: [Daftar file kode yang baru dibuat/dimodifikasi]
- **Assumed Role**: `Architecture Reviewer`

---

## ❄️ Matriks Drift Detection & Kepatuhan Invariants

| Kriteria Invarian | Metode Verifikasi | Hasil Pemeriksaan (PASS/FAIL) | Catatan Temuan / Justifikasi |
|---|---|---|---|
| **Kernel Purity** | Pemeriksaan import kernel. | [PASS/FAIL] | [Jika FAIL, sebutkan import melanggar] |
| **Dependency Direction** | Uji `import-linter`. | [PASS/FAIL] | [Hasil eksekusi import-linter] |
| **Capability Isolation** | Resolusi kapabilitas subsistem. | [PASS/FAIL] | [Apakah ada pemanggilan concrete?] |
| **API Freeze compliance** | Uji signature stability. | [PASS/FAIL] | [Apakah modul stable dirusak?] |
| **Absolute Zero Comments** | Pemindaian syntax kode. | [PASS/FAIL] | [Apakah bersih dari komentar #?] |

---

## 🚦 Status Akhir Review
- **Review Status**: [APPROVED / REJECTED]
- **Outstanding Architecture Risks**: [Sebutkan risiko jika ada]
- **Reviewer Signature**: [Nama Model AI / Peran]
