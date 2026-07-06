# Aether Execution Engine

## Purpose
Universal Execution Runtime untuk AetherOS. Menjalankan Task melalui Executor apapun (AI, Docker, Human, SSH, CLI, Browser, MCP) tanpa mengetahui implementasi spesifiknya.

## Responsibilities
- Mengelola lifecycle eksekusi (Session, Context, Plan, Result).
- Menyediakan SPI (Service Provider Interface) untuk Custom Executor.
- Mengorkestrasi middleware pipeline eksekusi.
- Mengelola Executor Pool (alokasi, release).
- Menerapkan Retry, Timeout, dan Cancellation policies.

## Public API
Semua class publik berada di `api/`.

## SPI
Semua interface yang dapat di-override berada di `spi/`.

## Dependencies
- `core/contracts/*` (read-only, API Freeze)
- `core/kernel/` public API only

## Forbidden Dependencies
- `core/kernel/internal/`
- Vendor libraries (openai, redis, sqlalchemy, fastapi, langgraph, openhands)
- Database drivers
- HTTP frameworks
