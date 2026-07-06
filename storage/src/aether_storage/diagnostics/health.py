from pydantic import BaseModel
from typing import Dict

class StorageDiagnostics(BaseModel):
    health: str = "Healthy"
    statistics: Dict[str, int] = {}
    metrics: Dict[str, float] = {}
    capabilities: list = []
    mounted_providers: list = []
    transactions_active: int = 0
    cache_hits: int = 0
    quota_usage: float = 0.0
