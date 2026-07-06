# AetherOS

**Open Agent Operating System**

AetherOS bukanlah sekadar kerangka kerja (*framework*) untuk membuat *AI Agent*. AetherOS adalah sistem operasi berskala penuh yang dirancang dari nol untuk mensimulasikan dan menjalankan sebuah organisasi berbasis kecerdasan buatan (*Artificial Intelligence*).

Filosofi utama kami adalah:
> *"Build Organizations, not Agents."*

Alih-alih berfokus pada agen AI yang bekerja mandiri (seperti chatbot), AetherOS menyediakan infrastruktur sistem (*Kernel, Execution, Storage, Repository, Artifact, Workspace, Organization*) tempat para agen bekerja sebagai **bagian dari sebuah sistem sosial, birokrasi, dan kolaborasi**.

---

## 🏗 High-Level Architecture

Sistem ini disusun berdasarkan prinsip *Dependency Direction* (ADR-0025) murni secara *bottom-up*. Tidak ada runtime tingkat atas yang mengetahui atau menyimpan *state* internal dari runtime di bawahnya.

```text
               [ Company Brain ]
             (Knowledge Orchestrator)
                       │
       ┌───────────────┴────────────────┐
       │                                │
[ Organization Runtime ]     [ Constitution Runtime ]
(Operating Context)          (Rules & Compliance)
       │                                │
[ Workspace Application ]    [ Agent/Workflow Runtime ]
(CQRS & Pipelines)           (Cognition & Execution)
       │
   ┌───┴────┬───────────┬───────────┐
   │        │           │           │
[Workspace] [Storage] [Repository] [Artifact]
(Domain)   (Blobs)     (Graph)    (Semantic)
   │        │           │           │
   └────────┴───────────┴───────────┘
                       │
                 [ Runtime SDK ]
               (Universal Facade)
                       │
             [ Kernel & Execution ]
```

### Konsep Inti
- **Universal ResourceURI**: Seluruh interaksi lintas komponen diatur melalui `ResourceURI` (`workspace://...`, `artifact://...`, `storage://...`). 
- **Ownership Matrix (ADR-0024)**: Setiap lapis runtime hanya menyimpan dan mengelola data miliknya. *Repository* tidak menyimpan file, melainkan graf revisi. *Storage* menyimpan blob.
- **Company Brain (M4)**: Bukan sekadar model LLM, melainkan *Knowledge Orchestrator* yang mengonstruksi graf pengetahuan (*Subject-Predicate-Object*) berdasarkan abstraksi dari *Organization Layer*.

---

## 🚀 Quick Start (Coming Soon)

AetherOS sedang dalam tahap pembekuan fondasi arsitektur (M3.6). Rilis publik dengan instalasi pip sedang dipersiapkan untuk Milestone 9.

Untuk pengembangan lokal (*Development*):
```bash
git clone https://github.com/aminuddin12/AetherOS.git
cd AetherOS
uv sync
```

Menjalankan CLI:
```bash
uv run aether --help
```

Contoh penggunaan Runtime SDK (sebagai ilustrasi arsitektur masa depan):
```python
from aether_runtime.sdk import AetherRuntime

async def main():
    runtime = AetherRuntime()
    
    # Mencari identitas di dalam direktori
    members = await runtime.organization.directory.members()
    
    # Mengeksekusi komando pada workspace
    result = await runtime.workspace_app.execute(
        command="InitWorkspaceCommand",
        payload={"uri": "workspace://engineering/core"}
    )
```

---

## 🗺 Roadmap Status

AetherOS dikembangkan dalam milestone terukur yang bergeser dari sistem dasar (OS) hingga orkestrasi kognitif (Brain).

- ✅ **M1**: Kernel
- ✅ **M2**: Execution, CLI, Runtime SDK
- ✅ **M3.0–3.4**: Workspace & Application Runtime
- ✅ **M3.5**: Organization Runtime
- 🔄 **M3.6**: Documentation Freeze (Current)
- ⏳ **M4**: Company Brain
- ⏳ **M5**: Agent Runtime
- ⏳ **M6**: Provider Runtime
- ⏳ **M7**: Workflow Runtime
- ⏳ **M8**: Constitution Runtime
- ⏳ **M9**: Distribution Packs
- ⏳ **M10**: Aether Studio

---

## 🤝 Contribution & Governance

Pengembangan sistem AetherOS sangat ketat pada disiplin arsitektur. Sebelum berkontribusi, wajib membaca [Developer Guide](docs/id/getting-started/developer.md) dan memahami [Runtime Package Blueprint](docs/id/adr/ADR-0027-Runtime-Package-Blueprint.md).

## 📄 License
(TBD)
