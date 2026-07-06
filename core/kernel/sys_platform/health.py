from enum import Enum
from typing import List, Dict
from .base import RuntimeDescriptor

class LifecycleState(str, Enum):
    CREATED = "Created"
    DISCOVERED = "Discovered"
    REGISTERED = "Registered"
    RESOLVED = "Resolved"
    INITIALIZED = "Initialized"
    STARTING = "Starting"
    RUNNING = "Running"
    READY = "Ready"
    STOPPING = "Stopping"
    STOPPED = "Stopped"
    SHUTDOWN = "Shutdown"

class HealthState(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"

class DependencyImpactEvaluator:
    @staticmethod
    def evaluate_derived_health(
        descriptor: RuntimeDescriptor,
        failed_dependencies: List[str],
        critical_requirements: List[str]
    ) -> HealthState:
        if not failed_dependencies:
            return HealthState.HEALTHY
            
        for dep in failed_dependencies:
            if dep in critical_requirements:
                return HealthState.FAILED
                
        return HealthState.DEGRADED
