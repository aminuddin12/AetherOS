# Development Constitution

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Konstitusi Pengembangan ini memuat aturan dasar tertinggi yang mengikat dan tidak dapat dinegosiasikan. Pelanggaran terhadap salah satu aturan di bawah ini secara otomatis membatalkan seluruh Pull Request atau kode yang Anda hasilkan.

---

## 1. Asas Utama: "Build Organizations, not Agents"

AetherOS beroperasi sebagai **Sistem Operasi untuk Organisasi Digital**, bukan sekadar kumpulan agen pintar yang berdiri sendiri. 
Setiap kali mendesain subsistem baru:
- **TIDAK BOLEH** menganggap subsistem sebagai chatbot.
- **WAJIB** merancang subsistem sebagai komponen modular dari sebuah tata kelola organisasi (Identity, Directory, Workspace, Storage, Registry).

---

## 2. Aturan Konstitusi yang Tidak Boleh Dilanggar (Absolute Rules)

### 2.1. Absolute Zero Comments (Bebas Komentar Kode)
- **MUTLAK**: Dilarang membiarkan, menyisipkan, atau menulis komentar kode bentuk apa pun (`//`, `/* */`, `#`, `"""docstring"""` di dalam fungsi) di dalam file kode sumber yang Anda buat atau modifikasi.
- Kode wajib mendokumentasikan dirinya secara penuh melalui penamaan variabel, fungsi, dan kelas yang representatif dan semantik (*self-documenting code*).
- Seluruh penjelasan detail arsitektur, parameter, dan daur hidup wajib diletakkan pada berkas Markdown (`.md`) eksternal di bawah folder `docs/` atau direktori `.ai/`.

### 2.2. Arah Dependensi Vertikal (ADR-0025)
- Aliran impor dependensi murni mengalir dari bawah ke atas (*bottom-up*):
  `Level 0 (Kernel/Execution) -> Level 1 (Storage/Repo/Artifact/Workspace) -> Level 2 (Workspace App) -> Level 3 (Organization) -> Level 4 (Brain/Intelligence)`.
- Dilarang keras melakukan impor horizontal lintas domain selevel secara konkret. Komunikasi lintas runtime didelegasikan via **ResourceURI** atau **Capability Resolution**.

### 2.3. Kepemilikan Data Tersegmentasi (ADR-0024)
- Setiap runtime memiliki hak kekuasaan penuh atas jenis datanya sendiri.
- Subsistem dilarang memanipulasi atau memiliki duplikat data milik subsistem lain (misal: *Repository* hanya menyimpan Graf Revisi yang merujuk ke URI Storage, sedangkan berkas fisik murni disimpan oleh *Storage*).

### 2.4. Fasad Tunggal SDK (ADR-0011)
- Akses eksternal oleh aplikasi (CLI, REST, GUI) wajib melewati fasad SDK terpadu (`AetherRuntime`). Tidak diizinkan melakukan pemanggilan lintas subsistem secara ad-hoc tanpa melewati perantara syscall SDK.

---

## 3. Definition of Done (DoD)

Sebuah tugas pengembangan dinyatakan selesai jika dan hanya jika memenuhi kriteria berikut:
1. **Lulus Linting & Tes**: Unit test lulus 100% menggunakan `pytest` secara offline dan in-memory.
2. **Tanpa Komentar**: File kode bebas dari komentar dan docstring Python.
3. **Pembaruan Berkas**: Dokumen spesifikasi terkait (`docs/id/runtime/`, `docs/id/specifications/`) diperbarui secara sinkron.
4. **Pembaruan ADR/RFC**: Jika terjadi perubahan kontrak publik, ADR baru harus diusulkan dan didokumentasikan di `docs/id/adr/`.
5. **Daftar Perubahan**: Walkthrough diperbarui untuk mencatat riwayat implementasi.
