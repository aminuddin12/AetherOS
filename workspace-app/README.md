# Workspace Application Runtime

Layer aplikasi orkestrasi use-case (CQRS Command/Query Handlers & Middleware Pipeline) untuk AetherOS.

## Struktur Folder
- `src/aether_workspace_app/application/`: CommandBus, QueryBus, middleware, commands, queries, dan results DTO.
- `src/aether_workspace_app/composition/`: Composition root (bootstrap & registry) untuk DI.
- `src/aether_workspace_app/orchestrator/`: Engine eksekusi pipeline utama.
- `src/aether_workspace_app/inspectors/`: Health, Policy, Diagnostics inspectors.
