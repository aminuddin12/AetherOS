# Authoritative Terminology Reference

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Daftar istilah baku ini mendefinisikan secara kaku dan unik makna setiap konsep arsitektur penting di dalam ekosistem AetherOS.

---

## 📖 Leksikon Baku AetherOS (Ecosystem Glossary)

| Istilah | Definisi Baku Terikat |
|---|---|
| **Kernel** | Layanan sistem operasi dasar (*system services*): DI, registry, dispatcher, supervisor, dan diagnostics. |
| **Runtime Platform** | Komponen Kernel (`sys_platform/`) yang mengelola bootstrap, deskriptor, relasi graph dependensi, dan resolusi kapabilitas runtime subsistem. |
| **Workspace** | Batas operasional pengerjaan proyek tunggal (*Aggregate Root boundary*) yang membawahi status file, repositori, dan otorisasi lokal. |
| **Storage** | Layanan CAS (Content-Addressable Storage) untuk manajemen data biner fisik (*Blob/Stream*). |
| **Repository** | Layanan pelacakan riwayat versi berkas berbasis graf komit (*Revision Graph*). |
| **Artifact** | Node pengetahuan semantik (*Semantic Resource*) yang memberikan metadata tipe, klasifikasi, silsilah lineage, dan proyeksi terhadap berkas. |
| **Organization** | Operating Context tertinggi yang membawahi struktur perusahaan, keanggotaan manusia & AI (Directory), RBAC, dan kepatuhan audit trail. |
| **Runtime** | Abstraksi modul subsistem yang dideklarasikan sebagai unit plug-in (Storage Runtime, Workspace Runtime, dll). |
| **Capability** | Kemampuan terstruktur (`CapabilityDescriptor`) yang dideklarasikan subsistem penyedia (`Provides`) untuk dikonsumsi subsistem peminta (`Requires`). |
| **Registry** | Wadah pencatatan metadata murni (bukan instans objek) di tingkat Kernel. |
| **Descriptor** | Dokumen metadata statis immutable (dihasilkan dari berkas `manifest.yaml` subsistem). |
| **Composition** | Proses perakitan beberapa runtime subsistem menjadi kelompok stack operasional. |
| **Stack** | Hasil akhir perakitan komposisi runtime (contoh: Workspace Stack). |
| **Bootstrap** | Sekuens langkah booting inisialisasi awal platform dan subsistem terdaftar. |
| **Lifecycle** | Status daur hidup aktif operasional runtime subsistem. |
| **Health** | Status kesehatan operasional runtime subsistem (`HEALTHY`, `DEGRADED`, `FAILED`), terpisah dari Lifecycle. |
| **Context** | Objek pembungkus dependensi sistem terpadu (`RuntimeContext`). |
| **SDK** | Fasad universal panggilan sistem call terpusat (`AetherRuntime`). |
