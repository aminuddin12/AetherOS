---
Status: Deprecated
Reason: Legacy architecture based on multi-agent chatbot framework (Redis, PostgreSQL, Qdrant, FastAPI, LangGraph, PydanticAI) has been replaced by the modular Operating System model (Kernel, Execution Engine, Runtime SDK, Workspace, Storage, Repository, Artifact, Organization).
Superseded By: ADR-0011 through ADR-0027, docs/id/architecture/book.md
Replacement: docs/id/architecture/book.md
---

# ADR-0001: Penggunaan LangGraph untuk Orkestrasi State Machine

## Konteks
AetherOS adalah OS multi-agen. Ketika Manager mendelegasikan tugas ke agen-agen spesialis, kita memerlukan kerangka kerja untuk mengelola alur logika kompleks (looping, *fallback*, persetujuan manusia). Mengandalkan *while-loop* statis dalam Python atau *chaining* kaku seperti LangChain standar rentan terhadap *infinite loops* dan kesulitan menyimpan state (memori) secara handal saat terjadi kegagalan (crash).

## Keputusan
Kita menggunakan **LangGraph** sebagai mesin orkestrasi untuk merancang eksekusi *State Machine* (Grafik Status) pada AetherOS Kernel.

## Konsekuensi Positif
- State dapat di-persist (disimpan) dan di-resume dengan mudah.
- *Human-in-the-Loop* (Persetujuan manusia) bersifat *native* (bawaan) melalui fitur `interrupt`.
- Siklus eksekusi agen (ReAct) sangat mudah dipetakan menjadi Graph (Node & Edges).

## Konsekuensi Negatif
- Kurva pembelajaran (learning curve) LangGraph lebih curam bagi pengembang baru (kontributor) dibandingkan script Python biasa.
- Menambah dependensi berat pada ekosistem LangChain.
