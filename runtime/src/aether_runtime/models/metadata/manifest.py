from pydantic import BaseModel

class RuntimeManifest(BaseModel):
    runtime_version: str
    kernel_version: str
    contracts_version: str
    execution_version: str
    workspace_version: str
    compatibility: str
