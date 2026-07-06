# Coding Standard

---
Status: Implemented
Version: 1.0.0
Owner: Core Platform Team
Last Updated: 2026-07-07
Required Reading: docs/id/getting-started/quickstart.md
---

## Aturan Pengkodean Wajib (Coding Rules)

### 1. Absolute Zero Comments (Bebas Komentar)
**SANGAT KETAT**: Dilarang membiarkan, menyisipkan, atau menulis komentar kode bentuk apa pun (`//`, `/* */`, `#`, `"""docstring"""` di dalam fungsi) di dalam file kode sumber yang dimodifikasi atau dibuat. Kode harus sepenuhnya mendokumentasikan dirinya sendiri secara semantik melalui penamaan variabel, fungsi, dan kelas yang representatif (*self-documenting code*).

### 2. Versi Python & Lingkungan
- Wajib menggunakan **Python 3.12+**.
- Pengelolaan paket dan eksekusi lokal wajib memanfaatkan `uv`.

### 3. Strict Type Hinting
- Seluruh fungsi, parameter, dan nilai kembalian wajib dideklarasikan type hint secara eksplisit (lulus verifikasi `mypy` tingkat ketat).

### 4. Pydantic & Immutability
- Gunakan **Pydantic V2** untuk validasi skema input/output.
- Seluruh kelas DTO data bisnis (Contracts) wajib dideklarasikan bersifat immutable (`frozen=True`).

### 5. Pemisahan Interface & Implementasi
- Pisahkan deklarasi kontrak dalam kelas Python `Protocol` dari kode implementasinya.
- Impor internal melintasi sub-sistem dilarang mengimpor kelas konkret, melainkan hanya merujuk ke protokol abstrak.

### 6. Konvensi Penamaan (Naming Conventions)
- Kelas Domain / Kontrak: `PascalCase`
- Fungsi & Variabel: `snake_case`
- Nama Berkas: `snake_case` (menggunakan kebab-case jika diizinkan oleh konvensi framework luar).
