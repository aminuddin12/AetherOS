from pydantic import BaseModel

class ExecutionStatus(BaseModel):
    engine: str
    threads: int
    queues: int
    status: str
