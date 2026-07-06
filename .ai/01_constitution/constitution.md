# AetherOS Development Constitution

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Konstitusi Pengembangan ini memuat asas arsitektural tertinggi dan aturan mutlak yang tidak boleh dilanggar oleh model AI maupun pengembang manusia di repositori AetherOS.

---

## 1. Asas Tertinggi (Core Vision)

### "Build Organizations, not Agents"
AetherOS adalah **Sistem Operasi untuk Organisasi Digital**. Setiap agen AI yang berjalan di atas AetherOS bertindak sebagai entitas pekerja yang dikendalikan oleh kebijakan birokrasi, sosial, dan hukum organisasi. Oleh karena itu, semua subsistem harus didesain sebagai komponen dari struktur organisasi (Identity, Directory, Workspace, Storage, Registry), bukan sebagai asisten personal chatbot terisolasi.

---

## 2. Aturan Mutlak (Constitutional Rules)

### 2.1. Absolute Zero Comments (Bebas Komentar Kode)
- **ATURAN MUTLAK**: Dilarang menulis komentar (`#`, `//`, `/* */`) atau docstring (`"""..."""` di dalam fungsi) di dalam file kode sumber Python yang Anda buat atau modifikasi.
- Kode wajib mendokumentasikan dirinya secara penuh melalui penamaan variabel, fungsi, dan kelas yang representatif dan semantik (*self-documenting code*).
- Seluruh penjelasan fungsional detail, tipe parameter, dan diagram urutan wajib diletakkan pada berkas Markdown (`.md`) eksternal di folder `docs/`.

### 2.2. Arah Dependensi Vertikal (ADR-0025)
- Impor dependensi murni mengalir dari bawah ke atas (*bottom-up*):
  `Level 0 (Kernel/Execution/SysPlatform) -> Level 1 (Storage/Repo/Artifact/Workspace) -> Level 2 (Workspace App) -> Level 3 (Organization) -> Level 4 (Brain/Intelligence)`.
- Dilarang keras melakukan impor horizontal lintas domain selevel secara konkret. Komunikasi lintas runtime didelegasikan via **ResourceURI** atau **Capability Resolution**.
- Kernel hanya bergantung pada abstraksi Runtime Platform dan dilarang mengimpor subsistem runtime aplikasi secara langsung.

### 2.3. Segregasi Kepemilikan Data (ADR-0024)
- Setiap runtime memiliki hak kekuasaan eksklusif atas tipe datanya sendiri.
- Subsistem dilarang memanipulasi atau menduplikasi data milik subsistem lain. (Contoh: *Repository* hanya menyimpan Graf Revisi yang merujuk ke URI Storage, sedangkan berkas fisik murni disimpan oleh *Storage*).

---

## 3. Definition of Done (DoD)

Pengembangan sebuah fitur dinyatakan selesai jika dan hanya jika memenuhi kriteria berikut secara lengkap:
1. **Kode**: Kode sumber lulus verifikasi sintaksis, bersih dari seluruh komentar kode/docstrings, dan menggunakan type-hinting yang ketat.
2. **Pengujian**: Unit test lulus 100% menggunakan `pytest` secara offline dan *in-memory* di bawah namespace yang bersangkutan.
3. **Dokumentasi**: Berkas spesifikasi runtime (`docs/id/runtime/`) dan spesifikasi arsitektur diperbarui secara sinkron.
4. **Catatan Keputusan**: Perubahan pada antarmuka publik atau kontrak wajib diawali dengan pembuatan berkas ADR baru di `docs/id/adr/` yang berstatus `Accepted`.
5. **Daftar Perubahan**: Riwayat pembaruan dicatat pada berkas Walkthrough percakapan.
