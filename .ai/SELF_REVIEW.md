# Self Review Guide

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Sebelum Anda mengirimkan hasil pengerjaan kode atau laporan akhir ke Chief Architect, Anda **wajib** mengajukan dan menjawab pertanyaan audit mandiri di bawah ini secara jujur.

---

## 🧐 Lembar Evaluasi Mandiri AI (Self-Review Checklist)

### 1. Kepatuhan Konstitusi & ADR
- [ ] **Bebas Komentar**: Apakah ada karakter komentar (`#`, `//`, `/* */`) atau docstring Python yang tertinggal di dalam kode sumber yang baru dibuat atau dimodifikasi? *(Jika ada, hapus segera).*
- [ ] **Pemisahan Ketergantungan**: Apakah perubahan ini mengimpor langsung modul eksternal terlarang atau dependensi melintang horizontal?
- [ ] **Data Ownership**: Apakah subsistem ini mencoba menulis atau memanipulasi berkas penyimpanan secara langsung tanpa melewati Storage/Repository?

### 2. Kepatuhan Antarmuka & API
- [ ] **API Stability**: Apakah ada rute API publik yang bertanda `[Stable]` mengalami perubahan tipe data parameter atau dihapus?
- [ ] **Capability Contract**: Apakah ada kapabilitas runtime baru yang tidak terdaftar dalam `Provides` descriptor?

### 3. Penyelarasan Dokumen & Pengujian
- [ ] **Dokumentasi Subsistem**: Apakah `docs/id/runtime/<subsystem>.md` sudah diperbarui untuk menerangkan perubahan terbaru?
- [ ] **README Lokal**: Apakah `README.md` pada modul subsistem sudah sinkron?
- [ ] **Unit Testing**: Apakah cakupan pengujian unit test bertambah seiring bertambahnya logic baru?
- [ ] **Pytest Pass**: Apakah seluruh tes berhasil dijalankan secara in-memory?

### 4. Evaluasi Rekayasa Mutu
- [ ] **Technical Debt**: Apakah implementasi ini bersih dari workaround kotor?
- [ ] **Peer Acceptance**: Apakah co-architect atau insinyur senior lain akan menyetujui perubahan ini tanpa catatan penolakan?
- [ ] **Consistency**: Apakah penamaan simbol kelas (`PascalCase`) dan metode/variabel (`snake_case`) sudah konsisten dengan leksikon glosarium?
