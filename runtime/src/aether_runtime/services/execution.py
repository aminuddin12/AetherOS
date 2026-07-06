from ..adapters.execution import ExecutionAdapter

class ExecutionService:
    @staticmethod
    async def get_status():
        raw_engine = {"threads": 8, "queues": 2, "status": "idle"}
        return ExecutionAdapter.to_status_dto(raw_engine)
