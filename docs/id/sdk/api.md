# Public API Register

Dokumen ini merekam status stabilitas (Stability Status) seluruh rute fasad yang diekspos melalui **Runtime SDK** (`AetherRuntime`).

## Status Definitions
- **[Stable]**: Kontrak publik telah dibekukan (API Freeze). Perubahan *breaking* dilarang.
- **[Experimental]**: Kontrak sedang diuji atau didefinisikan. Perubahan dapat terjadi tanpa peringatan.
- **[Internal]**: Rute khusus untuk komunikasi antar subsistem OS. Aplikasi dilarang memanggil secara langsung.

## Fasad Registry (`runtime.*`)

### `runtime.kernel`
- `runtime.kernel.metrics.record()` — **[Stable]**
- `runtime.kernel.telemetry.trace()` — **[Stable]**

### `runtime.execution`
- `runtime.execution.run_sync()` — **[Stable]**
- `runtime.execution.spawn()` — **[Stable]**

### `runtime.workspace`
- `runtime.workspace.init()` — **[Stable]**
- `runtime.workspace.status()` — **[Stable]**

### `runtime.storage`
- `runtime.storage.blobs.put()` — **[Stable]**
- `runtime.storage.blobs.get()` — **[Stable]**

### `runtime.repository`
- `runtime.repository.commits.create()` — **[Stable]**
- `runtime.repository.graph.traverse()` — **[Stable]**

### `runtime.artifact`
- `runtime.artifact.registry.publish()` — **[Stable]**
- `runtime.artifact.lineage.trace()` — **[Stable]**

### `runtime.workspace_app`
- `runtime.workspace_app.execute(command)` — **[Stable]**
- `runtime.workspace_app.query(query)` — **[Stable]**

### `runtime.organization`
- `runtime.organization.directory.members()` — **[Stable]**
- `runtime.organization.registry.workspaces()` — **[Stable]**
- `runtime.organization.catalog.resources()` — **[Stable]**
- `runtime.organization.audit.history()` — **[Stable]**
- `runtime.organization.policy.evaluate()` — **[Stable]**
- `runtime.organization.configuration.current()` — **[Stable]**
- `runtime.organization.capabilities.available()` — **[Stable]**

> *Catatan: Keseluruhan fasad dari M1 hingga M3.5 telah dibekukan sebelum memasuki M4.*
