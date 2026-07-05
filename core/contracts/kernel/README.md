# Kernel Contracts

Package ini mendefinisikan antarmuka dan kontrak untuk lapisan abstraksi utama AetherOS (AI Kernel).

## Aturan
- **Wajib Ada:** Definisi Protocol untuk Runtime, Dispatcher, Scheduler (Schedule/Policy), Executor, Pipeline, Registry.
- **Tidak Boleh Ada:** Implementasi OpenHands, Redis Streams, LangGraph.
- **Dependensi yang Diizinkan:** `base`, `common`.
