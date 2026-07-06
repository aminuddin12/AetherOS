# ADR-0010: Execution Session Unit of Work

## Status
Accepted

## Context
Setiap eksekusi perlu dibungkus dalam wrapper yang melacak timing, parent/child relationships, dan status. Ini penting untuk tracing, billing, dan debugging.

## Decision
`ExecutionSession` menjadi Unit of Work wrapper. Setiap submit task membuat session baru. Sessions dapat di-nest (parent → child) untuk sub-task execution.

## Consequences
- **Keuntungan**: Full observability. Mudah untuk menghitung biaya, durasi, dan dependency tree.
- **Kerugian**: Overhead pembuatan session untuk setiap eksekusi (dianggap negligible).
