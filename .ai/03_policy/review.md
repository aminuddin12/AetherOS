# Review Policy & Architecture Drift

---
Status: Implemented
Version: 1.0.0
Owner: Core Platform Team
Last Updated: 2026-07-07
---

Kebijakan ini menetapkan mekanisme audit arsitektural untuk mendeteksi penyimpangan arsitektur (*Architecture Drift*) pada setiap perubahan repositori.

---

## 1. Aturan Deteksi Pergeseran (Drift Detection Rules)

Model AI atau peninjau kode wajib memeriksa 4 jenis penyimpangan berikut secara otomatis:

### 1.1. Drift Arah Dependensi
- **Pemicu**: Modul mengimpor modul horizontal selevel secara konkret atau top-down melintasi tingkatan layer.
- **Sanksi**: Pengerjaan langsung dibatalkan secara mutlak (LEVEL 4 - Stop).

### 1.2. Drift Kemurnian Kernel
- **Pemicu**: Kernel (`core/kernel/`) memanggil atau mengandalkan runtime di bawah workspace, storage, atau organization.
- **Sanksi**: Blokir merge segera.

### 1.3. Drift Keselarasan ADR/RFC
- **Pemicu**: Modifikasi kode menyimpang dari keputusan tertulis yang terbekukan dalam berkas ADR/RFC yang aktif.
- **Sanksi**: AI wajib merevisi kode atau menghentikan implementasi untuk meminta ADR/RFC baru (LEVEL 3).

### 1.4. Drift Konsistensi Dokumen
- **Pemicu**: Implementasi kode berubah tanpa diikuti pembaruan berkas spesifikasi subsistem (`docs/id/runtime/`).
- **Sanksi**: Status penyelesaian ditolak (DoC failed).

---

## 2. Kriteria Kelulusan Tinjauan (Review Approval Matrix)

- Perubahan structural/arsitektural wajib mendapatkan persetujuan dari peran **Architecture Reviewer** dan **Quality Auditor** sebelum merge.
- Perubahan behavior/fungsional murni memerlukan peninjauan oleh **Testing Engineer**.
