# Documentation Policy

---
Status: Implemented
Version: 1.0.0
Owner: Core Platform Team
Last Updated: 2026-07-07
---

Kebijakan ini menetapkan standar pemeliharaan, metadata, dan struktur dokumentasi Markdown di repositori AetherOS.

---

## 1. Metadata Dokumen Wajib (Mandatory Document Metadata)

Setiap berkas spesifikasi runtime subsistem di bawah `docs/id/runtime/` wajib diawali dengan YAML Frontmatter terstruktur berikut:

```yaml
---
Status: [Draft | Implemented | Partially Implemented | Planned | Deprecated]
Version: X.Y.Z
Owner: [Tim Pengembang]
Last Updated: YYYY-MM-DD
---
```

---

## 2. Struktur Spesifikasi Baku (Structure Standard)

Seluruh berkas spesifikasi subsistem wajib memuat bagian-bagian berikut secara berurutan:
1. **What**: Penjelasan fungsionalitas subsistem.
2. **Why**: Justifikasi arsitektural keberadaan komponen.
3. **Responsibilities**: Batasan tanggung jawab yang jelas.
4. **Non-Responsibilities**: Batasan hal yang sengaja dikeluarkan dari lingkup tugas subsistem.
5. **Dependencies**: Daftar modul dan pustaka yang diimpor (tidak boleh melanggar ADR-0025).
6. **Public API / Contracts**: Penjelasan fasad metode yang diekspos ke SDK.

---

## 3. Aturan Kepatuhan Tautan & Mermaid (Mermaid & Link Rules)

- **No Broken Links**: Semua pranala tautan relatif wajib divalidasi keberadaannya secara berkala.
- **Mermaid Render Compliance**:
  - Quote node label yang mengandung karakter khusus: `id["Label (Kurung)"]`.
  - Dilarang keras menggunakan tag HTML di dalam label Mermaid untuk menghindari kegagalan render di penampil eksternal.
