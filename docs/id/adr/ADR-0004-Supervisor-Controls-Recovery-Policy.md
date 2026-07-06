# ADR-0004: Supervisor Controls Recovery Policy

## Status
Accepted

## Context
Dispatcher is pure Pub/Sub. Supervisor dictates retry/dead-letter policy.

## Decision
(Keputusan implementasi spesifik terkait 0012-supervisor-controls-recovery-policy.md)

## Consequences
- Keuntungan: Mematuhi filosofi OS, loose coupling, highly testable.
- Kerugian: Kompleksitas awal dalam setup boilerplate.
