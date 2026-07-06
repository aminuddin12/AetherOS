# Repository Memory

---
Status: Implemented
Version: 1.0.0
Owner: Core Platform Team
Last Updated: 2026-07-07
---

Dokumen memori ini mencatat rangkuman status perkembangan repositori, keputusan tertunda, risiko arsitektur, dan hutang teknis aktif agar pengerjaan antar sesi AI tetap sinambung.

---

## 1. Status Milestone & Batas Pembekuan (Milestone Memory)

- **Completed Milestone**: M3.7 (Runtime Platform & Bootstrap Engine) selesai dibangun di `sys_platform/`.
- **Active Focus**: M4.0 (Company Brain) - Fase pemetaan spesifikasi dan pembuatan draf arsitektur kognitif.
- **Architecture Freeze Status**: Seluruh modul dari Level 0 hingga Level 3 berstatus **FROZEN** (tidak boleh dimodifikasi tanpa ADR).

---

## 2. Hutang Teknis & Risiko Arsitektur (Known Technical Debt & Risks)

- **Standard Library Name Collision**: Namespace `platform` sebelumnya bertabrakan dengan pustaka bawaan Python, sehingga berhasil direfaktorkan secara permanen ke `sys_platform`. Jangan pernah menggunakan nama `platform` sebagai folder modul tingkat kernel lagi.
- **Mock-in-Memory Testing**: Beberapa unit test lama masih berisiko memanggil filesystem eksternal secara aktif. Pastikan adapter in-memory murni digunakan untuk setiap penambahan kode subsistem baru.

---

## 3. Keputusan & Desain Tertunda (Pending Decisions)
- Spesifikasi final interaksi graf semantik lintas-workspace untuk Company Brain (M4) masih dalam status draf di `docs/id/architecture/drafts/company-brain-spec.md`.
