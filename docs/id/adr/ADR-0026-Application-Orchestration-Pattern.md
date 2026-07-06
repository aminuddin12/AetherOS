# ADR-0026: Application Orchestration Pattern

## Status
Accepted

## Context
Pada Workspace Application Runtime (M3.4), kita mengorkestrasi berbagai runtime (Workspace Core, Storage, Repository, Artifact) untuk mengeksekusi aksi organisasi tingkat tinggi. Mengizinkan *Commands* atau *Queries* memanggil subsistem secara langsung tanpa lapisan pengatur akan memicu logika *spaghetti* (God Object anti-pattern) dan menyulitkan implementasi fitur silang (cross-cutting concerns) seperti otorisasi, metrik, dan *tracing*.

## Decision
Arsitektur **Application Orchestration Pattern** ditetapkan dengan aturan berikut:

1. **Use Case Layer, bukan Business Logic Layer:** Workspace Application HANYA bertugas sebagai orkestrator (Validasi -> Resolve Runtime -> Pipeline -> Publish Event). State bisnis murni tetap hidup di Domain Runtime masing-masing.
2. **Command & Query Bus:** Semua eksekusi harus melalui Bus (`CommandBus`, `QueryBus`). Command tidak pernah memanggil Runtime SDK secara langsung, ia meneruskannya melalui Bus menuju Handler.
3. **Orchestration Pipeline:** Eksekusi Use Case WAJIB melintasi Middleware Pipeline terpusat (Validation, Authorization, Metrics, Tracing, Logging) sebelum menyentuh Runtime.
4. **Immutable Result Objects:** Handler dilarang mereturn tipe generik (seperti `bool` atau `dict`). Handler harus mengembalikan DTO Imutabel (contoh: `WorkspaceInitializationResult`).
5. **Composition Root:** Perakitan dependensi Runtime dilakukan terpusat melalui `composition/bootstrap.py`. *Command* tidak boleh merakit / melakukan instansiasi runtime sendiri.
6. **Application Context:** Semua *Commands* beroperasi di atas abstraksi `ApplicationContext`, yang merangkum *OrganizationContext*, *WorkspaceContext*, dan *RuntimeSession*. Ini mempersiapkan transisi mulus ke Milestone 3.5 (Organization Runtime).

## Consequences
- **Positive:** Skalabilitas luar biasa; logika tidak bercampur; GUI/Studio dapat dengan mudah mengonsumsi Result Objects; Observability (metrics & tracing) terjamin secara otomatis untuk setiap Use Case.
- **Negative:** Diperlukan struktur *boilerplate* yang cukup tebal (Command, Handler, Result, Bus) untuk operasi yang tampak sederhana.
