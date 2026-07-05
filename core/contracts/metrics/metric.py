from enum import StrEnum
from pydantic import Field
from ..base import Entity

class MetricType(StrEnum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"

class Metric(Entity):
    """
    Definisi (metadata) dari suatu matriks yang akan diukur.
    """
    name: str = Field(..., description="Name of the metric (e.g., 'http_requests_total')")
    description: str = Field(..., description="Human readable description")
    metric_type: MetricType = Field(..., description="Type of metric")
    unit: str = Field(..., description="Unit of measurement (e.g., 'seconds', 'bytes')")
