# Organization Runtime

## Purpose
Menyediakan fungsionalitas inti untuk domain Organization.

## Responsibilities
- Mengelola state spesifik untuk Organization.
- Menyediakan interface publik (Fasad) untuk interaksi eksternal.

## Public API
- `runtime.organization.*`

## Dependencies
- Mengikuti ADR-0025 (Bottom-up).

## Events
- Menerbitkan domain events saat terjadi perubahan status signifikan.

## Lifecycle
- Diinisiasi melalui Dependency Registry / Composition Root.

## Future Extension
- Siap diintegrasikan dengan Intelligence Layer (Company Brain).
