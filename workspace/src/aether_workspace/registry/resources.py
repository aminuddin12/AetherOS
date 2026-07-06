from pydantic import BaseModel

class ResourceReference(BaseModel):
    id: str
    type: str
    uri: str

class ResourceRegistry:
    def __init__(self):
        self.resources: dict[str, ResourceReference] = {}
