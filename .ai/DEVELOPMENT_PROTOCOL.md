# Development Protocol

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Protokol ini mendefinisikan pipa eksekusi (*mandatory execution pipeline*) yang wajib diikuti oleh model AI pada setiap tugas. Anda wajib memproses instruksi Chief Architect melalui tahapan-tahapan di bawah ini secara linier tanpa melompati satu fase pun.

---

## 🏗️ Pipa Eksekusi AI (Execution Pipeline)

```text
[Menerima Tugas]
       │
       ▼
1. Muat Tata Kelola & Konstitusi (.ai/)
       │
       ▼
2. Analisis Konteks Repositori & Kode Aktual (Source Code)
       │
       ▼
3. Verifikasi Status Milestone & ADR Terkait
       │
       ▼
4. Lakukan Audit Arsitektur Awal (Pre-implementation Review)
       │
       ▼
5. Eksekusi Perubahan Kode (Terapkan Aturan Bebas Komentar)
       │
       ▼
6. Sinkronisasi Dokumentasi & Tulis Ulang Unit Tests
       │
       ▼
7. Jalankan Self-Review & Verifikasi Pytest
       │
       ▼
[Kirim Hasil Kode Mentah / Raw Output]
```

---

## 🔍 Detail Setiap Tahapan Protokol

### Tahap 1: Memuat Konstitusi & Tata Kelola
- Muat berkas `.ai/DEVELOPMENT_CONSTITUTION.md` dan `.ai/DECISION_HIERARCHY.md`.
- Identifikasi aturan mutlak yang membatasi ruang tugas Anda (seperti larangan menyisipkan komentar).

### Tahap 2: Analisis Kode Aktual
- Gunakan pencarian repositori untuk menganalisis kode yang saat ini berjalan pada repositori.
- **Dilarang keras berasumsi**. Jika ada ketidakcocokan antara dokumentasi dan kode sumber, kode sumber adalah kebenaran tunggal (*source of truth*).

### Tahap 3: Verifikasi ADR & RFC
- Baca indeks ADR di `docs/id/adr/README.md` dan RFC terkait.
- Pastikan perubahan Anda tidak melanggar keputusan arsitektur yang telah disetujui sebelumnya.

### Tahap 4: Pre-implementation Review
- Lakukan review berdasarkan **[Review Protocol](REVIEW_PROTOCOL.md)** sebelum menulis kode apa pun.
- Jika terdeteksi potensi kerusakan arsitektur atau depresi kegagalan kaskade, berikan laporan audit terlebih dahulu kepada Chief Architect.

### Tahap 5: Implementasi Kode
- Tulis kode dengan type-hinting yang ketat, Pydantic model jika berupa DTO, dan terisolasi dari dependensi terlarang.
- **Hapus komentar**: Pastikan tidak ada karakter `#` di luar deklarasi string literal multiline atau file konfigurasi.

### Tahap 6: Sinkronisasi Dokumen & Tes
- Jika API berubah, perbarui berkas spesifikasi subsistem (`docs/id/runtime/`) dan daftarkan status stabilitasnya di `docs/id/sdk/api.md`.
- Tulis ulang unit test di bawah sub-folder `/tests/` atau direktori tes subsistem terkait.

### Tahap 7: Verifikasi & Pengiriman
- Jalankan pengujian unit lokal untuk memverifikasi fungsionalitas kode baru.
- Kirimkan keluaran berupa kode mentah (*raw output*) bebas dari basa-basi percakapan (*conversational filler*).
