# Priority System

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Protokol ini mendefinisikan skala prioritas optimasi kode dan arsitektur sistem. Ketika Anda menghadapi keterbatasan sumber daya (seperti batas token output) atau trade-off teknis, gunakan daftar ini sebagai panduan penentu prioritas utama.

---

## 📈 Urutan Prioritas Optimasi (System Priorities)

```text
1. Integritas Arsitektur (Architecture Integrity)
                   │
                   ▼
2. Konsistensi Repositori (Repository Consistency)
                   │
                   ▼
3. Stabilitas API (API Stability & Stability Labels)
                   │
                   ▼
4. Akurasi Dokumentasi (Documentation Accuracy)
                   │
                   ▼
5. Ketepatan Fungsionalitas & Pengujian (Correctness & Testing)
                   │
                   ▼
6. Performa Sistem (Boot/Execution Latency)
                   │
                   ▼
7. Gaya Kode (Formatting & Lint Rules Compliance)
```

---

## 🚦 Aturan Penerapan Prioritas

- **Batas Token Output (Mass Operations)**: Jika Anda sedang melakukan refactoring massal pada satu direktori besar dan mendekati batas limit token keluaran model AI, **TIDAK BOLEH** memotong kode menjadi tidak lengkap. Hentikan eksekusi secara bersih dan kembalikan pesan:
  `PAUSED: Awaiting 'continue' to process the next batch.`
- **Integritas vs Performa**: Jangan pernah mengorbankan isolasi dependensi (ADR-0025) untuk menghemat sedikit latensi startup. Modularitas dan kebersihan arsitektur sistem selalu diutamakan dibanding optimasi mikro-latensi.
- **Integritas vs Gaya Kode**: Kepatuhan terhadap aturan arsitektur mutlak (seperti bebas komentar kode) adalah harga mati. Dilarang membiarkan komentar kotor berada di dalam berkas Python hanya karena modul eksternal merekomendasikan penulisan docstrings.
