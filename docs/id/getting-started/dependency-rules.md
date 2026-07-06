# Dependency Rules

Untuk mencegah *spaghetti code* dan *circular dependency*, sistem layer berikut diberlakukan secara kaku:

1. **Level 0 (Contracts)**: Tidak boleh mengimpor dari manapun selain Python Standard Library dan Pydantic.
2. **Level 1 (Kernel)**: Hanya boleh mengimpor dari **Contracts** dan sesama komponen internal Kernel (via DI).
3. **Level 2 (Services/Providers)**: Mengimpor Contracts dan antarmuka Kernel.

**Alat Validasi**: Gunakan `import-linter` atau `pydeps` pada CI/CD untuk menggagalkan build jika aturan ini dilanggar.
