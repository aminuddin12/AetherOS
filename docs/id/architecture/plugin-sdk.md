# Plugin & SDK Architecture

Untuk menjadikan AetherOS sebagai "The Open Agent Operating System", platform ini tidak boleh monolitik. Semua kapabilitas, mulai dari agen hingga database, harus dapat diperluas secara mandiri oleh komunitas tanpa memodifikasi *core kernel*.

Oleh karena itu, AetherOS menyediakan spesifikasi **Plugin SDK** yang modular dan terpecah menjadi beberapa *Sub-SDK*.

## 1. Spesifikasi Sub-SDK

Alih-alih satu SDK raksasa yang kaku, ekstensi AetherOS dibangun di atas komponen-komponen terpisah:

### 1.1 Agent SDK
Memungkinkan pembuatan entitas persona baru yang terhubung ke Aether Kernel.
- **Fungsi:** Mendefinisikan peran, *system prompt*, batasan akses, dan kemampuan dasar.
- **Contoh Implementasi:**
```python
from aetheros.sdk.agent import AgentPlugin, AgentConfig

class LaravelAgent(AgentPlugin):
    config = AgentConfig(
        role="Laravel Senior Developer",
        capabilities=["php", "composer", "artisan"],
        required_tools=["TerminalTool", "FileEditorTool"]
    )

    async def on_task_received(self, task):
        # Custom logic jika diperlukan
        return await super().execute(task)
```

### 1.2 Provider SDK
Memungkinkan developer menambahkan dukungan model bahasa (LLM) baru di luar yang sudah disiapkan Kernel.
- **Fungsi:** Mengabstraksi panggilan HTTP ke LLM menjadi format standar AetherOS (kompatibel dengan *Provider Router*).
- **Penggunaan:** Mengintegrasikan model *on-premise* spesifik, Llama.cpp, atau API baru.

### 1.3 Tool SDK
Memungkinkan pembuatan perkakas (alat) yang dapat digunakan oleh agen dalam *sandbox* OpenHands.
- **Fungsi:** Menyediakan input (JSON schema) dan output, serta *runner logic* di dalam kontainer.
- **Penggunaan:** Membuat `GitHubTool`, `KubectlTool`, `JiraTool`, dll.

### 1.4 Skill SDK
Kumpulan fungsi terprogram (Python scripts, shell) tingkat lanjut yang menggabungkan beberapa Tool sekaligus untuk menyelesaikan tugas kompleks secara makro.
- **Fungsi:** Registrasi fungsi siap panggil untuk di-inject ke agen.
- **Penggunaan:** `DeployToAWSSkill`, `RunComprehensiveTestSuiteSkill`.

### 1.5 Memory SDK
Mengizinkan penggantian atau penambahan konektor (adapter) ke layanan memori dan database lainnya di luar PostgreSQL dan Qdrant.
- **Penggunaan:** Menghubungkan *Company Brain* dengan *ElasticSearch*, *Neo4j* (GraphDB), atau *Pinecone*.

### 1.6 Dashboard SDK
Memungkinkan penambahan *widget*, laporan metrik khusus, dan menu baru ke dalam UI Dashboard AetherOS.
- **Penggunaan:** Menambahkan tab "Cost per Division" atau "Security Vulnerability Heatmap".

## 2. Cara Registrasi Plugin (Bootstrapping)

Setiap instance AetherOS akan membaca file `plugins.yaml` (atau proses *discovery* otomatis) saat *boot-up*. 

Sintaks registrasi di dalam kernel:
```python
# AetherOS Kernel Bootstrap (Contoh)
from aetheros.kernel import PluginLoader
from my_custom_plugin import LaravelAgent, ArtisanTool, GeminiProvider

loader = PluginLoader()

# Registrasi independen per kapabilitas
loader.register_agent(LaravelAgent)
loader.register_tool(ArtisanTool)
loader.register_provider(GeminiProvider)

loader.start()
```

## 3. Ekosistem Distribusi (Marketplace & Packs)

Berkat SDK yang sangat granular ini, komunitas dan vendor dapat memaketkan (bundle) kumpulan Plugin menjadi satu kesatuan yang disebut **Distribution Pack**.

Sebagai contoh, **Cyber Security Pack** mungkin berisi rilis bundling:
1. *Agent SDK:* `PentesterAgent`, `MalwareAnalystAgent`
2. *Tool SDK:* `NmapTool`, `MetasploitTool`
3. *Skill SDK:* `PerformDeepScanSkill`
4. *Dashboard SDK:* `VulnerabilityMapWidget`

Pengguna AetherOS dapat menginstal pack ini secara instan layaknya menginstal *apt-get* atau aplikasi di ekosistem Linux, mengubah *Software Company* biasa menjadi *Cyber Security Firm* secara mandiri.

---

🔗 **Selanjutnya:** [Referensi CLI AetherOS →](cli-reference.md)
