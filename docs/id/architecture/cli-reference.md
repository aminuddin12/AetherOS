# 09.2 — Referensi CLI

> Dokumen ini mendeskripsikan antarmuka baris perintah (CLI) AetherOS untuk interaksi langsung dengan orkestrator.

---

## 9.2.1 Instalasi dan Setup

### Perintah Dasar

| Command | Deskripsi |
|---------|-----------|
| `aetheros init` | Inisialisasi workspace baru |
| `aetheros config` | Konfigurasi sistem (API keys, providers, dll.) |
| `aetheros status` | Status sistem (agen, tasks, health) |
| `aetheros version` | Versi AetherOS |

---

## 9.2.2 Project Management

| Command | Deskripsi |
|---------|-----------|
| `aetheros project create <name>` | Buat proyek baru |
| `aetheros project list` | Daftar proyek |
| `aetheros project use <name>` | Set proyek aktif |
| `aetheros project info [name]` | Info detail proyek |
| `aetheros project archive <name>` | Arsipkan proyek |

---

## 9.2.3 Instruction Management

| Command | Deskripsi |
|---------|-----------|
| `aetheros instruct "<instruksi>"` | Kirim instruksi ke Manager Agent |
| `aetheros instruct --file <path>` | Kirim instruksi dari file |
| `aetheros instruct --priority high` | Kirim instruksi dengan prioritas |
| `aetheros instruct list` | Daftar instruksi aktif |
| `aetheros instruct status <id>` | Status instruksi |
| `aetheros instruct cancel <id>` | Batalkan instruksi |

---

## 9.2.4 Task Monitoring

| Command | Deskripsi |
|---------|-----------|
| `aetheros task list` | Daftar tasks (filter: --status, --agent, --project) |
| `aetheros task info <id>` | Detail task |
| `aetheros task logs <id>` | Log eksekusi task |
| `aetheros task retry <id>` | Retry task yang gagal |
| `aetheros task watch` | Real-time task monitoring |

---

## 9.2.5 Agent Management

| Command | Deskripsi |
|---------|-----------|
| `aetheros agent list` | Daftar agen dan status |
| `aetheros agent info <role>` | Detail agen |
| `aetheros agent restart <role>` | Restart agen |
| `aetheros agent logs <role>` | Log agen |
| `aetheros agent scale <role> <count>` | Scale agen instances |

---

## 9.2.6 Approval Management (HITL)

| Command | Deskripsi |
|---------|-----------|
| `aetheros approve list` | Daftar approval pending |
| `aetheros approve info <id>` | Detail approval request |
| `aetheros approve grant <id>` | Setujui aksi |
| `aetheros approve deny <id> --reason "<alasan>"` | Tolak aksi |

---

## 9.2.7 Knowledge & Brain

| Command | Deskripsi |
|---------|-----------|
| `aetheros brain stats` | Statistik Project Brain |
| `aetheros brain search "<query>"` | Semantic search di knowledge base |
| `aetheros brain export --format json` | Export knowledge entries |

---

## 9.2.8 Analytics

| Command | Deskripsi |
|---------|-----------|
| `aetheros analytics cost` | Ringkasan biaya (filter: --period, --project, --agent) |
| `aetheros analytics tokens` | Penggunaan token |
| `aetheros analytics performance` | Metrik performa |

---

## 9.2.9 System Administration

| Command | Deskripsi |
|---------|-----------|
| `aetheros system health` | Health check semua komponen |
| `aetheros system providers` | Status LLM providers |
| `aetheros system config set <key> <value>` | Set konfigurasi |
| `aetheros system config get <key>` | Get konfigurasi |
| `aetheros system audit --trace <trace_id>` | Trace audit logs |

---

## 9.2.10 Global Flags

| Flag | Deskripsi |
|------|-----------|
| `--project <name>` | Override proyek aktif |
| `--output json\|table\|yaml` | Format output |
| `--verbose` | Verbose output |
| `--quiet` | Suppress non-essential output |
| `--no-color` | Disable colored output |
| `--config <path>` | Path ke config file |

---

🔗 **Selanjutnya:** [Desain Dashboard →](dashboard-design.md)

🔗 **Kembali:** [Spesifikasi API ←](api-specification.md)
