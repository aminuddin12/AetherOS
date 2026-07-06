from pydantic import BaseModel
from typing import List, Dict, Any

class AuditEvent(BaseModel):
    event_id: str
    action: str
    actor_id: str
    timestamp: str
    payload: Dict[str, Any]

class AuditEntry(BaseModel):
    entry_id: str
    event: AuditEvent
    hash: str

class AuditTrail(BaseModel):
    trail_id: str
    entries: List[AuditEntry]

class ComplianceRecord(BaseModel):
    record_id: str
    trail_id: str
    status: str
    
class Evidence(BaseModel):
    evidence_id: str
    record_id: str
    artifact_uri: str
