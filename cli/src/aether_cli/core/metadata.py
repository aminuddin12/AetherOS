from pydantic import BaseModel
from typing import List, Optional

class CommandMetadata(BaseModel):
    name: str
    description: str
    version: str = "1.0.0"
    experimental: bool = False
    deprecated: bool = False
    permissions: List[str] = []
