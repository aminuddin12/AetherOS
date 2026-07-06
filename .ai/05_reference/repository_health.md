# Repository Health Metrics

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Indikator Kesehatan Repositori ini menetapkan parameter evaluasi kelayakan mutu repositori secara objektif dan terukur.

---

## 📈 Parameter Evaluasi Kesehatan (Repository Health Indicators)

Kesehatan repositori dinyatakan **HEALTHY** jika dan hanya jika seluruh parameter berikut bernilai **PASS**:

| Parameter Kesehatan | Target Kelulusan (Quality Gate) | Indikator Kelulusan | Status Terkini |
|---|---|---|---|
| **Documentation** | 100% berkas spesifikasi runtime sinkron dengan kode aktual. | Bebas broken links & render Mermaid sukses. | **PASS** |
| **Architecture** | Arah dependensi vertikal bottom-up mematuhi ADR-0025. | `import-linter` check lulus tanpa error. | **PASS** |
| **Dependency Direction** | Tidak ada impor konkret horizontal antar subsistem selevel. | `import-linter` check lulus. | **PASS** |
| **API Freeze** | Modul berlabel `[Stable]` tidak mengalami perubahan parameter destruktif. | API signature check lulus. | **PASS** |
| **Tests** | Seluruh test suite lulus offline & in-memory. | pytest check lulus 100%. | **PASS** |
| **ADR & RFC Compliance**| Kode aktual mematuhi keputusan ADR dan RFC aktif. | Drift check lulus. | **PASS** |
| **Coverage** | Target cakupan terpenuhi (Contracts/Kernel 100%, SDK/Execution 80%). | coverage report lulus. | **PASS** |
| **Lint & Formatting** | Kode bersih dari kesalahan sintaksis dan import tidak terpakai. | `ruff check .` lulus. | **PASS** |

---

## 🚦 Penanganan Degradasi Kesehatan (Status Transition)

- Jika salah satu parameter bernilai **FAIL**, status repositori beralih ke **DEGRADED**. AI wajib memprioritaskan perbaikan pada parameter yang rusak sebelum diperbolehkan mengajukan pull request baru.
- Jika terjadi konflik arsitektur fatal (seperti impor horizontal Concrete yang dipaksakan), status repositori beralih ke **FAILED** / **BLOCKED**, dan AI wajib menghentikan pengerjaan tugas (LEVEL 4 - Stop).
