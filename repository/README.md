# Repository Runtime

Pengelola revision graph dan commits history untuk AetherOS.

## Struktur Folder
- `src/aether_repository/core/`: Model domain commit, branch, dan revision graph.
- `src/aether_repository/resolver/`: Penyelesaian alias branch/tag ke commit hash.
- `src/aether_repository/uri/`: Router skema URI `repository://`.
- `src/aether_repository/adapters/`: Adapter Git dan In-Memory.
