# AetherOS System Architecture Book

Dokumen ini adalah referensi arsitektur tertinggi dari **AetherOS (Open Agent Operating System)**.

## Visi & Filosofi
**"Build Organizations, not Agents."**
AetherOS tidak dibangun untuk merakit agen mandiri, melainkan untuk mensimulasikan lingkungan operasional penuh (Organisasi) tempat para agen dan manusia bekerja sama di bawah naungan aturan (Constitution), direktori identitas (Identity), dan ruang kerja (Workspace).

## Prinsip Desain
1. **Resource Universality**: Seluruh entitas diabstraksikan sebagai *ResourceURI* (contoh: `artifact://...`).
2. **Absolute Decoupling**: Tidak ada *two-way dependency*. Ketergantungan murni mengalir dari bawah ke atas.
3. **No Blob Ownership Violation**: Setiap *runtime* hanya memegang kekuasaan atas datanya sendiri. (Misal, *Repository* tidak menyimpan file, hanya menyimpan graf revisi yang menunjuk ke *Storage URI*).

## Ekosistem Runtime
Sistem terbagi ke dalam tiga layer:
1. **Infrastructure Layer**: Kernel, Execution, Runtime SDK.
2. **Organization Layer**: Workspace, Storage, Repository, Artifact, Workspace App, Organization.
3. **Intelligence Layer**: Company Brain, Agent, Provider, Workflow, Constitution.

## Tata Kehidupan Sistem
Semua runtime dirangkai menggunakan **Composition Root** (Bootstrap) dan disatukan melalui **Runtime SDK Facade**. AetherOS beroperasi murni dengan merutekan pesan abstrak dan tidak mengizinkan pemanggilan fungsi bisnis secara melintang antar-paket selevel.
