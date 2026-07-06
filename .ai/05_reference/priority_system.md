# System Priority Matrix

---
Status: Implemented
Version: 1.0.0
Owner: AI Governance Architect
Last Updated: 2026-07-07
---

Protokol ini mendefinisikan prioritas optimasi teknis (*System Priority Matrix*) dalam pengambilan keputusan rekayasa di AetherOS.

---

## 📈 Skala Prioritas Optimasi (Optimization Scale)

```text
1. Integritas Arsitektur (Architecture Integrity)
                   │
                   ▼
2. Konsistensi Repositori (Repository Consistency)
                   │
                   ▼
3. Stabilitas API (API Stability)
                   │
                   ▼
4. Akurasi Dokumentasi (Documentation Accuracy)
                   │
                   ▼
5. Ketepatan Fungsionalitas (Correctness & Testing)
                   │
                   ▼
6. Performa Sistem (Performance & Boot Latency)
                   │
                   ▼
7. Kepatuhan Gaya Kode (Code Style & Formatting)
```

---

## 🚦 Aturan Penerapan Prioritas Utama

- **Integritas Arsitektur vs Gaya Kode**: Keharusan de-kopel modular vertikal (ADR-0025) wajib diutamakan dibanding kerapian atau kemudahan pengetikan kode. Jangan pernah menulis kode dengan struktur melintang horizontal demi menghemat pembuatan file atau baris kode.
- **Konsistensi vs Performa Mikro**: Kejelasan pemisahan state (`base.py`) dan descriptor (`manifest.yaml`) tidak boleh dikorbankan demi menghemat latensi parsing startup mikro-detik. Kejelasan kontrak arsitektur selalu menjadi prioritas utama.
- **Akurasi Dokumentasi**: Peta navigasi dokumentasi dan sinkronisasi metadata runtime wajib diperlakukan setara dengan penulisan kode fungsional.
