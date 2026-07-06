# AI Execution Protocol & Completion Pipeline

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Protokol ini mendefinisikan pipa pengerjaan use-case (*Execution Pipeline*) dari awal inisiasi kontrak tugas hingga penyerahan manifest akhir.

---

## 🚦 Pipa Pengerjaan Penugasan (Execution Pipeline)

Setiap pengerjaan penugasan wajib mematuhi status daur hidup AI kognitif berikut:

```text
[Planning] ──> [Implementation] ──> [Documentation] ──> [Testing] ──> [Review] ──> [Validation] ──> [Delivery] ──> [Self Audit]
```

### 1. Planning (Perencanaan)
- **Aksi**: Muat templat `contracts/task_contract.md` dan lakukan analisis dampak (*Impact Analysis*).
- **Status**: `PLANNING`.

### 2. Implementation (Implementasi Kode)
- **Aksi**: Terapkan penulisan kode sumber murni bebas komentar sesuai dengan [repository_constitution.md](../01_constitution/repository_constitution.md).
- **Status**: `IMPLEMENTING`.

### 3. Documentation (Dokumentasi)
- **Aksi**: Sinkronisasikan spesifikasi runtime subsistem yang terdampak di `docs/id/runtime/`.
- **Status**: `RESOLVING_CONTEXT`.

### 4. Testing (Pengetesan)
- **Aksi**: Tulis pengujian unit test dan jalankan pytest suite secara offline & in-memory.
- **Status**: `TESTING`.

### 5. Review (Peninjauan Mandiri)
- **Aksi**: Jalankan pemeriksaan kepatuhan arsitektural (*Drift Detection*) sesuai [review.md](../03_policy/review.md).
- **Status**: `REVIEWING`.

### 6. Validation (Validasi Dependensi & Kualitas)
- **Aksi**: Jalankan validator `import-linter` dan pengecekan syntax statis.
- **Status**: `VALIDATING`.

### 7. Delivery (Penyerahan Manifest)
- **Aksi**: Hasil pengolahan kognitif dikumpulkan ke dalam berkas `COMPLETION_MANIFEST.md` menggunakan templat `contracts/delivery_contract.md`.
- **Status**: `COMPLETED`.

---

## 🧐 Post-Delivery Self Audit

Setelah status `COMPLETED` tercapai, AI wajib melakukan audit akhir dengan menjawab 6 pertanyaan evaluasi berikut secara eksplisit dalam pesan obrolan:

1. **Dependency Direction**: Apakah perubahan ini melanggar arah dependensi vertikal bottom-up (ADR-0025)?
2. **Contracts Change**: Apakah ada kontrak publik di `core/contracts/` yang berubah tanpa persetujuan ADR baru?
3. **ADR Consistency**: Apakah implementasi ini konsisten dengan ADR aktif?
4. **Docs Sync**: Apakah dokumentasi runtime spec telah disinkronisasikan penuh dengan kode aktual?
5. **Scope Control**: Apakah ada fungsionalitas yang melebar (*scope creep*) di luar batasan *Non-Goals* Task Contract?
6. **Core Vision**: Apakah solusi ini mempertahankan filosofi utama "Build Organizations, not Agents"?
