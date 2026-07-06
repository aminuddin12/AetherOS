from ..models.responses.execution import ExecutionStatus

class ExecutionAdapter:
    @staticmethod
    def to_status_dto(raw_engine_obj) -> ExecutionStatus:
        return ExecutionStatus(
            engine="Execution Engine",
            threads=raw_engine_obj.get("threads", 8),
            queues=raw_engine_obj.get("queues", 2),
            status=raw_engine_obj.get("status", "idle")
        )
