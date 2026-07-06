from pydantic import BaseModel
from typing import List

class CompositionProfile(BaseModel):
    model_config = {"frozen": True}
    
    profile_id: str
    name: str
    runtime_ids: List[str]

class RuntimeStack:
    def __init__(self, profile: CompositionProfile) -> None:
        self._profile = profile
        self._active_runtime_ids: List[str] = list(profile.runtime_ids)

    def get_profile_id(self) -> str:
        return self._profile.profile_id

    def list_stack_runtimes(self) -> List[str]:
        return self._active_runtime_ids
