# SPI (Service Provider Interface)

## Purpose
Mendefinisikan semua interface yang boleh diimplementasikan oleh pihak ketiga (plugin, distribution, custom executor).

## Responsibilities
- Menyediakan kontrak Executor universal.
- Menyediakan kontrak Strategy, Policy, dan Middleware.

## Public API
Semua class di package ini adalah public.

## Dependencies
- `core/contracts/base`

## Forbidden Dependencies
- Implementasi konkret apapun

## Extension Points
- Implementasikan `Executor` untuk jenis runtime baru.
- Implementasikan `ExecutionStrategy` untuk pola eksekusi baru.
- Implementasikan `RetryPolicy` / `TimeoutPolicy` untuk kebijakan kustom.
- Implementasikan `ExecutionMiddleware` untuk pipeline hook.
