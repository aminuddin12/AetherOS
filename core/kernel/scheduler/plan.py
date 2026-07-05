from typing import List
from pydantic import BaseModel
from core.contracts.task.task import Task
from core.contracts.base.reference import ResourceReference

class ExecutionPlan(BaseModel):
    task: Task
    assigned_worker_ref: ResourceReference | None = None
    steps: List[str] = []
