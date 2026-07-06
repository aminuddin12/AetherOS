# Architectural Invariants

---
Status: Implemented
Version: 1.0.0
Owner: Core Platform Team
Last Updated: 2026-07-07
---

Peti panduan ini mencatat **Architectural Invariants** (aturan abadi arsitektur) AetherOS yang mutlak tidak boleh tersentuh perubahan atau di-bypass oleh modifikasi kode apa pun.

---

## 🏛️ Invarian Arsitektur Abadi (Architectural Invariants)

1. **Kernel Independence (Kemurnian Kernel)**: Kernel harus tetap mandiri dan terisolasi. Kernel dilarang mengimpor atau bergantung secara langsung pada subsistem runtime tingkat atas (Storage, Repository, Artifact, Workspace, dll).
2. **Dependency Direction (Arah Dependensi)**: Aliran impor dependensi bersifat vertikal searah ke bawah (*bottom-up*). Arah dependensi ini tidak boleh dibalik (*never be reversed*).
3. **Capabilities Over Concrete**: Pemanggilan lintas subsistem harus diselesaikan menggunakan resolusi kapabilitas abstrak (`CapabilityResolver`), bukan instansiasi kelas konkret subsistem lain secara langsung.
4. **Organization Precedes Agent (Organisasi Mendahului Agen)**: Subsistem tata kelola dan hak akses organisasi wajib dibangun dan diselesaikan sebelum runtime agen pintar dapat dideklarasikan secara fungsional.
5. **Workspace is a Runtime, Not a Folder (Workspace Sebagai Runtime)**: Workspace didefinisikan sebagai batas isolasi komputasional dinamis (*Aggregate Root Runtime*), bukan sekadar folder fisik atau direktori kerja lokal.
6. **Contract-Driven Architecture**: Semua pertukaran data antar lapisan wajib dijembatani oleh kontrak terbekukan (`core/contracts/`), bukan pertukaran objek kelas internal secara mentah.
7. **Public API Stability**: Seluruh tanda tangan API publik yang berlabel `[Stable]` tidak boleh diubah atau dirusak setelah menyentuh status *API Freeze*.
8. **Documentation Follows Implementation**: Berkas dokumentasi arsitektur dan spesifikasi runtime wajib diperbarui secara sinkron seiring dengan adanya perubahan fungsional kode aktual.
9. **The Repository is the Single Source of Truth**: Kode sumber aktual dan ADR yang disetujui adalah kebenaran sistem tertinggi di atas dokumen panduan.
