# Workspace Runtime

Batas operasional proyek (Aggregate Root) untuk AetherOS.

## Struktur Folder
- `src/aether_workspace/core/`: Domain model Workspace.
- `src/aether_workspace/application/`: Handlers CQRS lokal.
- `src/aether_workspace/bus/`: Message bus lokal per-workspace.
- `src/aether_workspace/capabilities/`: Capability Manager.
- `src/aether_workspace/manifest/`: Parser workspace.yaml.
- `src/aether_workspace/lifecycle/`: State machine daur hidup workspace.
