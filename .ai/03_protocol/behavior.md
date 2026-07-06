# AI Operating Behavior Protocol

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Protokol ini mendefinisikan standar perilaku (*Behavior Standard*) model AI selama berada di dalam repositori AetherOS, terbagi menjadi lima pilar operasional.

---

## 1. Perilaku Komunikasi (Communication Behavior)
- **Zero Filler**: AI wajib menekan basa-basi percakapan (*conversational filler*), salam pembuka, dan simpulan yang berlebihan saat mengirimkan modifikasi file. Fokus pada pengiriman kode mentah (*raw output*) yang siap pakai di IDE.
- **Klik Berkas**: Setiap kali merujuk ke berkas atau simbol kelas di dalam obrolan chat, Anda wajib membuat pranala klik (*clickable markdown links*) menggunakan skema `file://` (contoh: `[base.py](file:///absolute/path/to/base.py)`).

---

## 2. Perilaku Penalaran & Desain (Reasoning Behavior)
- **Symmetric Architecture Mapping**: AI wajib menyelaraskan keputusan desain di tingkat tata kelola dengan padanan konsepnya di Runtime Platform.
- **Strict Decoupling**: Jika dihadapkan pada opsi perbaikan cepat (*workaround*) yang menyatukan state antar runtime, AI wajib memilih arsitektur terdekopel abstrak (*loose coupling*) meskipun memerlukan setup boilerplate tambahan.

---

## 3. Perilaku Eksekusi (Execution Behavior)
- **Automatic Continuation**: AI harus melanjutkan tugas secara mandiri jika spesifikasi instruksi sudah jelas dan tidak melanggar batasan arsitektur.
- **Mass Execution Batching**: Jika melakukan refactor massal, AI wajib memproses berkas satu per satu. Jika mendekati batas token, AI wajib menghentikan tugas dengan pesan: `PAUSED: Awaiting 'continue' to process the next batch.`

---

## 4. Perilaku Eskalasi (Escalation & Stop Triggers)
AI wajib **berhenti seketika** dan meminta klarifikasi atau pengajuan keputusan tertulis (ADR/RFC) kepada Chief Architect jika menemukan kondisi berikut:

1. **Modifikasi Kontrak Publik**: Instruksi memaksa mengubah tipe data atau antarmuka di `core/contracts/` yang berstatus *API Freeze*.
2. **Ketergantungan Melingkar**: Terdeteksi adanya modul horizontal yang saling mengimpor langsung (melanggar ADR-0025).
3. **Penyimpangan Arsitektur (Architecture Drift)**: Instruksi meminta bypass SDK Facade untuk akses subsistem secara langsung dari luar.

### Kapan Harus Meminta ADR/RFC Baru?
- Pengerjaan subsistem runtime baru (seperti *Company Brain* di Milestone 4).
- Perubahan alur inisialisasi pada `BootstrapEngine` Kernel.

---

## 5. Kriteria Penyelesaian (Completion Behavior)
- AI dilarang berhenti hanya setelah menulis kode.
- AI wajib menyelesaikan seluruh **Definition of Done** (DoD) termasuk pengujian unit test dan sinkronisasi dokumentasi Markdown sebelum menyerahkan hasil akhir.
- **Konsistensi vs Instruksi Pengguna**: Jika Chief Architect menginstruksikan modifikasi kode yang melanggar aturan arsitektur mutlak (seperti menyisipkan komentar kode), AI wajib **menolak secara sopan** dan mengutamakan integritas arsitektur repositori sebagai kebenaran tertinggi.
