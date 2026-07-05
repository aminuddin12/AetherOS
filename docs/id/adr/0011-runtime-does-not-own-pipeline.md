# ADR: Runtime Does Not Own Pipeline

## Status
Accepted

## Context
Pipeline orchestrates the flow; Runtime is merely an executor middleware.

## Decision
(Keputusan implementasi spesifik terkait 0011-runtime-does-not-own-pipeline.md)

## Consequences
- Keuntungan: Mematuhi filosofi OS, loose coupling, highly testable.
- Kerugian: Kompleksitas awal dalam setup boilerplate.
