import os

folders = [
    "interfaces",
    "core",
    "manifest",
    "lifecycle",
    "locking",
    "policy",
    "capabilities",
    "registry",
    "events",
    "bus",
    "extensions",
    "snapshot",
    "application/commands",
    "application/queries",
    "application/builders",
    "application/loaders",
    "application/inspectors"
]

readmes = {
    "interfaces": "Contracts for Dependency Injection. Modules here must only contain Protocols.",
    "core": "Workspace Aggregate Root and primary domain context. Must not depend on infrastructure.",
    "manifest": "Domain models for Manifest parsing, loading, and serializing.",
    "lifecycle": "State Machine for Workspace lifecycle.",
    "locking": "Advanced Workspace Lock Manager (Lease, TTL, Prioritization).",
    "policy": "Policy Engine for evaluating rules and constraints.",
    "capabilities": "Manager for deriving and validating Workspace Capabilities.",
    "registry": "Lightweight registry for ResourceReferences.",
    "events": "Event Sourcing ready EventStore, Dispatcher, and Projection.",
    "bus": "Internal Workspace Message Bus for publish/subscribe.",
    "extensions": "Extension Manager for Plugins, Hooks, and Middlewares.",
    "snapshot": "Stub API for Workspace snapshots (implemented in M3.3).",
    "application": "CQRS application layer replacing traditional 'services'."
}

base_dir = "workspace/src/aether_workspace"

for folder in folders:
    path = os.path.join(base_dir, folder)
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "__init__.py"), "w") as f:
        f.write("")
        
for folder, desc in readmes.items():
    path = os.path.join(base_dir, folder, "README.md")
    with open(path, "w") as f:
        f.write(f"# {folder.title()}\n\n{desc}\n")

print("✅ M3.0 Scaffolding completed.")
