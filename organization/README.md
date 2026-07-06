# Organization Runtime

Penyedia Operating Context tingkat tertinggi (Identitas, Keanggotaan, RBAC, Kebijakan, Audit Trail) untuk AetherOS.

## Struktur Folder
- `src/aether_organization/core/`: Context dan Identity perusahaan.
- `src/aether_organization/directory/`: Membership dan RBAC.
- `src/aether_organization/registry/`: WorkspaceRegistry dan ResourceCatalog.
- `src/aether_organization/policies/`: Engine otorisasi kebijakan global.
- `src/aether_organization/audit/`: Audit logger terstruktur.
- `src/aether_organization/config/`: Configuration & Capabilities profiles.
- `src/aether_organization/protocols/`: Protokol persistensi.
- `src/aether_organization/adapters/`: Adapter In-Memory.
