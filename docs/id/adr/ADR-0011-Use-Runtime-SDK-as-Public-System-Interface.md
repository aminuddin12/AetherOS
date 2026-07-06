# ADR-0011: Use Runtime SDK as the Public System Interface

## Status
Accepted

## Context
AetherOS berkembang dari "AI Agent Framework" menjadi **Open Agent Operating System**. Dengan bertambahnya lapisan (Kernel, Execution, Workspace, Knowledge, Organization), mengekspos Kernel secara langsung ke Frontend (CLI, GUI, REST, SDK) menciptakan risiko *tight-coupling*. Apabila Kernel mengalami refactoring internal, semua aplikasi klien di atasnya akan rusak. Selain itu, CLI secara historis memuat *business logic* (di folder `services/`) yang menyebabkan fungsionalitas tersebut tidak bisa digunakan ulang oleh Aether Studio (GUI).

## Decision
Kita memutuskan untuk membuat lapisan penengah resmi: **Internal Runtime SDK** (`runtime/`). Lapisan ini bertindak layaknya "System Call Interface" (syscall) pada sistem operasi tradisional. 

Aturan arsitektural yang ditetapkan:
1. **Satu-satunya Entry Point**: CLI tidak boleh memanggil Kernel langsung. Semua interaksi mengalir melalui: `CLI -> Runtime SDK -> Kernel`.
2. **Anti-Corruption Layer (ACL)**: Runtime memisahkan struktur datanya sendiri (Runtime Models/DTO) dari objek internal Kernel. DTO dikonversi oleh lapisan *Adapters*.
3. **Async First**: Walaupun Kernel saat ini beroperasi in-memory secara sinkron, seluruh fungsi publik Runtime SDK diwajibkan menggunakan pola asinkron (`async def`). Ini mencegah *breaking changes* ketika Workspace dan Knowledge (yang sangat berat pada I/O) diimplementasikan kelak.
4. **No Business Logic**: Runtime SDK hanyalah **Gateway**. Tugasnya murni berkisar pada *Validation, Authorization, Transformation, Routing, dan Response*. Logic inti tetap milik Kernel, Workspace, atau komponen internal lain.
5. **Event Translation**: Runtime memiliki Event Bus terpisah. Event dari Kernel dicegat, diterjemahkan, lalu dipancarkan kembali sebagai Runtime Event (misal `KernelWorkerStarted` -> `RuntimeExecutionStarted`) agar struktur event internal tidak terekspos.

## Consequences
- **Keuntungan**: 
  - Frontend (Aether Studio, REST, CLI) menjadi sangat tipis dan 100% menggunakan kode yang sama.
  - Skalabilitas masa depan terjamin; Kernel dapat dirombak total tanpa merusak UI.
- **Kerugian**: 
  - Penambahan lapisan abstraksi (Facade -> Services -> Adapters) dan boilerplate yang signifikan untuk operasi-operasi sepele.
