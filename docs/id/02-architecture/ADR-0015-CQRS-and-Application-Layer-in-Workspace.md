# ADR-0015: CQRS and Application Layer in Workspace

## Status
Accepted

## Context
Seiring berkembangnya kompleksitas operasi Workspace, penggunaan folder `services/` yang berisi kelas-kelas monolith cenderung berakhir sebagai *God Objects*. Pemisahan antara operasi yang mengubah *state* (Command) dan operasi yang murni membaca *state* (Query) tidak tegas, menyebabkan *technical debt*.

## Decision
Kita mengadopsi pola *Command Query Responsibility Segregation* (CQRS) pada *Application Layer* Workspace.
- Folder `services/` ditiadakan.
- Operasi ditulis dalam `application/commands/` dan `application/queries/`.
- Komponen pendukung lainnya ditempatkan di `application/builders/`, `loaders/`, dan `inspectors/`.

## Consequences
- **Keuntungan**: Keterpisahan *concern* yang sangat jelas. Command dapat dibungkus dengan *Event Emission* secara lebih terstruktur. Queries dapat dioptimasi independen.
- **Kerugian**: Jumlah file dan boiler-plate meningkat tajam untuk operasi-operasi yang sangat sederhana.
