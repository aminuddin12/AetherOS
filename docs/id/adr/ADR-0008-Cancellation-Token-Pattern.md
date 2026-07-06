# ADR-0008: Cancellation Token Pattern

## Status
Accepted

## Context
Eksekusi yang berjalan lama (misal: AI Agent loop, Docker build) harus bisa dibatalkan secara *cooperative* tanpa memaksa (kill). Dibutuhkan mekanisme yang memungkinkan executor memeriksa status pembatalan secara periodik.

## Decision
Mengadopsi pola `.NET CancellationToken`. `CancellationTokenSource` mengontrol token, sementara `CancellationToken` (read-only view) diberikan ke executor. Executor bertanggung jawab memeriksa `token.is_cancelled` secara periodik.

## Consequences
- **Keuntungan**: Clean cancellation tanpa resource leak. Bisa di-nest (linked tokens).
- **Kerugian**: Executor yang tidak memeriksa token tidak akan berhenti. Ini adalah tanggung jawab implementor.
