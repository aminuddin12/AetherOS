# Review Protocol

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Sebelum melakukan modifikasi atau pembuatan kode sumber baru, model AI **wajib** melakukan audit arsitektur secara mandiri. Protokol ini memastikan bahwa kontribusi Anda tidak mencederai integritas arsitektur AetherOS.

---

## 📋 Matriks Audit Arsitektur (Pre-implementation Checklist)

| Area Review | Parameter Pemeriksaan | Kriteria Lulus (Pass Criteria) |
|---|---|---|
| **Integritas Arsitektur** | Apakah perubahan ini memperkenalkan dependensi melingkar (*circular dependency*)? | Bebas dari circular dependency. Divalidasi oleh `import-linter`. |
| **Arah Dependensi** | Apakah ada impor modul horizontal (melintang antar subsistem selevel) atau impor dari tingkat atas ke bawah? | Seluruh aliran impor bersifat vertikal ke bawah (*bottom-up*) mematuhi ADR-0025. |
| **API Freeze** | Apakah perubahan ini memodifikasi tanda tangan (*signature*) dari modul berstatus API Freeze (M1 s/d M3.5)? | Panggilan publik ke `core/contracts/` dan subsistem inti bersifat *read-only*. Perubahan tanda tangan API publik dilarang tanpa pengajuan RFC baru. |
| **Kesesuaian ADR** | Apakah desain ini bertentangan dengan keputusan di ADR-0001 s/d ADR-0028? | 100% patuh terhadap keputusan ADR aktif. |
| **Runtime Integrity** | Apakah perubahan ini menyalahgunakan batas kepemilikan data subsistem (ADR-0024)? | Setiap runtime hanya berurusan dengan tipe datanya sendiri. |
| **Capability Integrity** | Apakah subsistem baru mendeklarasikan kapabilitasnya secara eksplisit dalam Runtime Manifest? | Subsistem memiliki manifest yang mendefinisikan kapabilitas `Provides` dan `Requires` secara presisi. |
| **Technical Debt** | Apakah implementasi ini memperkenalkan perbaikan cepat (*workaround*) yang kotor? | Seluruh dependensi diselesaikan menggunakan Dependency Injection melalui Composition Root, bukan instansiasi ad-hoc. |
| **Kualitas Kode** | Apakah ada docstring atau komentar yang disisipkan di dalam berkas Python? | Bersih dari seluruh elemen komentar (`#`, `//`, dll). |

---

## 🛑 Prosedur Eskalasi Kegagalan Audit

Jika selama audit arsitektur awal Anda mendeteksi adanya pelanggaran aturan di atas pada instruksi yang diberikan oleh Chief Architect:
1. **HENTIKAN** proses penulisan kode segera.
2. Tulis laporan audit ringkas kepada Chief Architect yang menerangkan:
   - Aturan mana yang dilanggar (misal: Pelanggaran ADR-0025 karena impor horizontal).
   - Dampak arsitektural jika kode dipaksa ditulis.
   - Usulan alternatif solusi yang patuh arsitektur.
3. Tunggu persetujuan atau arahan revisi sebelum melanjutkan pengerjaan.
