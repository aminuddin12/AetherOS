from pydantic import BaseModel

class OrganizationIdentity(BaseModel):
    id: str
    name: str
    tenant_id: str
    status: str
    
class OrganizationContext(BaseModel):
    organization: OrganizationIdentity
    operating_mode: str
