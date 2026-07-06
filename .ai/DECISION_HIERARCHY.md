# Decision Hierarchy

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Protokol ini mengatur penyelesaian sengketa keputusan arsitektural (*conflict resolution hierarchy*). Jika terdapat pertentangan instruksi atau perbedaan antara dokumen, Anda wajib menggunakan hierarki ini sebagai pedoman kebenaran tertulis tertinggi.

---

## 🏛️ Tangga Kebenaran Sistem (Decision Hierarchy)

```text
1. Keputusan Langsung Chief Architect (Instruksi Chat Terkini)
                       │
                       ▼
2. Architecture Decision Records (ADR) Log (ADR-0001 s/d ADR-0028)
                       │
                       ▼
3. Approved Requests for Comments (RFC)
                       │
                       ▼
4. Development Constitution (.ai/DEVELOPMENT_CONSTITUTION.md)
                       │
                       ▼
5. AetherOS System Architecture Book (docs/id/architecture/book.md)
                       │
                       ▼
6. Implementasi Kode Terkini (Source Code Aktual)
                       │
                       ▼
7. Dokumen Standar Pengkodean & Gaya Pengetesan (Coding Standard)
```

---

## 🚦 Penjelasan Resolusi Konflik

- **Instruksi Chat vs ADR**: Jika Chief Architect memberikan instruksi baru di chat yang bertentangan dengan ADR yang sudah dibekukan, instruksi chat terbaru adalah hukum tertinggi yang harus dijalankan. Namun Anda harus mencatat bahwa hal tersebut melanggar ADR yang lama, dan mengusulkan draf pembaruan ADR.
- **Dokumentasi vs Kode Aktual**: Jika kode aktual menggunakan struktur kelas tertentu, tetapi dokumen arsitektur di runtime spec menuliskan hal berbeda (tanpa ada catatan ADR), **kode aktual** dianggap sebagai sumber kebenaran utama. Perbaiki dokumentasi yang salah agar selaras dengan kode, bukan sebaliknya.
- **Konstitusi vs Standar Gaya**: Jangan pernah mengorbankan integritas arsitektur (seperti batasan arah dependensi Level 0 ke Level 1) demi merapikan penulisan gaya pengkodean (*code formatting*).
