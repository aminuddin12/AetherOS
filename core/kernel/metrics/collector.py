from core.contracts.metrics.metric import TelemetryEvent
from .aggregator import MetricsAggregator
from .exporter import MetricsExporter

class MetricsCollector:
    def __init__(self, aggregator: MetricsAggregator, exporter: MetricsExporter):
        self.aggregator = aggregator
        self.exporter = exporter
        self.events_buffer = []

    def record(self, event: TelemetryEvent) -> None:
        self.events_buffer.append(event)
        # Flush if buffer full
        if len(self.events_buffer) > 100:
            self.exporter.export(self.events_buffer)
            self.events_buffer.clear()
