# Quality Policy

---
Status: Implemented
Version: 1.0.0
Owner: Core Platform Team
Last Updated: 2026-07-07
---

Kebijakan Kualitas ini menetapkan tolok ukur kelayakan mutu kode sumber untuk dapat digabungkan (*merge*) ke dalam cabang utama repositori.

---

## 1. Persyaratan Pengkodean Bersih (Clean Code Gates)

1. **Absolute Zero Comments**: File kode harus benar-benar bersih dari seluruh komentar atau docstring Python.
2. **Strict Typing**: Seluruh deklarasi fungsi wajib memiliki pengetikan statis yang kaku (*type hinting*) untuk parameter dan nilai kembalian.
3. **No Workarounds**: Implementasi dilarang menggunakan workaround cepat yang bertentangan dengan kebersihan desain sistem (misalnya: modifikasi langsung state tanpa melalui service resolver).

---

## 2. Pemeriksaan Statis Wajib (Quality Gates)

Setiap Pull Request wajib melewati pemeriksaan statis berikut:
- **Linting**: Bersih dari peringatan linting `ruff check .`.
- **Type Check**: Lulus verifikasi pengetekan statis `mypy .` atau `pyright`.
- **Arah Dependensi**: Lulus verifikasi `import-linter` sesuai batasan ADR-0025.
- **Dua Persetujuan**: Memerlukan minimal dua tinjauan sukses (dari `Architecture Reviewer` dan `Quality Auditor`).
