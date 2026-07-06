# AetherOS Repository Constitution

---
Status: Implemented
Version: 1.0.0
Owner: Core Platform Team
Last Updated: 2026-07-07
---

Konstitusi Repositori ini berisi hukum teknis arsitektur terluar yang mengikat dan berlaku universal bagi seluruh kontributor (manusia dan model AI) di repositori AetherOS.

---

## 1. Aturan Kualitas Mutlak (Universal Code Standards)

### 1.1. Absolute Zero Comments (Bebas Komentar Kode)
- **HUKUM UTAMA**: Dilarang membiarkan, menulis, atau menyisipkan komentar kode berbentuk apa pun (`#`, `//`, `/* */`, `"""docstring"""` di dalam fungsi) di dalam file kode sumber yang dibuat atau dimodifikasi.
- Kode wajib mendokumentasikan dirinya secara penuh melalui penamaan variabel, kelas, dan metode secara semantik (*self-documenting code*).
- Seluruh penjelasan arsitektur, parameter, dan daur hidup wajib diletakkan pada berkas Markdown (`.md`) eksternal di folder `docs/` atau di `.ai/`.

### 1.2. Arah Dependensi Vertikal Terisolasi (ADR-0025)
- Impor dependensi murni mengalir dari bawah ke atas (*bottom-up*):
  `Level 0 (Kernel/Execution/SysPlatform) -> Level 1 (Storage/Repo/Artifact/Workspace) -> Level 2 (Workspace App) -> Level 3 (Organization) -> Level 4 (Brain/Intelligence)`.
- Dilarang keras melakukan impor horizontal lintas subsistem selevel secara konkret. Hubungan lintas subsistem wajib didelegasikan via **ResourceURI** atau **Capability Resolution** melalui Kernel.

### 1.3. Segregasi Kepemilikan Data (ADR-0024)
- Setiap runtime subsistem memiliki otoritas penuh atas tipe datanya sendiri.
- Subsistem dilarang memanipulasi atau menduplikasi data milik subsistem lain. (Contoh: *Repository* hanya menyimpan Graf Revisi yang merujuk ke URI Storage, sedangkan berkas fisik murni disimpan oleh *Storage*).

### 1.4. Fasad Tunggal SDK (ADR-0011)
- Akses eksternal oleh aplikasi (CLI, REST, GUI) wajib melewati fasad SDK terpadu (`AetherRuntime`). Tidak diizinkan melakukan pemanggilan lintas subsistem secara ad-hoc tanpa melewati syscall SDK.

---

## 2. Integritas Arsitektur di Atas Kecepatan (Architecture Priority)
- **HUKUM INTEGRITAS**: Kontributor (khususnya model AI) dilarang keras mengutamakan kecepatan eksekusi atau keringkasan token di atas integritas arsitektur. 
- Tindakan mengambil jalan pintas cepat (*dirty workaround*) yang melanggar isolasi subsistem akan langsung ditolak secara mutlak pada tahap review merge.
