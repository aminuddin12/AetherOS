---
Status: Deprecated
Reason: Legacy architecture based on multi-agent chatbot framework (Redis, PostgreSQL, Qdrant, FastAPI, LangGraph, PydanticAI) has been replaced by the modular Operating System model (Kernel, Execution Engine, Runtime SDK, Workspace, Storage, Repository, Artifact, Organization).
Superseded By: ADR-0011 through ADR-0027, docs/id/architecture/book.md
Replacement: docs/id/architecture/book.md
---

# Organizational Intelligence

AetherOS dirancang untuk menjadi **organisasi yang bisa belajar**. Sistem ini tidak sekadar mengingat riwayat obrolan masa lalu, tetapi mengekstrak **kecerdasan struktural** dari interaksi sehari-hari untuk memodifikasi perilakunya di masa depan. Konsep ini dinamakan **Organizational Intelligence**.

## 1. Dari Project Brain ke Company Brain

Pengetahuan tidak lagi dikurung dalam batasan satu proyek. **Company Brain** berada di level teratas hirarki, memayungi seluruh proyek dalam organisasi. 

```
Company Brain
├── Organizational Intelligence
├── Company DNA
├── Company Constitution
├── Global Knowledge
├── Lessons Learned
├── Shared Skills
└── Project Brains
    ├── Proyek ERP (Workspace A)
    ├── Proyek CRM (Workspace B)
    └── Proyek Web (Workspace C)
```

## 2. Tingkatan Memori dalam Company Brain

Untuk merealisasikan AI Organization, memori dipecah menjadi beberapa bagian spesifik dengan fungsionalitas berbeda:

### 2.1 Knowledge (Pengetahuan Fakta)
Fakta-fakta teknis dan spesifikasi sistem.
- *Contoh:* "Modul Auth di Proyek ERP menggunakan JWT."

### 2.2 Lessons Learned (Pelajaran)
Kesalahan masa lalu dan cara memperbaikinya.
- *Contoh:* "Library X menyebabkan *memory leak* jika tidak ditutup koneksinya. Gunakan *context manager*."

### 2.3 Patterns (Pola Kode & Arsitektur)
Ekstraksi pola yang berhasil dari kode sebelumnya agar dapat direplikasi.
- *Contoh:* "Semua Controller di organisasi ini menggunakan pola CQRS."

### 2.4 Policies & Standards (Kebijakan)
Aturan tidak tertulis atau tertulis organisasi.
- *Contoh:* "Deployment ke production dilarang dilakukan pada hari Jumat."

### 2.5 Predictions & Recommendations
Proyeksi berdasarkan metrik historis.
- *Contoh:* "Pekerjaan ini diperkirakan akan selesai dalam 30 interaksi berdasarkan metrik proyek sebelumnya."

### 2.6 Company DNA
Bawaan budaya perusahaan, gaya bahasa, filosofi pengembangan, dan prinsip-prinsip utama.
- *Contoh:* "Kami menghargai kode yang mudah dibaca daripada kode yang terlalu cerdik (clever) namun sulit dikelola."

## 3. Siklus Pembelajaran Otonom (Self-Evolution)

Pembeda utama AetherOS dari framework seperti AutoGPT atau OpenHands adalah kemampuannya untuk mendeteksi *pattern of failure* (pola kegagalan) dan mengadaptasi proses bisnis organisasi secara otomatis.

**Skenario: Organisasi yang Belajar**

1. **Kejadian Berulang:** Setelah berjalan 6 bulan, agen QA sering me-reject *pull request* dari Agen Backend.
2. **Analisis Akar Masalah (Root Cause):** Kernel AI dan Manager Agent melakukan analitik dari database PostgreSQL. Ditemukan bahwa 80% penolakan terjadi karena Agen Backend lupa membuat *unit test* untuk endpoint baru.
3. **Pembelajaran (Lessons Learned):** Sistem mendaftarkan "Backend sering melupakan testing" ke dalam *Company Brain*.
4. **Adaptasi Kebijakan (Policy Update):** Manager Agent, secara otonom (dengan persetujuan Manusia/HITL), memodifikasi `project.yaml` (Konstitusi Proyek).
5. **Eksekusi Baru:** Di tiket selanjutnya, Manager Agent *secara otomatis menyisipkan* **Testing Checklist** ke dalam instruksi agen Backend sebelum pekerjaan dimulai.
6. **Hasil:** Tingkat *rejection* dari QA turun secara dramatis. Organisasi AI telah berevolusi secara organik.

## 4. Keuntungan Jangka Panjang

Dengan *Organizational Intelligence*, nilai tambah perusahaan tidak terletak pada prompt yang mereka berikan ke agen, melainkan pada **seberapa besar dan matang Company Brain** yang telah mereka bangun selama bertahun-tahun beroperasi.

Sama seperti mempekerjakan tim veteran yang sudah mengetahui luar dalam budaya dan sistem perusahaan, agen yang *di-deploy* ke dalam AetherOS setelah 5 tahun perusahaan berjalan akan jauh lebih pintar dari agen yang baru di-deploy di hari pertama.

---

🔗 **Selanjutnya:** [Arsitektur Multi-Workspace →](multi-workspace.md)
