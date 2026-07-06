# AI Delivery Protocol

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Protokol ini mendefinisikan langkah operasional penyerahan hasil kerja (*Delivery*) bagi model AI kepada Chief Architect.

---

## 🚦 Urutan Delivery (Delivery Sequence)

AI wajib mengeksekusi sekuens penyerahan berikut secara ketat:

### 1. Pemuatan Delivery Contract
- Muat templat `contracts/delivery_contract.md`.
- Isi seluruh metadata pekerjaan, hasil pengetesan, dan daftar berkas yang diubah.

### 2. Penghasilan Completion Manifest
- Simpan dokumen tersebut dengan nama `COMPLETION_MANIFEST.md` di folder output obrolan atau di root `.ai/` (jika pengerjaan berupa revisi repositori jangka panjang).

### 3. Eksekusi Post-Delivery Self Audit
- Lakukan pengujian mandiri kognitif akhir dengan menjawab 6 pertanyaan wajib di [execution.md](execution.md).

### 4. Raw Output Delivery
- Sajikan jawaban akhir berupa kode mentah bebas komentar secara terstruktur ke Chief Architect.
