# Common Contracts

Package ini mendefinisikan struktur data esensial yang dibagikan secara global ke seluruh sistem (lintas-domain), seperti Trace dan Context.

## Aturan
- **Wajib Ada:** Struktur data umum non-domain khusus (seperti Tracer, Context penyerta eksekusi).
- **Tidak Boleh Ada:** Configuration (karena konfig adalah runtime detail), business models (seperti Workspace atau Agen).
- **Dependensi yang Diizinkan:** `base`, `identity`.
