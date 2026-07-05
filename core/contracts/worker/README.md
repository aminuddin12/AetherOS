# Worker Contracts

Package ini mendefinisikan persona, siklus hidup, dan metrik kinerja (reputasi) dari entitas eksekutor (Agent/Worker) di dalam AetherOS.

## Aturan
- **Wajib Ada:** Abstract Worker, Role, CapabilityProfile, Reputation, Lifecycle.
- **Tidak Boleh Ada:** Logic LangChain/LlamaIndex Agent, class PydanticAI yang runnable.
- **Dependensi yang Diizinkan:** `base`, `identity`, `memory`, `event`.
