# ADR-0015: Executor as Universal SPI

## Status
Accepted

## Context
AetherOS harus mampu menjalankan task melalui berbagai macam runtime: AI Agent, Docker Container, SSH Command, Human Task, Browser Automation, MCP, CLI. Dibutuhkan satu interface universal agar Execution Engine tidak mengetahui detail implementasi.

## Decision
Dibuat interface `Executor` (ABC) di `core/execution/spi/executor.py` dengan method: `execute`, `validate`, `cancel`, `shutdown`, `health`, `capabilities`. Semua jenis executor mengimplementasikan SPI ini.

## Consequences
- **Keuntungan**: True provider/executor agnosticism. Plugin cukup mengimplementasikan satu interface.
- **Kerugian**: Executor yang sangat sederhana (misal: shell script) tetap harus mengimplementasikan semua method.
