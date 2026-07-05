# Plugin Contracts

Package ini mendefinisikan ekstensi pihak ketiga (Plugin, Workflow, Agent Pack) tanpa *vendor lock-in*.

## Aturan
- **Wajib Ada:** Extension, ExtensionManifest, Plugin.
- **Tidak Boleh Ada:** OS/File parsing implementation (seperti importlib atau Yapsy).
- **Dependensi yang Diizinkan:** `base`.
