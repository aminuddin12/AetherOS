# Decision Hierarchy & Knowledge Priority

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Protokol ini mendefinisikan skala kebenaran tertulis tertinggi (*Decision Hierarchy*) dan aturan prioritas pengetahuan (*Knowledge Priority*) untuk menyelesaikan sengketa interpretasi dalam pengembangan AetherOS.

---

## 🏛️ Tangga Kebenaran Sistem (Decision Hierarchy)

Jika terjadi kontradiksi informasi, model AI wajib mematuhi hierarki keputusan dari tingkat atas ke bawah secara mutlak:

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
4. Development Constitution (.ai/01_constitution/constitution.md)
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

## 🚦 Aturan Resolusi Konflik Informasi

- **Instruksi Obrolan vs Berkas**: Keputusan instan dari Chief Architect dalam obrolan chat terbaru membatalkan keputusan tertulis sebelumnya. Namun, AI wajib mengusulkan pembuatan atau pembaruan berkas keputusan arsitektur (ADR) jika perubahan memicu pergeseran jangka panjang pada modul ter-freeze.
- **Implementasi Aktual vs Dokumentasi Terbuka**: Jika berkas panduan (`getting-started/`) menuliskan pola impor tertentu tetapi kode sumber aktual menggunakan pola lain, **kode sumber aktual adalah sumber kebenaran tertinggi**. Perbarui berkas panduan agar selaras dengan kode, bukan sebaliknya.
- **Konstitusi vs Instruksi Kotor**: Jika pengguna menginstruksikan pembuatan fungsi yang melanggar Konstitusi (misal: menyisipkan komentar kode `#`), AI wajib **menolak modifikasi tersebut secara sopan** dan merujuk ke aturan *Absolute Zero Comments* di Konstitusi.
