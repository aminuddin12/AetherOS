# ADR-0025: Runtime Dependency Direction

## Status
Accepted

## Context
Seiring berkembangnya AetherOS dengan bertambahnya jumlah subsistem runtime (Workspace, Storage, Repository, Artifact, dll), kita perlu mencegah terjadinya struktur kode yang menyerupai piringan spageti (*spaghetti code*) akibat dependensi yang saling silang. Ketergantungan dua arah (*circular dependencies*) akan menghancurkan modularitas OS.

## Decision
Ditetapkan hukum mutlak mengenai **Dependency Direction** antar-runtime:

1. **Arah Dependensi Vertikal (Bottom-Up):**
   Sebuah runtime HANYA BOLEH bergantung (import/memanggil) pada runtime yang berada pada layer di bawahnya dalam hierarki berikut:
   ```text
   Company Brain
        ↑
   Organization Runtime
        ↑
   Workspace Application Runtime
        ↑
   Artifact Runtime
        ↑
   Repository Runtime
        ↑
   Storage Runtime
        ↑
   Workspace Core Runtime
        ↑
   Runtime SDK
        ↑
   Execution Engine
        ↑
   Kernel
   ```
2. **Larangan Dependensi Horizontal:**
   Tidak boleh ada dependensi langsung (direct import) secara horizontal antar-runtime untuk urusan domain. Jika *Artifact* perlu berinteraksi dengan *Repository*, interaksi harus melewati **ResourceURI**, **Reference Objects**, atau disalurkan melalui **Runtime SDK**.
3. **Anti Circular Dependency:**
   *Circular dependency* adalah pelanggaran fatal arsitektur. Package yang menyebabkan *circular dependency* akan ditolak dalam fase CI/CD.
4. **Independensi Rilis:**
   Setiap runtime harus tetap dapat diuji, di-*build*, dan dirilis secara independen.

## Consequences
- **Positive**: Arsitektur tetap bersih, dapat diskalakan (*scalable*), dan pergantian implementasi pada satu runtime tidak merusak runtime lainnya.
- **Negative**: Orkestrasi fitur tingkat tinggi membutuhkan lapisan aplikasi ekstra (seperti *Workspace Application Runtime*) karena runtime dasar tidak bisa memanggil ke atas atau menyamping.
