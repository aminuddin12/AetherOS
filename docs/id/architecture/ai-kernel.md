# AI Kernel

AetherOS bukan hanya kumpulan agen yang saling mengobrol. Inti dari sistem ini adalah **Aether Kernel** — sebuah lapisan abstraksi (OS Layer) yang memisahkan "Siapa yang berpikir" (Agen & LLM) dari "Bagaimana sistem berjalan" (Infrastruktur, Akses, dan Memori). 

Kernel memastikan bahwa agen bertindak sebagai entitas pekerja murni yang tunduk pada aturan sistem operasi, bukan entitas bebas.

## 1. Arsitektur Kernel

Aether Kernel bertindak sebagai pengelola sumber daya pusat (Central Resource Manager) seperti halnya kernel Linux mengelola memori dan CPU. 

```text
AETHER KERNEL (Layer Abstraksi OS)
├── Runtime
├── Scheduler
├── Event Dispatcher
├── Provider Router
├── Permission Engine
├── Memory Engine
├── Company Brain
├── Workspace Manager
├── Plugin Manager
├── Tool Runtime
├── Agent Supervisor
└── Metrics Engine
```

## 2. Komponen Utama Kernel

### 2.1 Runtime & Agent Supervisor
Menyediakan lingkungan hidup (lifecycle) tempat agen dijalankan. **Agent Supervisor** bertindak seperti `systemd` atau Process Manager; ia memantau kesehatan agen, melakukan *restart* jika agen mengalami *infinite loop*, dan menangani perpindahan tugas (handover) antar agen.

### 2.2 Scheduler & Event Dispatcher
- **Scheduler:** Mengatur urutan eksekusi tugas (kronologis atau berbasis prioritas) dan cron-job agen otonom.
- **Event Dispatcher:** Mengelola event bus asinkron (via Redis Streams). Kernel yang memutuskan pesan dari agen A dikirimkan ke agen B, agen tidak berhak memanggil agen lain secara langsung (seperti *Direct API Call*).

### 2.3 Provider Router
Mengabstraksikan LLM. Ketika agen membutuhkan komputasi penalaran (reasoning), Kernel merutekannya melalui Provider Router ke OpenAI, Anthropic, atau Ollama berdasarkan *cost*, *speed*, dan *capability* yang dibutuhkan.

### 2.4 Permission Engine
Mesin otorisasi (RBAC) yang selalu mengecek **AI Constitution** sebelum mengizinkan agen mengeksekusi suatu alat (Tool). 
*Contoh:* Agen meminta `ExecuteCommand(rm -rf /)`. Permission Engine mengevaluasi *Workspace Policy* dan menolak akses tersebut.

### 2.5 Memory Engine & Company Brain
Agen tidak melakukan *direct query* ke PostgreSQL atau Qdrant. Kernel menyediakan *Memory Engine SDK*. 
Ketika agen selesai bekerja, Kernel yang bertugas mem-parsing output agen, merangkumnya, mengekstrak pola, dan memasukkannya ke dalam **Company Brain** (Pengetahuan Jangka Panjang organisasi).

### 2.6 Workspace Manager
Mengatur batas kerja (*namespace*) untuk agen. Memisahkan konteks proyek A dan proyek B. Agen di Workspace A tidak bisa membaca file kode di Workspace B tanpa otorisasi lintas-proyek.

### 2.7 Tool Runtime & Plugin Manager
Mengelola kotak pasir eksekusi (OpenHands Sandbox). **Plugin Manager** memastikan bahwa SDK khusus pihak ketiga (misalnya ekstensi *Cyber Security Pack*) dapat dimuat (loaded) dengan aman ke dalam sistem tanpa merusak Kernel inti.

### 2.8 Metrics Engine
Mencatat telemetri dan kinerja agen (OpenTelemetry). Dari metrik ini, fitur *Agent Reputation* dan *Cost Analytics* dapat beroperasi.

## 3. Alur Kerja (Workflow) dari Perspektif Kernel

1. **System Call:** Agen ingin menulis file. Ia tidak menggunakan Python `open()`. Ia menggunakan *Tool System Call* `WriteFileTool()`.
2. **Intercept:** Kernel menangkap *System Call* ini.
3. **Evaluate:** Kernel memanggil *Permission Engine* untuk memeriksa *AI Constitution*.
4. **Execute:** Jika diizinkan, *Tool Runtime* mengeksekusinya di dalam kotak pasir (Sandbox).
5. **Record:** *Metrics Engine* mencatat waktu dan biaya. *Memory Engine* menyimpan jejak bahwa file telah diubah.

Dengan pendekatan ini, **Organisasi (melalui Kernel) memiliki kontrol penuh atas kecerdasan buatan (Agen)**.

---

🔗 **Selanjutnya:** [Execution Loop →](execution-loop.md)
