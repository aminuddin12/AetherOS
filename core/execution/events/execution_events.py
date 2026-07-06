from pydantic import Field
from core.contracts.base import DomainEvent


class ExecutionStarted(DomainEvent):
    session_id: str = Field(...)
    executor_id: str = Field(...)


class ExecutionCompleted(DomainEvent):
    session_id: str = Field(...)
    duration_ms: float = Field(default=0.0)


class ExecutionFailed(DomainEvent):
    session_id: str = Field(...)
    reason: str = Field(...)


class ExecutionCancelled(DomainEvent):
    session_id: str = Field(...)
    reason: str = Field(default="")


class ExecutionTimedOut(DomainEvent):
    session_id: str = Field(...)
    timeout_seconds: float = Field(...)


class ExecutionRetried(DomainEvent):
    session_id: str = Field(...)
    attempt: int = Field(...)


class ExecutorAllocated(DomainEvent):
    session_id: str = Field(...)
    executor_id: str = Field(...)


class ExecutorReleased(DomainEvent):
    session_id: str = Field(...)
    executor_id: str = Field(...)
