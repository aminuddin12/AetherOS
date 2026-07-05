# Tool Contracts

Package ini membedakan antara spesifikasi statis (Tool), aksi eksekusi aktual (Action), dan makro tingkat lanjut (Skill).

## Aturan
- **Wajib Ada:** Tool, Action, Skill.
- **Tidak Boleh Ada:** Script bash, python subprocess, implementasi tool konkrit (GithubTool).
- **Dependensi yang Diizinkan:** `base`.
