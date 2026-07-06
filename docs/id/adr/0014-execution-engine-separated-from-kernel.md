# ADR-0014: Execution Engine Separated from Kernel

## Status
Accepted

## Context
Kernel Pipeline (`core/kernel/pipeline/`) berfungsi sebagai *system-level orchestrator* (routing, permission, scheduling). Namun kebutuhan eksekusi yang melibatkan retry, timeout, cancellation, executor pool, dan strategy membutuhkan lapisan tersendiri agar Kernel tetap kecil dan stabil.

## Decision
Execution Engine ditempatkan di `core/execution/` sebagai lapisan terpisah yang bergantung pada Kernel Public API dan Core Contracts, tetapi TIDAK bergantung pada Kernel Internal.

## Consequences
- **Keuntungan**: Kernel tetap stabil (Microkernel Architecture). Execution Engine bisa berkembang tanpa menyentuh Kernel.
- **Kerugian**: Sedikit duplikasi konsep (dua pipeline, dua middleware). Namun ini dianggap acceptable karena beroperasi pada layer berbeda.
