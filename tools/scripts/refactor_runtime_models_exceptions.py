import os
import shutil

# Move models
os.makedirs("runtime/src/aether_runtime/models/responses", exist_ok=True)
os.makedirs("runtime/src/aether_runtime/models/health", exist_ok=True)

shutil.move("runtime/src/aether_runtime/models/kernel.py", "runtime/src/aether_runtime/models/responses/kernel.py")
shutil.move("runtime/src/aether_runtime/models/execution.py", "runtime/src/aether_runtime/models/responses/execution.py")
shutil.move("runtime/src/aether_runtime/models/diagnostics.py", "runtime/src/aether_runtime/models/health/diagnostics.py")

# Create initial files for new structure
files = {
    "runtime/src/aether_runtime/models/responses/__init__.py": "",
    "runtime/src/aether_runtime/models/requests/__init__.py": "",
    "runtime/src/aether_runtime/models/events/__init__.py": "",
    "runtime/src/aether_runtime/models/health/__init__.py": "",
    "runtime/src/aether_runtime/models/metadata/__init__.py": "",
    "runtime/src/aether_runtime/models/metadata/manifest.py": """
from pydantic import BaseModel

class RuntimeManifest(BaseModel):
    runtime_version: str
    kernel_version: str
    contracts_version: str
    execution_version: str
    workspace_version: str
    compatibility: str
""",
    "runtime/src/aether_runtime/exceptions/__init__.py": "",
    "runtime/src/aether_runtime/exceptions/runtime.py": "class RuntimeException(Exception): pass",
    "runtime/src/aether_runtime/exceptions/validation.py": "class RuntimeValidationException(Exception): pass",
    "runtime/src/aether_runtime/exceptions/permission.py": "class RuntimePermissionException(Exception): pass",
}

for path, content in files.items():
    with open(path, "w") as f:
        f.write(content.strip() + "\n")

print("✅ Phase 1 refactoring completed.")
