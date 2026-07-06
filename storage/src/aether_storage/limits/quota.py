from pydantic import BaseModel
from typing import Optional

class ResourceLimits(BaseModel):
    max_memory_bytes: Optional[int] = None
    max_objects: Optional[int] = None
    bandwidth_mbps: Optional[float] = None
    rate_limit_req_sec: Optional[int] = None
    timeout_sec: Optional[int] = None
    ttl_sec: Optional[int] = None
