# ADR-0014: Workspace Manifest & Descriptor Separation

## Status
Accepted

## Context
Konfigurasi dari sebuah entitas sistem sering dicampur aduk antara *Metadata Identitas* (ID, nama, pembuat) dan *Kebijakan/Perilaku* (Hak akses, fitur yang dinyalakan, batasan resources). Menyatukan keduanya menyulitkan query tingkat organisasi. Misalnya, kita ingin tahu "daftar ID semua Workspace" tanpa perlu mem-*parsing* aturan keamanan yang rumit.

## Decision
Kita membagi informasi deklaratif Workspace menjadi dua model *Domain Contract* murni:
1. **WorkspaceDescriptor**: Berfokus eksklusif pada identitas (ID, Name, Description, Owner, Version, Created).
2. **WorkspaceManifest**: Berfokus eksklusif pada konfigurasi operasional (*Policies*, *Capabilities*, *Extensions*, *Permissions*).

Keduanya adalah Domain Contract (Pydantic models) dan tidak terikat pada format YAML atau JSON. Format file hanyalah urusan *Serializer/Deserializer*.

## Consequences
- **Keuntungan**: Query metadata tingkat organisasi menjadi sangat ringan karena hanya perlu membaca `Descriptor`.
- **Kerugian**: Membutuhkan sinkronisasi antara perubahan Descriptor dan Manifest saat melakukan *commit* atau perubahan skala besar.
