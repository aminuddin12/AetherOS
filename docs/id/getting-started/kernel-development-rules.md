# Kernel Development Rules

AetherOS Kernel adalah jantung dari sistem operasi agen ini. Karena posisinya yang sangat kritikal, pengembangan Kernel harus tunduk pada aturan ketat berikut:

## 1. Ketergantungan (Dependencies)
- Kernel **hanya boleh bergantung pada** `core/contracts`.
- Kernel **DILARANG MENGIMPOR**:
  - `provider` (LLM vendor khusus)
  - `distribution`
  - `workspace runtime`
  - `company brain`
  - `plugin marketplace`
  - `database` (PostgreSQL, SQLite, Redis, Qdrant)
  - `http` / `fastapi`
  - `langgraph` / `openhands`

## 2. Komunikasi Antar Subsystem
- Semua komunikasi antar subsystem **harus menggunakan Contract** atau **Event** (`SystemEvent`, `SystemCommand`, dll).
- Dilarang keras memanggil logika internal subsystem lain secara langsung tanpa melalui antarmuka yang didefinisikan (Interface/Protocol).

## 3. Dokumentasi Subsystem
- Semua subsystem di dalam Kernel **WAJIB** memiliki `README.md`.

## 4. Injeksi Dependensi (IoC)
- Seluruh dependency antar class **wajib menggunakan Constructor Injection**.
- **TIDAK BOLEH** ada Singleton Global.
- **TIDAK BOLEH** ada Service Locator Anti-Pattern.
- **TIDAK BOLEH** ada Circular Import.

## 5. Manajemen State & Event
- Seluruh state yang bersifat *mutable* (berubah-ubah) **HANYA BOLEH** berada pada subsystem `StateManager`.
- Seluruh event yang beredar di dalam sistem **HARUS immutable** (frozen).

## 6. Sifat Dapat Diganti (Pluggability)
- Semua subsystem harus dapat diganti (di-swap) implementasinya tanpa mengharuskan modifikasi pada subsystem lainnya.
