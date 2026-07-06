# AetherOS Internal Runtime Specification

## 1. Tujuan Runtime Layer
Runtime Layer adalah SDK resmi dan satu-satunya antarmuka publik (System Call Interface) untuk berkomunikasi dengan AetherOS Kernel dan Execution Engine. Tujuannya adalah memastikan bahwa seluruh interaksi—baik dari CLI, GUI (Aether Studio), REST API, maupun VS Code Extension—berjalan secara aman, terkendali, dan tersentralisasi.

## 2. Posisi Runtime dalam Arsitektur
```text
[ Frontend (CLI / GUI / REST / Extension) ]
                       ↓
[ Runtime SDK (Session, Context, Facade)  ]  <-- Anti-Corruption Layer (ACL)
                       ↓
[ Core Kernel & Execution Engine          ]
```
Tidak ada satupun Frontend yang diizinkan untuk mengimpor atau memanggil objek dari `core.kernel` atau `core.execution` secara langsung. Semua harus melalui `AetherRuntime`.

## 3. Boundary dengan Kernel & Frontend
- **Boundary Atas (ke Frontend)**: Menyediakan fungsi asinkron (Async First) yang mengembalikan Data Transfer Objects (DTO) standar.
- **Boundary Bawah (ke Kernel)**: Memanggil fungsi sinkron/asinkron Kernel, menangani injeksi dependensi jika perlu, dan menerjemahkan entitas Kernel menjadi DTO Runtime.

## 4. Runtime Context & Session
- **RuntimeContext**: Menyimpan status deterministik dari pemanggil, termasuk User ID, Workspace saat ini, Locale, Configuration, Trace ID, dan Permission.
- **RuntimeSession**: Dikelola per-instance dari Frontend. Session memungkinkan lifecycle (Start/Stop) dan memori sementara (cache) selama Frontend terhubung ke Runtime.

## 5. Runtime Middleware
Setiap perintah (`facade`) akan melewati Pipeline Middleware sebelum menyentuh Kernel:
`Request -> Logging -> Permission -> Metrics -> Tracing -> Validation -> Facade Exec`

## 6. Runtime DTO/Models (ACL)
Runtime tidak mengekspos model internal (seperti `KernelManifest`). Runtime memiliki representasinya sendiri di `runtime/models/`, misalnya `KernelStatus`, `ExecutionStatus`.

## 7. Event Flow
Runtime dapat memancarkan events secara asinkron yang dapat di-subscribe oleh GUI atau REST Socket:
- `RuntimeStarted`, `RuntimeShutdown`
- `CommandExecuted`, `CommandFailed`
- `WorkspaceOpened`, `WorkspaceClosed`

## 8. Threading & Async Model
Semua API yang diekspos melalui `AetherRuntime` bersifat **Async First**. Hal ini diwajibkan untuk mempersiapkan eksekusi Workspace, AI Provider, dan Organisasi yang berat pada I/O di masa depan, mencegah perubahan *breaking* pada Frontend saat transisi asinkron terjadi sepenuhnya.

## 9. Versioning & Compatibility
API dari Runtime SDK mematuhi Semantic Versioning yang ketat. Jika terjadi perubahan *under-the-hood* pada Kernel, Runtime akan memetakannya kembali ke DTO lama untuk menjaga kompatibilitas, kecuali terdapat kenaikan Major Version.
