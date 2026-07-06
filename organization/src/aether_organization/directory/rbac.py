from pydantic import BaseModel
from typing import List, Dict

class Capability(BaseModel):
    name: str
    description: str

class Policy(BaseModel):
    policy_id: str
    effect: str # "allow" | "deny"
    capabilities: List[Capability]
    conditions: Dict[str, str]

class Permission(BaseModel):
    permission_id: str
    policies: List[Policy]

class Role(BaseModel):
    role_id: str
    name: str
    permissions: List[Permission]
