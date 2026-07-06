from pydantic import BaseModel
from typing import List

class DiagnosticItem(BaseModel):
    check: str
    status: str

class EnvironmentDiagnostics(BaseModel):
    results: List[DiagnosticItem]
