from core.contracts.task.task import Task
from .plan import ExecutionPlan

class KernelScheduler:
    """
    Hanya bertugas menghasilkan ExecutionPlan berdasarkan aturan antrian/prioritas.
    TIDAK mengeksekusi Task.
    """
    def generate_plan(self, task: Task) -> ExecutionPlan:
        # Mock logic for plan generation
        return ExecutionPlan(task=task)
