# Metrics Contracts

Package ini mendefinisikan struktur data untuk mencatat telemetri, metrik, biaya (cost), dan penggunaan (usage) token.

## Aturan
- **Wajib Ada:** Metric, Measurement, Telemetry, Cost, Usage, Token.
- **Tidak Boleh Ada:** Implementasi database time-series (Prometheus), konektor Datadog.
- **Dependensi yang Diizinkan:** `base`.
