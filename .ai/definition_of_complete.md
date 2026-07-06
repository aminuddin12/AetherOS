# Definition of Complete (DoC)

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Pekerjaan pengembangan atau perubahan repositori dinyatakan **Selesai Secara Sempurna (Complete)** jika dan hanya jika seluruh kriteria di bawah ini terpenuhi secara penuh:

---

## 📋 Kriteria Kelayakan Utama (Core Completion Criteria)

1. **Semua Sasaran Terpenuhi**: Kebutuhan fungsional dan teknis yang dijabarkan dalam *Task Contract* terpenuhi 100%.
2. **Tidak Melanggar Invariants**: Desain kode patuh terhadap seluruh aturan abadi arsitektur AetherOS di [invariants.md](01_constitution/invariants.md).
3. **Kontrak Tetap Valid**: Seluruh kontrak domain di `core/contracts/` yang terpengaruh tidak mengalami modifikasi sepihak (tanpa ADR) dan skema data tetap konsisten.
4. **Dokumentasi Diperbarui**: Berkas spesifikasi runtime di `docs/id/runtime/` dan hub dokumentasi disinkronkan dengan status implementasi aktual.
5. **Pengetesan Lulus**: Unit test dan integration test baru telah dibuat dan seluruh test suite lulus 100% menggunakan `pytest` secara offline dan in-memory.
6. **Tidak Ada Penyimpangan (No Drift)**: Pemeriksaan arsitektur pada [review.md](03_policy/review.md) menyatakan kelulusan tanpa peringatan deviasi.
7. **Tidak Ada Scope Creep**: AI tetap fokus pada cakupan *Goals* dan mematuhi batasan *Non-Goals* dari *Task Contract*.
8. **Completion Manifest Dihasilkan**: Berkas [delivery_contract.md](contracts/delivery_contract.md) berhasil diisi dan diubah menjadi `COMPLETION_MANIFEST.md` kognitif untuk serah terima sesi.

---

## 🚦 Penegakan Kriteria

Jika salah satu kriteria di atas bernilai negatif atau belum selesai, AI dilarang mengirimkan hasil pengerjaan sebagai status `COMPLETED`. AI wajib kembali ke status `IMPLEMENTING` atau `TESTING` untuk menyelesaikan kekurangan tersebut, atau melapor dengan eskalasi LEVEL 3/4.
