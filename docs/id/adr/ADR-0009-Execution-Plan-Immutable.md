# ADR-0009: Execution Plan Immutable

## Status
Accepted

## Context
ExecutionPlan adalah hasil dari Scheduler. Jika plan bisa dimutasi setelah dibuat, maka audit trail dan replay menjadi tidak reliable. 

## Decision
`ExecutionPlan` menggunakan Pydantic `frozen=True`. Setelah dibuat, ia tidak bisa dimodifikasi. Jika strategi berubah, plan baru harus dibuat.

## Consequences
- **Keuntungan**: Deterministic replay, mudah untuk event sourcing, audit trail terjamin.
- **Kerugian**: Perubahan minor memerlukan pembuatan plan baru (biaya alokasi memori kecil).
