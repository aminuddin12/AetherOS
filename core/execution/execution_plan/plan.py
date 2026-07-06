from typing import List, Dict, Any
from pydantic import BaseModel, ConfigDict, Field

class ExecutionPlan(BaseModel):
    """
    Arahan eksekusi immutable yang dihasilkan Scheduler.
    Setelah dibuat, tidak boleh dimutasi. Perubahan menghasilkan plan baru.
    """
    model_config = ConfigDict(frozen=True)

    task_id: str = Field(...)
    priority: int = Field(default=0)
    strategy_name: str = Field(default="sequential")
    dependency_ids: List[str] = Field(default_factory=list)
    executor_requirements: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
