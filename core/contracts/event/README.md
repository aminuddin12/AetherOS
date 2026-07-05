# Event Contracts

Package ini mendefinisikan struktur data komunikasi (CQRS + Messaging) yang mengalir melalui Event Bus di dalam AetherOS.

## Aturan
- **Wajib Ada:** Abstract Command, Query, Response, Notification, Message, Conversation, Event.
- **Tidak Boleh Ada:** Kafka, Redis, RabbitMQ implementation.
- **Dependensi yang Diizinkan:** `base`, `common`.
