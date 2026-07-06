from pydantic import BaseModel
from typing import List

class KernelStatus(BaseModel):
    version: str
    status: str
    uptime: float

class KernelServices(BaseModel):
    services: List[str]
