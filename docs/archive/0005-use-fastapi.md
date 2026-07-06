---
Status: Deprecated
Reason: Legacy architecture based on multi-agent chatbot framework (Redis, PostgreSQL, Qdrant, FastAPI, LangGraph, PydanticAI) has been replaced by the modular Operating System model (Kernel, Execution Engine, Runtime SDK, Workspace, Storage, Repository, Artifact, Organization).
Superseded By: ADR-0011 through ADR-0027, docs/id/architecture/book.md
Replacement: docs/id/architecture/book.md
---

# ADR-0005: Penggunaan FastAPI untuk Gateway & API

## Konteks
Aether Kernel membutuhkan *entrypoint* (titik masuk) bagi aplikasi eksternal, Dashboard UI, dan interaksi CLI (Command Line Interface). Lapisan ini harus mem-parsing *HTTP requests*, mengelola autentikasi, dan mem-validasi *payload* JSON sebelum dilempar ke *Event Dispatcher*.

## Keputusan
Kita menggunakan **FastAPI** sebagai kerangka kerja *Gateway* HTTP utama di Python.

## Konsekuensi Positif
- Berbasis *asyncio*, menjadikannya salah satu kerangka kerja Python tercepat.
- Terintegrasi penuh dengan Pydantic, sehingga validasi tipe data (schema validation) terjadi secara otomatis tanpa kode *boilerplate*.
- Membuat dokumentasi OpenAPI (Swagger) secara otomatis, yang sangat penting bagi "The Open Agent OS" agar sistem pihak ketiga dapat terintegrasi.

## Konsekuensi Negatif
- Menambah lapisan dependensi baru (Uvicorn, Starlette, Pydantic).
