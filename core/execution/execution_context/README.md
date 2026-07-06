# Execution Context

## Purpose
Context immutable yang diberikan kepada Executor saat eksekusi.

## Responsibilities
- Membawa informasi korelasi (correlation_id, trace_id).
- Membawa metadata dan konfigurasi eksekusi.
- Membawa cancellation token.

## Extension Points
- Tambahkan field metadata untuk kebutuhan custom executor.
