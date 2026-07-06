from typing import Protocol, List
from core.contracts.metrics.telemetry import TelemetryEvent


class MetricsExporter(Protocol):
    def export(self, events: List[TelemetryEvent]) -> None: ...


class NullExporter(MetricsExporter):
    def export(self, events: List[TelemetryEvent]) -> None:
        pass  # Discard
