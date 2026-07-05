# ADR-0002: Penggunaan Redis Streams untuk Event Bus

## Konteks
Dengan banyaknya agen spesialis, AI Kernel, dan Workspace yang bekerja serentak, kita butuh mekanisme komunikasi asinkron. *Direct API Call* (REST) antar agen menyebabkan arsitektur yang *tightly coupled* (saling ketergantungan erat) dan rentan terhadap kegagalan berantai (cascading failures). Jika Agen B sedang "mati", pesan dari Agen A tidak boleh hilang.

## Keputusan
Kita menggunakan **Redis Streams** sebagai *Event Bus* sentral dalam Aether Kernel.

## Konsekuensi Positif
- **Decoupled:** Pengirim (Publisher) tidak perlu tahu siapa penerimanya (Consumer).
- **Persistent:** Pesan tersimpan dalam stream hingga diproses dan di-acknowledge (ACK).
- **Consumer Groups:** Memungkinkan *load balancing* jika kita menjalankan banyak instance agen yang sama.
- Redis sangat cepat dan sebagian besar perusahaan sudah menggunakannya.

## Konsekuensi Negatif
- Menambah kompleksitas infrastruktur (wajib menjalankan container Redis).
- Memerlukan mekanisme *Dead Letter Queue* (DLQ) manual jika agen berulang kali gagal memproses pesan.
