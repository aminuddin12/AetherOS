# Provider Contracts

Package ini mendefinisikan infrastruktur dan abstraksi vendor (seperti penyedia LLM) tanpa *vendor lock-in*.

## Aturan
- **Wajib Ada:** Provider, ProviderCapability, Limits, Pricing, Health.
- **Tidak Boleh Ada:** Import dari `openai`, `anthropic`, HTTP Clients.
- **Dependensi yang Diizinkan:** `base`.
