<RULE[project]>
# GLOBAL SYSTEM DIRECTIVE: AI AUTONOMOUS EXECUTION & RELAY PROTOCOL

**TARGET:** All AI Agents (Gemini, Cursor, Windsurf, Copilot, Antigravity, etc.)
**MANDATE:** Immediate Execution. Zero Human Intervention. Continuous Flow.

---

## 1. CORE OPERATING PRINCIPLES

* **Zero-Question Policy:** Do not ask the user "what to do" or "how this works." All context, architecture, and business logic MUST be retrieved exclusively from the `/docs` directory.
* **Autonomous Confidence:** Execute decisions based on documentation without human approval.
* **Strict Source of Truth (Anti-Hallucination):** If technical details, credentials, or logic flows are missing from `/docs`, DO NOT guess or hallucinate code. You MUST halt execution immediately, do not write code, and output exactly:
`HALTED: Missing documentation in /docs/[topic]`.

## 2. ARCHITECTURAL & DEVELOPMENT STANDARDS

* **Atomic & Modular Execution:** System modifications must be modular. Resolve one component or route entirely, verify its functionality, log the status in the Task Contract, and only then proceed to the next. Minimize cognitive load by avoiding monolithic architectural rewrites in a single session.
* **Clean Code & Reusability:** Code must be clean, atomic, and highly recomposable. Reject dirty code and strictly avoid hardcoded elements.
* **UI/Frontend Strict Mandate:** Exclusively utilize standard native Nuxt UI components and Tailwind CSS utilities. The use of custom JSON-driven styling aliases or variant-driven UI systems is strictly prohibited and must be discarded.

## 3. BOOTSTRAP & STATE RETRIEVAL

Chat traces are volatile and subject to context-window limitations. State persistence relies entirely on physical files.

* **Phase 0 (IDE Rule Injection):** Read this mandate from root environment rules (`.cursorrules`, `.windsurfrules`, `.agents/AGENTS.md`, or `.github/copilot-instructions.md`).
* **Phase 0.5 (State Retrieval):** Before initiating any new task or reading `/docs` from scratch, you MUST check for the existence of `.ai/NEXT_TASK_STATE.md`. If this file exists and is populated, you are bound to resume execution precisely from the state defined within it.

## 4. STANDARDIZED HANDOVER & RELAY PROTOCOL (ESTAFET)

If you are approaching token/context limits, facing a timeout, or have completed a major milestone, you MUST trigger an autonomous interruption and perform a handover.

* **Clean Exit Rule:** Before pausing, ensure the codebase is not fundamentally broken. Ensure code compiles without fatal errors, and remove all unnecessary `console.log` statements or vague `TODO` comments.
* **State Serialization:** Write the exact current state to `.ai/NEXT_TASK_STATE.md` using the following strict schema:

```markdown
### RELAY STATE: [Insert Timestamp]

**1. COMPLETED TASK:**
- [Detail the exact function, component, or logic just finalized]

**2. CURRENT CONTEXT (Files Modified):**
- `path/to/file.ts` (Status: e.g., partially refactored, awaiting tests)

**3. NEXT EXACT STEP (Instruction for Next Agent):**
- [Specific, highly actionable command to continue the exact line of logic. Do not be vague.]
```

* **Version Control Fallback:** After writing the state file, execute an automated state save to ensure rollback capability (e.g., `git commit -am "chore(ai): auto-save relay state"`).
* **Termination Command:** Finally, terminate your current execution stream by outputting the standard relay command to the console:
`PAUSED: Estafet Task - Continue execution from .ai/NEXT_TASK_STATE.md`

## 5. GSD-CORE INTEGRATION MANDATE

* **Environment Context:** Perangkat utilitas dari repositori `[https://github.com/open-gsd/gsd-core.git](https://github.com/open-gsd/gsd-core.git)` telah terinstal secara penuh dan berstatus aktif di dalam *local environment*.
* **Execution Mandate:** Seluruh agen AI **WAJIB** memprioritaskan dan menggunakan *tools* dari `gsd-core` sebagai pilar utama untuk mendukung pengerjaan proyek, operasi sistem, eksekusi kode, atau manipulasi struktur direktori.
* **Prohibition of Redundancy:** Dilarang keras menulis skrip manual (*workarounds*) atau menggunakan metode konvensional untuk mengeksekusi tugas-tugas yang secara fungsional sudah dapat ditangani dengan lebih cepat dan standar oleh fitur-fitur bawaan dari `gsd-core`.

## 6. CONTAINERIZATION, QUALITY ASSURANCE, & SECURITY MANDATE

* **Container-Native Execution (Docker-First):** Apabila terdeteksi konfigurasi *container* (`Dockerfile`, `docker-compose.yml`), seluruh agen AI **WAJIB MUTLAK** menggunakannya untuk operasional (instalasi, *testing*, *database*). Dilarang keras mengeksekusi perintah *runtime native* di sistem lokal *host* kecuali diinstruksikan spesifik.
* **Deep Contextual Integrity & Zero-Surrender Policy:** Dilarang memberikan kode *placeholder* kosong atau *stub*. Jika kode gagal kompilasi atau tidak memenuhi standar, AI **DILARANG BERHENTI ATAU MENYERAH**. Wajib lakukan iterasi *debugging* otonom hingga sukses sempurna.
* **Strict Security & Latest Stable Tools:** AI **WAJIB** menggunakan versi stabil terbaru (*Latest Stable Release*) saat menginstal pustaka eksternal. AI juga harus memvalidasi kompatibilitas versi tersebut terhadap *tech stack* utama di *background* untuk menghindari konflik dependensi.
</RULE[project]>
