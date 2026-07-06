---
Status: Deprecated
Reason: Legacy architecture based on multi-agent chatbot framework (Redis, PostgreSQL, Qdrant, FastAPI, LangGraph, PydanticAI) has been replaced by the modular Operating System model (Kernel, Execution Engine, Runtime SDK, Workspace, Storage, Repository, Artifact, Organization).
Superseded By: ADR-0011 through ADR-0027, docs/id/architecture/book.md
Replacement: docs/id/architecture/book.md
---

# ADR-0008: Penggunaan OpenHands untuk Tool Execution Sandbox

## Konteks
"The Open Agent OS" memiliki fitur untuk mengedit *file* dan menjalankan *command line* bash (terutama untuk agen tipe Software Engineering atau Cyber Security). Menjalankan kode yang dihasilkan LLM langsung di lingkungan Kernel atau mesin *host* sangat berbahaya (*Remote Code Execution*).

## Keputusan
Kita menggunakan dan mengintegrasikan (atau mem-fork/menggunakan abstraksi) ekosistem **OpenHands** (sebelumnya OpenDevin) sebagai kotak pasir (Sandbox) eksekusi *Tool*.

## Konsekuensi Positif
- Keamanan terjamin karena perintah dieksekusi dalam *Docker Container* yang terisolasi.
- OpenHands sudah memecahkan tantangan menjalankan aksi terminal yang gigih (*stateful shell*).
- Ekosistem besar; jika komunitas OpenHands membuat alat perbaikan *bug*, AetherOS otomatis bisa memanfaatkannya.

## Konsekuensi Negatif
- Arsitektur sangat berat (membutuhkan integrasi intensif dengan Docker Daemon di mesin *host*).
- Kurang cocok untuk dijalankan di lingkungan *serverless* penuh tanpa virtualisasi yang diizinkan.
