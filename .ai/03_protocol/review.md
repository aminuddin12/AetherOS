# AI Review & Architecture Drift Detection Protocol

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Berkas ini mengonsolidasikan panduan pemeriksaan mandiri (*Self Review*) dan audit penyimpangan arsitektur (*Architecture Drift Detection*) sebelum dan sesudah penulisan kode.

---

## 1. Pre-Implementation Review Checklist

Model AI wajib memvalidasi hal berikut sebelum melakukan perubahan kode:

- [ ] **Batas Pengaruh Impor (Kernel Purity)**: Apakah perubahan ini memaksa Kernel untuk mengimpor atau bergantung pada subsistem runtime aplikasi (seperti Storage, Workspace, dll)? *(Kernel hanya boleh bergantung pada sys_platform dan contracts).*
- [ ] **Arah Dependensi Vertikal (ADR-0025)**: Apakah kode baru melanggar aliran impor *bottom-up*?
- [ ] **Stabilitas API**: Apakah perubahan merusak tanda tangan API yang dilabeli `[Stable]` di `docs/id/sdk/api.md`?
- [ ] **Isolasi Kapabilitas (Capability Isolation)**: Apakah subsistem ini mencoba memanggil subsistem lain secara langsung tanpa menggunakan resolusi kapabilitas abstrak (`CapabilityResolver`)?

---

## 2. Post-Implementation Drift Detection (Audit Penyimpangan)

Gunakan matriks audit ini untuk memastikan kode akhir Anda tidak mengalami pergeseran desain arsitektur (*architecture drift*):

| Jenis Pemeriksaan | Deskripsi Deteksi | Ambang Toleransi (Tolerance) |
|---|---|---|
| **Drift Struktur Platform** | Modul memanggil dependensi concrete runtime bypass `sys_platform/manager.py`. | **NOL (0 toleransi)**. Instansiasi concrete wajib di-host oleh manager. |
| **Drift Purity Kernel** | Komponen kernel mengimpor runtime aplikasi di atasnya. | **NOL**. CI/CD block on import linter fail. |
| **Drift Komparasi ADR** | Kode tidak menerapkan keputusan yang dibekukan di ADR. | **NOL**. Wajib patuh ADR aktif. |
| **Drift Komparasi RFC** | Detail implementasi menyimpang dari dokumen rancangan RFC yang disetujui. | **NOL**. Desain harus presisi dengan RFC. |

---

## 3. Lembar Evaluasi Mandiri AI (Self-Review Checklist)

Sebelum menyerahkan hasil akhir ke Chief Architect, tanyakan pertanyaan berikut:
1. **Did I violate an ADR/RFC?** (Apakah saya melanggar ADR/RFC aktif?)
2. **Did I introduce a breaking API?** (Apakah saya merusak API publik tanpa depresiasi?)
3. **Did I update documentation & tests?** (Apakah saya memperbarui dokumen runtime spec dan unit test?)
4. **Did I check for comments?** (Apakah saya menjamin kode 100% bebas komentar `#`?)
5. **Would another architect approve this change?** (Apakah arsitek senior lain akan menyetujui kode ini tanpa catatan penolakan?)
