# ADR-0012: Workspace as Operational Unit

## Status
Accepted

## Context
Di dalam platform OS tradisional, "Workspace" sering dianggap sebatas direktori kerja, repositori Git, atau "IDE Folder". Namun untuk AetherOS (The Open Agent Operating System), pandangan tersebut terlalu sempit. Kita membutuhkan sebuah boundary yang mampu merangkum tidak hanya file, melainkan juga _policies, knowledge, workflows, execution context, dan multi-agent collaboration_. 

## Decision
Kita mendefinisikan Workspace sebagai **Operational Unit Terkecil**. Workspace beroperasi layaknya *Process Space* (seperti Docker Container atau Linux Process Namespace), di mana:
- Ia mengisolasi *Artifacts*, *Knowledge*, dan *Workers*.
- Ia menegakkan *Policies* secara mandiri (mis. larangan akses internet, batasan waktu eksekusi).
- Seluruh state internal dilindungi oleh *Coordinator* dan *LockManager*, menjadikannya sangat terkendali layaknya transaksi database.

## Consequences
- **Keuntungan**: AetherOS dapat mendukung banyak Workspace sekaligus secara bersamaan dan aman, memungkinkan pemisahan departemen (Engineering vs Finance) layaknya multi-tenancy.
- **Kerugian**: Overhead memori dan komputasi untuk mengelola Context dan Session setiap kali sebuah Workspace dioperasikan.
