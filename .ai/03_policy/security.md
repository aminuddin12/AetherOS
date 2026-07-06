# Security Policy

---
Status: Implemented
Version: 1.0.0
Owner: Core Platform Team
Last Updated: 2026-07-07
---

Kebijakan ini menetapkan batas perlindungan keamanan lingkungan host dan otorisasi data di repositori AetherOS.

---

## 1. Aturan Isolasi Eksekusi Agen (Sandboxing Policy)

- **Isolated by Default**: Seluruh eksekusi baris kode dinamis atau perintah shell/terminal yang dipicu oleh agen wajib disalurkan melalui sandbox (`core/execution/`) terisolasi untuk mencegah eksploitasi lingkungan host.
- **Resource Constraints**: Setiap pemanggilan command atau subprocess oleh agen harus dibatasi oleh aturan timeout kaku dan batasan memori/CPU untuk menghindari *denial-of-service* (DoS).

---

## 2. Perlindungan Kredensial & Kunci API (Token Protection Policy)

- **Strict Environment Separation**: Kunci API model bahasa (seperti OpenAI API key, Gemini API key) dilarang keras ditulis secara hardcoded dalam kode sumber, berkas pengujian, atau konfigurasi manifest. Gunakan variabel lingkungan (`.env`).
- **No Token Logs**: Sistem supervisor telemetri dilarang mencatat isi obrolan yang mengandung kunci API atau token sesi rahasia ke dalam berkas log publik.
