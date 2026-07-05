# ADR-0004: Penggunaan PostgreSQL untuk Structured Ledger & Audit

## Konteks
Meski kita memiliki Vector DB (Qdrant) untuk data tidak terstruktur/semantik, AetherOS harus menjamin integritas data (ACID) untuk konfigurasi sistem, RBAC (Role-Based Access Control), Audit Trail (jejak aksi), status siklus hidup agen (Reputasi), dan struktur organisasi (Company, Project, Workspace). Data ini bersifat rasional dan sangat terstruktur.

## Keputusan
Kita menggunakan **PostgreSQL (v16+)** sebagai basis data relasional (*Structured Ledger*) utama.

## Konsekuensi Positif
- Standar industri untuk basis data relasional, terbukti tangguh dalam menangani data skala perusahaan.
- Mendukung tipe data JSONB, yang memungkinkan keluwesan (schema-less) saat menyimpan log atau metrik *Organizational Intelligence* yang dapat berubah-ubah formatnya.
- Integritas relasional menjamin bahwa jika *Workspace* dihapus, agen di dalamnya dapat diatur perilakunya (Cascade).

## Konsekuensi Negatif
- Perlu mengelola *Database Migrations* (via Alembic).
- Manajemen skema yang ketat memerlukan perencanaan awal.
