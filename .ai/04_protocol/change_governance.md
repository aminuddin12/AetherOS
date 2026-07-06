# AI Change Governance Protocol

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Protokol ini mendefinisikan pipa pengerjaan terpilah (*Change Governance Pipeline*) berdasarkan klasifikasi jenis perubahan berkas di repositori AetherOS.

---

## 🚦 Klasifikasi Perubahan & Jalur Pengerjaan (Change Classification)

AI wajib menentukan klasifikasi perubahan sebelum mulai menulis kode guna menghemat token dan mereduksi pengujian yang berlebihan:

| Klasifikasi Perubahan | Cakupan Berkas | Alur Pipa Pengerjaan Wajib (Change Pipeline) |
|---|---|---|
| **Architecture Change** | `core/contracts/`, `core/kernel/sys_platform/` | **Pipeline Lengkap**: Idea -> RFC -> ADR -> Implementation -> Docs -> Tests -> Review -> Validation -> Merge. |
| **Structural Change** | Menambah modul subsistem baru (Level 1) | **Pipeline Standar**: ADR -> Implementation -> Docs -> Tests -> Review -> Validation. |
| **Behavior Change** | Mengubah logic aplikasi (`workspace-app/`) | **Pipeline Fungsional**: Implementation -> Tests -> Review -> Validation. |
| **Documentation Change**| Berkas spesifikasi di `docs/` | **Pipeline Dokumen**: Modification -> Relative Link Validation -> Metadata sync -> Merge. |
| **Refactoring / Bug Fix**| Pembersihan kode atau perbaikan fungsi | **Pipeline Mutu**: Implementation -> Test run -> Code Quality checks -> Merge. |

---

## 🚦 Kebijakan Validasi Terarah (Targeted Validation)

- **Architecture Change**: Memerlukan 100% kelulusan peninjauan statis (`import-linter`, `ruff`, `mypy`) dan 100% kelulusan seluruh pytest suite.
- **Documentation Change**: Dilepaskan dari keharusan menjalankan pytest suite Python. Fokus murni pada pemeriksaan kebenaran broken links relatif dan diagram Mermaid.
