from pydantic import BaseModel
from enum import Enum
from typing import List

class IdentityType(str, Enum):
    HUMAN = "human"
    AGENT = "agent"
    WORKER = "worker"
    PROVIDER = "provider"
    SERVICE_ACCOUNT = "service_account"
    ROBOT = "robot"
    AUTOMATION = "automation"
    EXTERNAL_IDENTITY = "external_identity"

class OrganizationMembership(BaseModel):
    member_id: str
    identity_type: IdentityType
    status: str
    roles: List[str]
