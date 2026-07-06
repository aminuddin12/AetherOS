# Kernel Specification

---
Status: Implemented
Version: 1.0.0
Owner: Core Platform Team
Last Updated: 2026-07-07
Depends On: docs/id/specifications/contracts.md
Required Reading: docs/id/runtime/kernel.md
Related ADR: ADR-0005
Related RFC: None
---

## 1. Konsep Microkernel AetherOS
Kernel AetherOS dirancang mengikuti prinsip *Microkernel*. Tugas utamanya dibatasi hanya untuk mengoordinasikan *Dependency Injection* (DI), pemantauan sub-sistem (*Supervisor*), pendistribusian event internal (*Dispatcher*), dan koleksi telemetri metrik sistem.

## 2. Dependency Injection & Service Registry
Registry internal di `core/kernel/registry/` mendaftarkan seluruh sub-sistem runtime yang aktif. 
- Komponen di luar kernel tidak diperbolehkan mengakses registry internal ini secara langsung.
- Pendaftaran sub-sistem didelegasikan ke **Composition Root** melalui bootstrap saat inisiasi sistem call pertama kali.

## 3. Supervisor & Self-Healing
Sub-sistem pengawas (`supervisor`) bertugas memantau status operasional subsistem lain:
- Jika sub-sistem mengalami *crash* atau *degraded*, Supervisor bertugas memulihkan state lokal atau merekam tanda bahaya (*critical alarm*).
- Pemantauan dilakukan secara non-blocking menggunakan async loop.
