# Testing Standard

1. **Unit Testing**: Wajib ada untuk setiap logika internal subsystem. Mocks/Stubs diperbolehkan menggunakan spesifikasi dari `core/contracts`.
2. **Integration Testing**: Diuji melalui `KernelBootstrap` untuk melihat komunikasi antar subsystem tanpa modul eksternal.
3. **No Database in Kernel Tests**: Uji Kernel tidak boleh memerlukan koneksi Redis, PostgreSQL, atau LLM aktif. Semuanya harus berjalan *in-memory*.
