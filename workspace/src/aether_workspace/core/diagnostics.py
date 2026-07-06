from pydantic import BaseModel
from typing import Dict, List

class WorkspaceDiagnostics(BaseModel):
    health: str = "Healthy"
    metrics: Dict[str, float] = {}
    statistics: Dict[str, int] = {}
    runtime_info: str = ""
    resource_usage: Dict[str, float] = {}
    version: str = "1.0.0"
    manifest_info: str = ""
