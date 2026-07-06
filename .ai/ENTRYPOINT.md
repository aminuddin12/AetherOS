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

---

## 🚦 Cara Melanjutkan & Kapan Harus Berhenti

- **Cara Melanjutkan**: Jika instruksi sudah jelas dan prasyarat terpenuhi, AI harus bertindak di bawah status daur hidup `PLANNING` menuju `IMPLEMENTING`.
- **Kapan Harus Berhenti (Stop Triggers)**: Jika terdapat ketidakjelasan arsitektur (LEVEL 3) atau konflik arsitektur fatal (LEVEL 4), AI wajib menghentikan eksekusi dan mengevaluasi status kesehatannya menjadi `STOPPED` atau `FAILED` serta melapor kepada Chief Architect.
