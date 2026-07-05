import os
import datetime

subsystems = [
    "bootstrap",
    "configuration",
    "context",
    "dependency_injection",
    "diagnostics",
    "dispatcher",
    "events",
    "internal",
    "lifecycle",
    "metrics",
    "permissions",
    "pipeline",
    "registry",
    "runtime",
    "scheduler",
    "state",
    "supervisor"
]

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content.strip() + "\n")

# 1. Create Subsystem READMEs
for sub in subsystems:
    readme_content = f"""
# {sub.replace('_', ' ').title()} Subsystem

## Purpose
(Jelaskan tujuan utama subsistem ini)

## Responsibilities
- (Daftar tanggung jawab)

## Public Interfaces
- (Daftar class/protocol publik yang terekspos)

## Dependencies
- (Modul atau kontrak yang dibutuhkan)

## Forbidden Dependencies
- (Modul yang dilarang diimpor)

## Lifecycle
- (Bagaimana subsistem ini hidup dan mati)

## Extension Points
- (Bagian yang bisa di-extend plugin)

## Future Implementation
- (Rencana masa depan)

## Examples
(Contoh penggunaan)
"""
    write_file(f"core/kernel/{sub}/README.md", readme_content)
    write_file(f"core/kernel/{sub}/__init__.py", "")

# 2. ADRs
adrs = {
    "0009-use-composite-registry.md": "Use Composite Registry to avoid God Object and enable modular registration.",
    "0010-use-constructor-injection.md": "Use Pure Python Constructor Injection to decouple dependencies without third-party heavy DI libraries.",
    "0011-runtime-does-not-own-pipeline.md": "Pipeline orchestrates the flow; Runtime is merely an executor middleware.",
    "0012-supervisor-controls-recovery-policy.md": "Dispatcher is pure Pub/Sub. Supervisor dictates retry/dead-letter policy.",
    "0013-use-feature-flags-in-kernel.md": "KernelConfiguration must include Feature Flags to toggle subsystems for testing and lightweight deployments."
}

for filename, desc in adrs.items():
    adr_content = f"""
# ADR: {filename.replace('.md', '').split('-', 1)[1].replace('-', ' ').title()}

## Status
Accepted

## Context
{desc}

## Decision
(Keputusan implementasi spesifik terkait {filename})

## Consequences
- Keuntungan: Mematuhi filosofi OS, loose coupling, highly testable.
- Kerugian: Kompleksitas awal dalam setup boilerplate.
"""
    write_file(f"docs/id/adr/{filename}", adr_content)

print("Scaffolding complete.")
