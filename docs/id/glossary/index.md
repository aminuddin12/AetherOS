# AetherOS Glossary

Dokumen ini adalah sumber kebenaran tunggal (*single source of truth*) untuk seluruh terminologi teknis di dalam AetherOS. Konsistensi istilah mutlak diperlukan untuk mencegah ambiguitas, terutama karena AetherOS bukan sekadar *agent framework* melainkan sebuah *Operating System*.

### A
- **Agent**: Entitas kecerdasan buatan (*Intelligence Entity*) yang terdaftar di dalam direktori `Organization` dan mampu mengeksekusi aksi otonom berbasis `Company Brain`.
- **Artifact**: Sumber daya semantik (`Semantic Resource`) dalam format terstruktur yang diekstraksi dari *Repository*. Bukan sekadar metadata file, melainkan node dalam graf pengetahuan. Dialamatkan dengan `artifact://...`.

### C
- **Capability**: Otorisasi spesifik yang mendefinisikan batasan sumber daya yang boleh diakses entitas (manusia/agen). Meliputi *Compute*, *Storage*, *Model*, dan *Network*.
- **Company Brain**: Orkestrator Pengetahuan (*Knowledge Orchestrator*) pada *Intelligence Layer*. Ia TIDAK memiliki basis data pengetahuannya sendiri, melainkan menarik kesimpulan *on-the-fly* dengan membaca graf dari *Artifact*, *Repository*, dan *Organization*.

### K
- **Knowledge**: Hubungan logis yang dikonstruksikan oleh *Company Brain* dari kumpulan *Artifact* dan struktur *Repository*, umumnya direpresentasikan sebagai *Knowledge Triple* (Subject-Predicate-Object).

### L
- **Lineage**: Sejarah pembentukan atau transformasi sebuah *Artifact* yang melacak dari mana (dan oleh siapa) *Artifact* tersebut diturunkan.

### O
- **Organization**: Konteks Operasional Tertinggi (*Operating Context*) yang memayungi *Identity*, *Directory*, *Registry*, *Policies*, dan *Capabilities*.

### P
- **Projection**: Pandangan terarah (*view*) dari suatu *Artifact* ke dalam format lain. Misalnya, memproyeksikan *Artifact Code* menjadi *Artifact Documentation*.

### R
- **Reference**: Pointer memori yang aman (`ResourceReference` atau `WorkspaceReference`). Tidak mengandung data instansiasi asli (*Instance Object*) untuk menghindari ledakan memori.
- **Resource**: Objek universal di dalam AetherOS (dapat berupa Workspace, Storage, Repository, Artifact, Agent, atau Workflow).
- **Runtime**: Lapisan subsistem (*Subsystem Layer*) di AetherOS (misal: *Storage Runtime*, *Artifact Runtime*). Setiap runtime beroperasi mandiri dan mematuhi ADR-0027.

### U
- **URI (Universal Resource Identifier)**: Format alamat standar AetherOS (`scheme://domain/path`) yang digunakan untuk komunikasi antar runtime.

### W
- **Workspace**: Entitas dasar (*Aggregate Root*) yang membungkus kumpulan *Storage*, *Repository*, dan *Artifact* terkait dalam satu batas proyek. Dialamatkan dengan `workspace://...`.
