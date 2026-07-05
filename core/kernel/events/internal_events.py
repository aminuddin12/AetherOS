from pydantic import Field
from core.contracts.base import DomainEvent

class KernelStarted(DomainEvent): pass
class KernelStopped(DomainEvent): pass
class KernelBootstrapped(DomainEvent): pass

class WorkerRegistered(DomainEvent):
    worker_id: str = Field(...)
class WorkerUnregistered(DomainEvent):
    worker_id: str = Field(...)

class TaskScheduled(DomainEvent):
    task_id: str = Field(...)
class TaskCompleted(DomainEvent):
    task_id: str = Field(...)
class TaskFailed(DomainEvent):
    task_id: str = Field(...)
    reason: str = Field(...)

class PermissionDenied(DomainEvent):
    action: str = Field(...)
    resource: str = Field(...)
    actor: str = Field(...)

class PipelineStarted(DomainEvent):
    correlation_id: str = Field(...)
class PipelineCompleted(DomainEvent):
    correlation_id: str = Field(...)
