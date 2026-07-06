---
Status: Deprecated
Reason: Legacy architecture based on multi-agent chatbot framework (Redis, PostgreSQL, Qdrant, FastAPI, LangGraph, PydanticAI) has been replaced by the modular Operating System model (Kernel, Execution Engine, Runtime SDK, Workspace, Storage, Repository, Artifact, Organization).
Superseded By: ADR-0011 through ADR-0027, docs/id/architecture/book.md
Replacement: docs/id/architecture/book.md
---

# Reputasi Agen & Metrik

Mengorkestrasi puluhan agen yang bekerja secara paralel memerlukan sistem *performance tracking* yang objektif. Dalam AetherOS, setiap agen tidak diperlakukan sama secara *default*. Agen harus membuktikan kemampuannya.

Sistem **Reputasi Agen (Agent Reputation)** mencatat, mengukur, dan memberi peringkat kinerja agen. Metrik ini krusial bagi *Manager Agent* (atau *Scheduler Kernel*) untuk membuat keputusan: **"Kepada siapa tiket JIRA ini harus ditugaskan?"**

## 1. Komponen Metrik Penilaian

Peringkat (Score) agen tidak hanya diukur dari "berhasil/tidaknya" tugas, melainkan dikomputasikan dari vektor metrik 8-dimensi:

| Dimensi | Deskripsi | Cara Pengukuran (Contoh) |
|---------|-----------|--------------------------|
| **Performance** (Keberhasilan) | Berapa banyak *task* yang selesai sesuai Acceptance Criteria? | (Task Sukses / Total Task) * 100% |
| **Reliability** (Keandalan) | Seberapa jarang agen ini terjebak *infinite loop* atau gagal mengeksekusi *tool*? | Frekuensi intervensi supervisor kernel. |
| **Security** | Apakah kode yang dihasilkan aman? | Rasio penolakan (*reject*) dari Security Agent atau SAST tools. |
| **Creativity** | (Untuk tipe tertentu) Seberapa baik agen mencari alternatif solusi atau *workaround* saat *stuck*? | Keberhasilan menyelesaikan *task* kompleks yang tidak ada panduannya di *Company Brain*. |
| **Speed** (Kecepatan) | Seberapa cepat tugas diselesaikan? | Latency rata-rata dari *Assigned* hingga *Review*. |
| **Cost** (Biaya Token) | Seberapa efisien agen menggunakan prompt (token)? | Total $USD per tugas (misal: meminimalkan pemanggilan Claude 3.5 Sonnet untuk hal trivial). |
| **Communication** | Apakah agen menjelaskan argumen / komitnya dengan baik? | Sentiment analysis dari *code review* atau kejelasan deskripsi PR. |
| **Teamwork** | Seberapa efektif agen bekerja sama (handover) dengan agen lain tanpa kehilangan konteks? | Waktu resolusi pada *Multi-Agent Issue*. |

## 2. Pengambilan Keputusan oleh Manager (Routing)

Reputasi ini memungkinkan *Manager Agent* melakukan penugasan (routing) tugas secara dinamis dan cerdas. 

### Skenario A: Tiket Prioritas Rendah / Refactoring Rutin
*   **Kebutuhan:** *Low Cost*, *Medium Speed*.
*   **Aksi Manager:** Menugaskan "Junior Backend Agent" (Ollama Llama-3 / GPT-4o-Mini) yang *Cost Score*-nya sangat murah, meskipun kecepatannya rata-rata.

### Skenario B: Tiket Kerentanan Keamanan (Hotfix CVE)
*   **Kebutuhan:** *High Security*, *High Speed*, *High Reliability*. Cost tidak masalah.
*   **Aksi Manager:** Menugaskan "Senior Security & Backend Agent" (Claude 3.5 Sonnet / GPT-4o) dengan reputasi *Security Score* 98%+ dan *Reliability* 100%, mengesampingkan faktor *Cost*.

### Skenario C: Eksperimen Algoritma Baru
*   **Kebutuhan:** *High Creativity*, *High Performance*.
*   **Aksi Manager:** Memilih agen dengan *Creativity Score* tertinggi yang pernah sukses memecahkan *algorithmic bug* sebelumnya.

## 3. Degradasi dan Rehabilitasi Reputasi

Reputasi bersifat dinamis. 
1. **Degradasi:** Jika model AI di baliknya (misal model pihak ketiga) mengalami *performance drift* dan tiba-tiba agen tersebut mulai menulis kode yang penuh bug, maka *Performance Score* dan *QA Reject Rate* akan meningkat.
2. **Demotion (Penurunan Pangkat):** Sistem secara otomatis akan berhenti memberikan tugas kritis (*High-Severity*) kepada agen ini.
3. **Rehabilitasi:** Administrator dapat memerintahkan fase [Siklus Hidup: Training](agent-lifecycle.md) ulang untuk mereset metrik awal, memperbarui *prompt*, atau meng-upgrade model dasar agen tersebut.

Sistem Reputasi memastikan kualitas yang dihasilkan oleh *organisasi AI* Anda selalu bergerak ke arah positif (berkat evolusi dan seleksi natural).

---

🔗 **Selanjutnya:** [Komunikasi Agen →](agent-communication.md)
