from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class CommandContext:
    workspace_path: str
    user: str
    environment: str
    config: Dict[str, Any]
    output_format: str
    verbose: bool
