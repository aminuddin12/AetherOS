from pydantic import BaseModel
from typing import Dict, List

class ResourceReference(BaseModel):
    uri: str
    resource_type: str # e.g. "artifact", "storage", "agent"
    
class OrganizationResourceCatalog:
    """Cross-runtime global index holding ResourceURIs."""
    def __init__(self):
        self._resources: Dict[str, ResourceReference] = {}
        
    def register(self, resource_ref: ResourceReference) -> None:
        self._resources[resource_ref.uri] = resource_ref
        
    def search_by_type(self, resource_type: str) -> List[ResourceReference]:
        return [r for r in self._resources.values() if r.resource_type == resource_type]
