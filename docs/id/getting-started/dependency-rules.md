# Dependency Rules

---
Status: Implemented
Version: 2.0.0
Owner: Core Platform Team
Last Updated: 2026-07-07
Required Reading: docs/id/getting-started/coding-standard.md
Related ADR: ADR-0025
---

## Aturan Dependensi Vertikal (ADR-0025)

Untuk mencegah terbentuknya kode kusut (*spaghetti code*) dan ketergantungan melingkar (*circular dependencies*), aliran impor modul diatur secara vertikal dari bawah ke atas (*bottom-up*).

### 1. Level 0: Kernel & Execution Engine
- Hanya diperbolehkan bergantung pada `core/contracts/` dan pustaka standar Python.
- Dilarang keras mengimpor subsistem tingkat atas (Storage, Repository, Workspace, Organization, Brain).

### 2. Level 1: Sub-sistem Domain (Workspace, Storage, Repository, Artifact)
- Diperbolehkan bergantung pada `core/contracts/` dan fasad yang disediakan oleh **Runtime SDK**.
- Dilarang mengimpor implementasi konkret lintas subsistem. Hubungan lintas domain dikomunikasikan secara asinkron menggunakan abstraksi **ResourceURI**.

### 3. Level 2: Workspace Application Layer
- Berfungsi sebagai orkestrator use-case (CQRS Command/Query Handlers).
- Diperbolehkan mengimpor kontrak dan antarmuka subsistem di bawahnya (Level 1 & Level 0).
- Dilarang menyimpan *state* bisnis internal secara mandiri.

### 4. Level 3: Organization Runtime (Operating Context)
- Diperbolehkan memuat referensi dari Workspace dan subsistem bawahan murni melalui Runtime SDK.
- Dilarang mengimpor implementasi internal Workspace Core.

---

## Validasi Otomatis
Integritas aturan impor divalidasi pada setiap pull request menggunakan alat bantu linting. Pelanggaran impor horizontal akan secara otomatis menggagalkan status peninjauan (*Build Blocked*).
