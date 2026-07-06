from typing import List, Dict, Any
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime, UTC


class KernelManifest(BaseModel):
    """
    Identitas resmi dari AetherOS Kernel yang sedang berjalan.
    """

    kernel_uuid: UUID = Field(default_factory=uuid4)
    kernel_name: str = Field(default="AetherOS Core Kernel")
    kernel_version: str = Field(default="1.0.0-m1")

    supported_contract_version: str = Field(default="1.0")
    supported_api_version: str = Field(default="v1")
    supported_spec_version: str = Field(default="1.0")

    build_time: datetime = Field(default_factory=lambda: datetime.now(UTC))

    kernel_capabilities: List[str] = Field(
        default_factory=lambda: [
            "EventDispatch",
            "Metrics",
            "Scheduling",
            "Pipeline",
            "Supervisor",
            "RBAC",
        ]
    )
    metadata: Dict[str, Any] = Field(default_factory=dict)
