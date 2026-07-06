# AI Discovery Protocol

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Protokol ini mendefinisikan langkah operasional pencarian berkas di dalam repositori AetherOS agar model AI tidak berspekulasi mengenai lokasi berkas.

---

## 🚦 Pipa Pencarian Berkas (Search Sequence)

Jika Anda membutuhkan informasi spesifik mengenai implementasi atau keputusan arsitektur, Anda wajib mengikuti pipa pencarian berjenjang berikut:

```text
[Mulai Pencarian]
        │
        ▼
1. Pindai berkas /knowledge_index.md
        │
        ▼
2. Pindai direktori konkret via /02_context/repository_map.md
        │
        ▼
3. Cari ADR terkait di /docs/id/adr/
        │
        ▼
4. Cari RFC terkait di /docs/id/rfc/
        │
        ▼
5. Gunakan grep_search untuk mencari instans konkret kode aktual
        │
        ▼
[Hubungi Chief Architect jika tetap tidak ditemukan]
```

---

## 📋 Validasi Keberadaan Berkas (Existence Checks)

- Sebelum menyatakan suatu berkas "tidak ada", Anda wajib melakukan pencarian menggunakan alat bantu `grep_search` pada folder target dengan kata kunci nama modul atau tipe kelas.
- Jika berkas referensi lama yang dirujuk oleh dokumen arsitektur ternyata sudah dipindahkan, laporkan penyimpangan ini sebagai eskalasi LEVEL 2 (Architecture Uncertainty).
