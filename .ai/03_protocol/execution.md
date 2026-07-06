# AI Execution & Completion Pipeline

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Berkas ini mengonsolidasikan protokol eksekusi pengembangan dan pipa penyelesaian tugas secara berurutan dan terstruktur bagi model AI.

---

## 🚦 Pipa Penyelesaian Tugas (Completion Pipeline)

Setiap pengerjaan tugas wajib melewati 8 tahap pipa penyelesaian di bawah ini:

```text
[Planning] ──> [Implementation] ──> [Documentation] ──> [Testing] ──> [Review] ──> [Validation] ──> [Final Verification] ──> [Delivery]
```

### 1. Planning (Perencanaan)
- Buat rencana kerja internal sebelum menulis kode.
- Tentukan apakah perubahan memerlukan pembuatan ADR atau pembaruan RFC.

### 2. Implementation (Implementasi Kode)
- Tulis kode sumber murni bebas komentar/docstrings.
- Lakukan type-hinting ketat dan gunakan Pydantic V2 untuk DTO.

### 3. Documentation (Dokumentasi)
- Perbarui dokumentasi runtime spec (`docs/id/runtime/`) dan spesifikasi teknis jika ada perubahan antarmuka.
- Regenerasi diagram Mermaid jika daur hidup subsistem berubah.

### 4. Testing (Pengetesan)
- Tulis pengujian unit test baru di bawah namespace yang bersangkutan.
- Pastikan tes berjalan secara in-memory dan offline.

### 5. Review (Peninjauan Mandiri)
- Evaluasi seluruh kode sumber yang dimodifikasi terhadap kriteria lembar audit mandiri di [Self Review Guide](../03_protocol/review.md) (termasuk verifikasi bebas komentar).

### 6. Validation (Validasi Arsitektur)
- Jalankan pemeriksaan kepatuhan dependensi vertikal menggunakan `import-linter` (ADR-0025).

### 7. Final Verification (Verifikasi Akhir)
- Eksekusi test suite terpusat:
  `PYTHONPATH=core/kernel:organization/src:workspace-app/src:artifact/src:repository/src:storage/src:workspace/src:runtime/src uv run python3 -m pytest <path_to_tests>`
- Pastikan semua tes lulus 100%.

### 8. Delivery (Penyerahan Hasil)
- Kirimkan kode mentah yang siap digunakan oleh Chief Architect tanpa ada tambahan basa-basi percakapan.

---

## 🔄 Matriks Sinkronisasi Dampak Berkas (Sync Matrix)

AI dilarang menghentikan pekerjaan sebelum menyelaraskan berkas-berkas berikut jika terpengaruh oleh perubahan kode:

| Cakupan Modifikasi | Berkas yang WAJIB Diselaraskan secara Otomatis |
|---|---|
| Kontrak Domain Baru | - `core/contracts/` (Pemberian skema model `frozen=True`) |
| Perubahan Daur Hidup Platform | - `core/kernel/sys_platform/graph.py` (Update dependency node)<br/>- `docs/id/architecture/book.md` (Update Mermaid flowchart) |
| Perbaikan Fungsionalitas | - `docs/id/runtime/` (Update dokumentasi runtime terkait) |
| Penambahan Unit Tests | - `tests/` (Tambah tes koresponden) |
| Status Rilis Milestone | - `ROADMAP.md` (Pembaruan status kelulusan milestones) |
