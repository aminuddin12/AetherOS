from typing import Dict
from pydantic import Field
from datetime import datetime, UTC
from ..base import ValueObject

class Measurement(ValueObject):
    """
    Nilai aktual pada titik waktu tertentu dari sebuah metrik.
    """
    metric_id: str = Field(..., description="Reference to the Metric entity")
    value: float = Field(..., description="The measured value")
    tags: Dict[str, str] = Field(default_factory=dict, description="Dimensions for aggregation")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC), description="When measured")
