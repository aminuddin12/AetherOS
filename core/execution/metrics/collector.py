# AetherOS Metrics Collector
# Metrics collection and monitoring system

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
import time


@dataclass
class Metric:
    """Single metric data point."""
    name: str
    value: Any
    timestamp: float = field(default_factory=time.time)
    tags: Dict[str, str] = field(default_factory=dict)


class MetricsCollector:
    """Metrics collection and monitoring system."""

    def __init__(self):
        self._metrics: Dict[str, Metric] = {}
        self._enabled = True

    def collect(self, name: str, value: Any, tags: Optional[Dict[str, str]] = None) -> None:
        """Collect a metric."""
        if not self._enabled:
            return
            
        metric = Metric(
            name=name,
            value=value,
            tags=tags or {}
        )
        self._metrics[f"{name}_{metric.timestamp}"] = metric

    def get_metric(self, name: str) -> Optional[Metric]:
        """Get the latest metric by name."""
        # Find the most recent metric with this name
        matching_metrics = [
            m for m in self._metrics.values() 
            if m.name == name
        ]
        
        if not matching_metrics:
            return None
            
        return max(matching_metrics, key=lambda m: m.timestamp)

    def get_metrics(self, name: str) -> List[Metric]:
        """Get all metrics with the given name."""
        return [m for m in self._metrics.values() if m.name == name]

    def clear(self) -> None:
        """Clear all collected metrics."""
        self._metrics.clear()

    def enable(self) -> None:
        """Enable metrics collection."""
        self._enabled = True

    def disable(self) -> None:
        """Disable metrics collection."""
        self._enabled = False

    # Backward compatibility
    def record_execution(self, status: str, duration_ms: float = 0.0, retries: int = 0) -> None:
        """Backward compatible method for execution metrics."""
        self.collect("execution", 1, {"status": status, "type": "execution"})
        self.collect("execution_duration", duration_ms, {"status": status})
        self.collect("execution_retries", retries, {"status": status})

    def get_average_duration(self) -> float:
        """Get average execution duration."""
        metrics = self.get_metrics("execution_duration")
        if not metrics:
            return 0.0
        return sum(m.value for m in metrics) / len(metrics)

    def snapshot(self) -> Dict[str, int | float]:
        """Get snapshot of current metrics."""
        return {
            "execution_count": len(self.get_metrics("execution")),
            "average_duration": self.get_average_duration()
        }
        result = dict(self._counters)
        result["average_duration_ms"] = self.get_average_duration()
        return result
