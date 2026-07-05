# Identity Contracts

Package ini mendefinisikan konsep identitas, otentikasi, dan kontrol akses (RBAC) dalam domain AetherOS.

## Aturan
- **Wajib Ada:** Model-model yang merepresentasikan prinsipal (pengguna/agen/sistem), kredensial, otentikasi, dan otorisasi.
- **Tidak Boleh Ada:** Implementasi verifikasi password, integrasi OAuth, JWT decoding logic.
- **Dependensi yang Diizinkan:** `base`.
