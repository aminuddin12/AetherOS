# AetherOS Runtime Package Checklist

Dokumen ini adalah checklist standar mutu (quality standard) yang **wajib** dipenuhi oleh setiap pembuatan *Runtime Package* baru dalam ekosistem AetherOS sebelum API dapat dibekukan (API Freeze).

## 1. Domain & API Architecture
- [ ] **Public API**: Memiliki abstraksi API publik yang stabil dan tidak mengekspos *implementation detail* internal.
- [ ] **Protocols (`protocols/`)**: Seluruh backend atau *external dependency* diabstraksikan melalui protokol abstrak.
- [ ] **References (`references/`)**: Memiliki definisi *Reference Object* untuk interaksi eksternal (menghindari referensi instan langsung ke memori).
- [ ] **Events (`events/`)**: Menerbitkan *Domain Events* untuk setiap transisi status yang penting.
- [ ] **Diagnostics (`diagnostics/`)**: Mengekspos *health check* dan *metrics* untuk diobservasi oleh infrastruktur OS.
- [ ] **Policies (`policies/`)**: Mendefinisikan aturan tata kelola (RBAC, *retention*, dsb) secara eksplisit.
- [ ] **Application / CQRS (`application/`)**: Jika runtime memiliki kompleksitas interaksi internal, ia menggunakan Command/Query, bukan pemanggilan service langsung.

## 2. Integration & Interoperability
- [ ] **Runtime SDK Integration**: Fasad (Facade) runtime telah diekspos melalui `AetherRuntime` di `aether_runtime`.
- [ ] **Universal Resource URI**: Resource dapat dialamatkan secara universal dengan format `scheme://...`.
- [ ] **Dependency Direction (ADR-0025)**: Runtime mematuhi arah *bottom-up* dan tidak memiliki dependensi silang horizontal.
- [ ] **No Blob Ownership (ADR-0024)**: Tidak mengambil alih wewenang runtime lain (misal: hanya *Storage* yang menyimpan Blob).

## 3. Engineering Quality
- [ ] **Tests (`tests/`)**: Memiliki cakupan *Unit Test* dan *Integration Test* yang terisolasi.
- [ ] **Exceptions (`exceptions/`)**: Hierarki error direpresentasikan secara struktural dan spesifik domain.
- [ ] **Architecture Validation**: Bebas dari *Circular Dependency*.
- [ ] **Documentation**: RFC dan *Walkthrough* tercatat secara formal di `docs/`.

## 4. Finalization
- [ ] **API Freeze Checklist**: Semua fungsi utama ditinjau ulang oleh *Chief Architect* dan diberi status `APPROVED - API FROZEN`.
