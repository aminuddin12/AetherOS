# 📚 AetherOS Documentation Hub

Selamat datang di Dokumentasi Resmi **AetherOS (Open Agent Operating System)**.

AetherOS adalah sistem operasi agen terbuka berskala penuh yang dirancang secara terstruktur dan modular menggunakan pendekatan *Domain-Driven Design* (DDD) dan *Clean Architecture*.

---

## 🗂️ Struktur Navigasi Dokumentasi

Dokumentasi ini diorganisasikan ke dalam beberapa lapis ketergantungan penjelasan:

### 1. 🏗️ Landasan Arsitektur
- **[AetherOS System Architecture Book](architecture/book.md)**: Referensi teknis tertinggi yang menjelaskan filosofi "Build Organizations, not Agents", arah dependensi vertikal, ownership matrix, dan universal resource model.
- **[Architecture Decision Records (ADR) Log](adr/README.md)**: Log kronologis keputusan arsitektur (ADR-0001 s/d ADR-0027).
- **[Request for Comments (RFC) Log](rfc/README.md)**: Usulan dan rancangan fitur baru (RFC-0001, RFC-0011, RFC-0012).

---

### 2. 🔌 Panduan Subsistem (Runtime Specs)
Penjelasan rinci untuk masing-masing subsistem modular dalam OS:
- **[Kernel Subsystem](runtime/kernel.md)**: Layanan sistem operasi dasar, metrik, telemetri, dan logging.
- **[Execution Engine Subsystem](runtime/execution.md)**: Universal runtime eksekusi, sandboxing, retry, timeout, dan cancellation.
- **[Runtime SDK Subsystem](runtime/runtime-sdk.md)**: Fasad universal (System Call Interface) untuk interaksi luar.
- **[Workspace Subsystem](runtime/workspace.md)**: Batas isolasi pengerjaan proyek (Aggregate Root), CQRS, bus, dan diagnostics.
- **[Storage Subsystem](runtime/storage.md)**: Content-Addressable Storage (CAS) untuk berkas/blob fisik.
- **[Repository Subsystem](runtime/repository.md)**: Version control dan pengelolaan graf revisi kode.
- **[Artifact Subsystem](runtime/artifact.md)**: Metadata dokumen semantik dan pelacakan silsilah (Lineage).
- **[Organization Subsystem](runtime/organization.md)**: Operating Context global, direktori keanggotaan manusia/AI, RBAC, dan audit trail.

---

### 3. 🚦 Memulai Pengembangan (Onboarding)
- **[AI Governance System](../../.ai/GOVERNANCE.md)**: Protokol operasi wajib untuk model AI yang berkontribusi pada repositori.
- **[Runtime Package Checklist](getting-started/checklist.md)**: Kriteria kelayakan mutu (quality standard) untuk pembuatan paket runtime baru.
- **[Developer Onboarding Guide](getting-started/quickstart.md)**: Panduan instalasi lokal dan instruksi eksekusi.
- **[Glosarium Istilah](glossary/index.md)**: Kamus istilah teknis baku dalam ekosistem AetherOS.
- **[Roadmap Evolusi](roadmap/development-phases.md)**: Detail fase pengerjaan proyek dari infrastruktur dasar hingga Studio UI.

---

## 🏛️ Konvensi Kualitas Dokumentasi
Setiap dokumen spesifikasi di dalam repositori ini wajib mematuhi aturan metadata dan struktur baku:
- **What**: Penjelasan fungsionalitas subsistem.
- **Why**: Justifikasi keberadaan komponen.
- **Responsibilities vs Non-responsibilities**: Batasan tugas yang jelas.
- **Dependencies**: Modul mana saja yang diimpor (tidak boleh melanggar ADR-0025).
- **Public API**: Fasad method yang diekspos ke SDK.
