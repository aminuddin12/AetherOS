# Developer Onboarding & Quickstart Guide

---
Status: Implemented
Version: 1.0.0
Owner: Core Platform Team
Last Updated: 2026-07-07
Depends On: docs/id/README.md
Required Reading: docs/id/getting-started/checklist.md
Related ADR: ADR-0021, ADR-0027
Related RFC: None
Implementation Status: Ready for Local Development
---

## 1. Persiapan Lingkungan (Prerequisites)

Untuk mengembangkan atau berkontribusi pada AetherOS, pastikan sistem lokal Anda memenuhi syarat berikut:
- **Python 3.12+**
- **uv** (Python Package Manager super cepat, menggantikan pip/poetry). Instalasi: `curl -LsSf https://astral.sh/uv/install.sh | sh`

---

## 2. Setup Awal Proyek

Jalankan perintah berikut untuk mengkloning dan mensinkronisasikan seluruh workspace:

```bash
git clone https://github.com/aminuddin12/AetherOS.git
cd AetherOS
uv sync
```

Perintah `uv sync` secara otomatis akan:
1. Membuat virtual environment lokal `.venv`.
2. Mengunduh dan memasang semua dependensi multi-package (workspace members).
3. Melakukan instalasi dalam mode *editable* sehingga modifikasi kode langsung terbaca secara real-time.

---

## 3. Menjalankan Test Suite

AetherOS menerapkan prinsip *test-driven development* yang agresif. Anda dapat memverifikasi integritas seluruh sub-sistem dengan satu komando:

```bash
PYTHONPATH=organization/src:workspace-app/src:artifact/src:repository/src:storage/src:workspace/src:runtime/src uv run pytest
```

---

## 4. Alur Pembuatan Fitur Baru

Jika Anda ingin membuat subsistem atau fitur baru:
1. Bacalah **[Architecture Decision Records](adr/README.md)** untuk memastikan arah desain Anda selaras.
2. Buat sub-folder baru di root directory, inisialisasi `pyproject.toml`, dan daftarkan ke dalam `workspace.members` di `pyproject.toml` utama proyek.
3. Patuhi aturan pembagian wewenang data **[Ownership Matrix](../architecture/matrix.md)**.
4. Pastikan subsistem baru Anda mengimplementasikan fasad dan didaftarkan di **Composition Root** (`runtime/src/aether_runtime/sdk.py`).
5. Isi seluruh checklist kesiapan API di **[Runtime Package Checklist](checklist.md)** sebelum meminta *API Freeze review* ke Chief Architect.
