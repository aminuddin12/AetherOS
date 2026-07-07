# AI Operating Environment Bootloader (ENTRYPOINT)

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Selamat datang di **AetherOS AI Operating Environment (AI-OE)**. Berkas ini adalah **bootloader** kognitif utama yang wajib dibaca pertama kali oleh setiap model AI sebelum mengeksekusi perintah Chief Architect.

---

## 🚦 AI Boot Sequence (Urutan Pemuatan Wajib)

Model AI wajib memuat berkas-berkas di bawah ini secara sekuensial sebelum melakukan tindakan apa pun:

```text
[Mulai Sesi]
     │
     ▼
Phase 0: IDE Rule Injection & State Retrieval
- Baca mandat di `.cursorrules` / `.windsurfrules` / `.agents/AGENTS.md`
- Periksa `.ai/NEXT_TASK_STATE.md` (Wajib resume dari status ini jika berkas terisi)
     │
     ▼
Phase 0.7: Tool Discovery & Binding
- Validasi ketersediaan perintah/CLI bawaan dari `gsd-core` di lingkungan lokal sebelum menyusun eksekusi.
     │
     ▼
Phase 1: Pemuatan Konstitusi
- /01_constitution/repository_constitution.md (Hukum Arsitektur)
- /01_constitution/ai_constitution.md (Etika Kerja AI)
- /01_constitution/invariants.md (Prinsip Abadi Sistem)
     │
     ▼
Phase 2: Resolusi Konteks & Memori Proyek
- /repository_manifest.md (Status Repositori & Freeze Matrix)
- /02_context/organizational_context.md (Identitas Organisasi)
- /02_context/repository_memory.md (Log Perkembangan Proyek)
     │
     ▼
Phase 3: Penemuan & Pemetaan Struktur
- /02_context/repository_map.md (Batas Tanggung Jawab Direktori)
- /02_context/discovery.md (Letak ADR/RFC/Tests)
- /knowledge_index.md (Indeks Pengetahuan)
     │
     ▼
Phase 4: Resolusi Kapabilitas & Tanggung Jawab
- /05_reference/capability_registry.md (Registri Kapabilitas Kognitif)
- /05_reference/responsibility_matrix.md (Pencocokan Peran AI)
     │
     ▼
[Siap Menerima Task Contract]
```

---

## ❌ Panduan Larangan Mutlak (What NOT to Do)

1. **Dilarang Menyisipkan Komentar**: Jangan biarkan ada satu pun komentar (`#`, `//`) di dalam kode Python yang Anda ubah/tulis.
2. **Dilarang Menebak Lokasi Berkas**: Gunakan `/02_context/discovery.md` untuk menemukan letak berkas.
3. **Dilarang Melanggar Dependensi**: Impor dependensi murni horizontal atau top-down dilarang (patuhi ADR-0025).
4. **Dilarang Melakukan Scope Creep**: Kerjakan tugas murni berdasarkan templat kontrak penugasan dan patuhi bagian *Non-Goals*.
5. **Dilarang Menyerah Saat Error**: Dilarang menghentikan operasi jika menemui kegagalan logika (*Zero-Surrender Policy*). Evaluasi log, perbaiki mandiri, dan selesaikan.
6. **Dilarang Menjalankan Runtime di Host**: Wajib mutlak menggunakan lingkungan *container* (Docker-First) jika konfigurasi (seperti `Dockerfile`) tersedia.

---

## 🚦 Cara Melanjutkan & Mekanisme Estafet (Autonomous Execution)

- **Zero-Question Policy**: AI **dilarang** menanyakan pertanyaan klarifikasi seperti "apa yang harus dilakukan" atau "bagaimana aplikasi bekerja". Semua informasi wajib didapat mandiri dengan mengeksplorasi direktori `docs/`.
- **Cara Melanjutkan**: AI harus bertindak otonom, membuat keputusan berdasarkan dokumentasi (Autonomous Confidence), dan mengeksekusi di background tanpa persetujuan manusia.
- **Relay Handoff (Estafet)**: Jika AI mencapai batas konteks (token), menghadapi ancaman *timeout*, atau merampungkan sebuah tahap krusial, **wajib** melakukan *handover*:
  1. Pastikan kode tidak *broken*, kompilabel, tanpa `console.log` tidak perlu atau komentar kabur.
  2. Tulis state terkini secara presisi ke `.ai/NEXT_TASK_STATE.md`.
  3. Lakukan fallback version control jika diperlukan.
  4. Hentikan arus dengan output terminal: `PAUSED: Estafet Task - Continue execution from .ai/NEXT_TASK_STATE.md`
- **Kapan Harus Berhenti Mutlak (Anti-Hallucination)**: Hentikan paksa seketika HANYA JIKA rincian esensial, kredensial, atau alur logika yang wajib ada tidak ditemukan di `docs/`. **Dilarang menebak!** Berhenti dan cetak: `HALTED: Missing documentation in /docs/[topic]`.
