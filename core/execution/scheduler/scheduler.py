from core.execution.execution_plan import ExecutionPlan

class ExecutionScheduler:
    """
    Menghasilkan ExecutionPlan dari task metadata.
    Hanya planner — bukan executor.
    """
    def create_plan(
        self,
        task_id: str,
        priority: int = 0,
        strategy: str = "sequential",
    ) -> ExecutionPlan:
        return ExecutionPlan(
            task_id=task_id,
            priority=priority,
            strategy_name=strategy,
        )
