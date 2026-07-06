# Repository Discovery Protocol

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Peti panduan ini membantu kontributor untuk menemukan berkas referensi utama (ADR, RFC, pengujian, contoh, dan kontrak) tanpa perlu menebak lokasi berkas.

---

## 🔍 Lokasi Penemuan Berkas (Discovery Index)

### 1. Menemukan Keputusan Arsitektur (ADR)
- **Log Utama**: [docs/id/adr/README.md](../../docs/id/adr/README.md)
- **Berkas Detil**: Seluruh berkas ADR aktif disimpan dengan format penamaan `ADR-XXXX-*.md` di folder `docs/id/adr/`.
- **ADR Deprecated**: Catatan sejarah yang telah digantikan disimpan di folder `docs/archive/`.

### 2. Menemukan Usulan Fitur (RFC)
- **Log Utama**: [docs/id/rfc/README.md](../../docs/id/rfc/README.md)
- **Berkas Detil**: Disimpan di folder `docs/id/rfc/` dengan format `rfc-XXXX-*.md`.

### 3. Menemukan Berkas Pengujian (Tests)
- **Pengujian Unit Subsistem**: Disimpan di folder `tests/` utama atau di sub-folder `tests/` di bawah masing-masing subsistem (contoh: `core/kernel/sys_platform/tests/`).
- **Snapshot Compatibility**: Berkas tanda tangan API disimpan di folder `tests/snapshot/`.

### 4. Menemukan Kontrak Publik (Contracts)
- Seluruh DTO dan protokol abstrak disimpan di folder **`core/contracts/src/aether_contracts/`** (tersegmentasi menjadi base, common, event, identity, workspace, storage, repository, artifact).

### 5. Menemukan Spesifikasi Daur Hidup & API Runtime
- Spesifikasi detail per subsistem dapat ditemukan di folder **`docs/id/runtime/`** (misal: `kernel.md`, `storage.md`, `workspace.md`, `organization.md`).

---

## 🚦 Kebijakan Penemuan (Discovery Policy)

Setiap kali melakukan modifikasi fitur:
1. **Pindai Indeks ADR** untuk melihat apakah ada keputusan yang mengikat modul tersebut.
2. **Pindai Berkas Tes Terkait** untuk melihat bagaimana modul dipanggil dan diuji sebelumnya.
3. **Pindai Kontrak Domain** di `core/contracts/` untuk melihat struktur data yang diperbolehkan.
