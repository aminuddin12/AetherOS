# AI Capability Registry

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Registri ini mendaftarkan kapabilitas kognitif (*AI Capabilities*) yang dapat diaktifkan oleh model AI selama memproses pengerjaan tugas di repositori AetherOS.

---

## 🔌 Daftar Kapabilitas Kognitif (Cognitive Capabilities)

| Nama Kapabilitas | Tujuan Fungsional | Berkas Kebijakan Rujukan |
|---|---|---|
| **Architecture Analysis** | Menganalisis keselarasan model data dengan standardisasi DDD dan Clean Architecture. | [architecture.md](../03_policy/architecture.md) |
| **Architecture Review** | Mengevaluasi kode sumber baru dari kemungkinan penyimpangan arsitektural (*Drift*). | [review.md](../03_policy/review.md) |
| **ADR Validation** | Memastikan perubahan tidak merusak atau melanggar keputusan tertulis di indeks ADR. | [decision_hierarchy.md](decision_hierarchy.md) |
| **Dependency Analysis**| Memindai struktur import Python untuk menjamin kepatuhan arah vertikal. | [architecture.md](../03_policy/architecture.md) |
| **Documentation** | Meregenerasi atau mensinkronisasikan berkas spesifikasi runtime Markdown. | [documentation.md](../03_policy/documentation.md) |
| **Testing** | Menulis unit test tiruan (*Mock-based*) dan menguji cakupan kualitas test suite. | [testing.md](../03_policy/testing.md) |
| **Implementation** | Melakukan pengodean bersih bebas komentar dengan Pydantic DTO. | [quality.md](../03_policy/quality.md) |
| **Quality Audit** | Memvalidasi kelulusan gerbang mutu Definition of Complete (DoC). | [../definition_of_complete.md](../definition_of_complete.md) |
| **Security Audit** | Memeriksa kebocoran kunci API dan pembatasan isolasi eksekusi sandbox. | [security.md](../03_policy/security.md) |

---

## 🚦 Aturan Aktivasi Kapabilitas (Capability Profiling)

AI tidak diperkenankan mengaktifkan seluruh kapabilitas secara membabi buta. Aktifkan kapabilitas secara selektif berdasarkan tipe klasifikasi perubahan di [change_governance.md](../04_protocol/change_governance.md) (contoh: *Documentation Change* hanya memerlukan kapabilitas `Documentation` dan `Quality Audit`).
