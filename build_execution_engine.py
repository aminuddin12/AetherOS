import os

def w(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content.strip() + "\n")

BASE = "core/execution"

# ═══════════════════════════════════════════════════
# 1. TOP-LEVEL README & __init__
# ═══════════════════════════════════════════════════

w(f"{BASE}/README.md", """
# Aether Execution Engine

## Purpose
Universal Execution Runtime untuk AetherOS. Menjalankan Task melalui Executor apapun (AI, Docker, Human, SSH, CLI, Browser, MCP) tanpa mengetahui implementasi spesifiknya.

## Responsibilities
- Mengelola lifecycle eksekusi (Session, Context, Plan, Result).
- Menyediakan SPI (Service Provider Interface) untuk Custom Executor.
- Mengorkestrasi middleware pipeline eksekusi.
- Mengelola Executor Pool (alokasi, release).
- Menerapkan Retry, Timeout, dan Cancellation policies.

## Public API
Semua class publik berada di `api/`.

## SPI
Semua interface yang dapat di-override berada di `spi/`.

## Dependencies
- `core/contracts/*` (read-only, API Freeze)
- `core/kernel/` public API only

## Forbidden Dependencies
- `core/kernel/internal/`
- Vendor libraries (openai, redis, sqlalchemy, fastapi, langgraph, openhands)
- Database drivers
- HTTP frameworks
""")

w(f"{BASE}/__init__.py", "")

# ═══════════════════════════════════════════════════
# 2. SPI — Service Provider Interfaces
# ═══════════════════════════════════════════════════

w(f"{BASE}/spi/__init__.py", """
from .executor import Executor
from .strategy import ExecutionStrategy
from .policy import ExecutionPolicy
from .middleware import ExecutionMiddleware
from .retry_policy import RetryPolicy
from .timeout_policy import TimeoutPolicy

__all__ = [
    "Executor",
    "ExecutionStrategy",
    "ExecutionPolicy",
    "ExecutionMiddleware",
    "RetryPolicy",
    "TimeoutPolicy",
]
""")

w(f"{BASE}/spi/README.md", """
# SPI (Service Provider Interface)

## Purpose
Mendefinisikan semua interface yang boleh diimplementasikan oleh pihak ketiga (plugin, distribution, custom executor).

## Responsibilities
- Menyediakan kontrak Executor universal.
- Menyediakan kontrak Strategy, Policy, dan Middleware.

## Public API
Semua class di package ini adalah public.

## Dependencies
- `core/contracts/base`

## Forbidden Dependencies
- Implementasi konkret apapun

## Extension Points
- Implementasikan `Executor` untuk jenis runtime baru.
- Implementasikan `ExecutionStrategy` untuk pola eksekusi baru.
- Implementasikan `RetryPolicy` / `TimeoutPolicy` untuk kebijakan kustom.
- Implementasikan `ExecutionMiddleware` untuk pipeline hook.
""")

w(f"{BASE}/spi/executor.py", """
from abc import ABC, abstractmethod
from typing import Any, Dict, List

class ExecutorCapability:
    def __init__(self, name: str, version: str = "1.0"):
        self.name = name
        self.version = version

class ExecutorHealth:
    def __init__(self, healthy: bool = True, message: str = "OK"):
        self.healthy = healthy
        self.message = message

class Executor(ABC):
    \"\"\"
    Universal Executor Interface.
    Semua jenis executor (AI, Docker, Human, SSH, CLI, Browser, MCP)
    harus mengimplementasikan interface ini.
    \"\"\"

    @abstractmethod
    async def execute(self, context: 'ExecutionContext', payload: Any) -> Any:
        \"\"\"Menjalankan payload dalam context yang diberikan.\"\"\"
        ...

    @abstractmethod
    async def validate(self, context: 'ExecutionContext', payload: Any) -> bool:
        \"\"\"Memvalidasi apakah executor dapat menjalankan payload ini.\"\"\"
        ...

    @abstractmethod
    async def cancel(self) -> None:
        \"\"\"Membatalkan eksekusi yang sedang berjalan.\"\"\"
        ...

    @abstractmethod
    async def shutdown(self) -> None:
        \"\"\"Membersihkan resource dan mematikan executor.\"\"\"
        ...

    @abstractmethod
    def health(self) -> ExecutorHealth:
        \"\"\"Melaporkan status kesehatan executor.\"\"\"
        ...

    @abstractmethod
    def capabilities(self) -> List[ExecutorCapability]:
        \"\"\"Mendeklarasikan kemampuan executor.\"\"\"
        ...
""")

w(f"{BASE}/spi/strategy.py", """
from abc import ABC, abstractmethod
from typing import Any, List

class ExecutionStrategy(ABC):
    \"\"\"
    Menentukan BAGAIMANA sekelompok unit kerja dieksekusi.
    Contoh: Sequential, Parallel, Batch, MapReduce.
    \"\"\"

    @abstractmethod
    async def execute(self, units: List[Any], executor_fn: Any) -> List[Any]:
        \"\"\"Menjalankan units menggunakan executor_fn sesuai strategi.\"\"\"
        ...
""")

w(f"{BASE}/spi/policy.py", """
from .retry_policy import RetryPolicy
from .timeout_policy import TimeoutPolicy

class ExecutionPolicy:
    \"\"\"
    Menggabungkan seluruh policy yang mengatur eksekusi.
    \"\"\"
    def __init__(
        self,
        retry: RetryPolicy | None = None,
        timeout: TimeoutPolicy | None = None,
    ):
        self.retry = retry or RetryPolicy()
        self.timeout = timeout or TimeoutPolicy()
""")

w(f"{BASE}/spi/retry_policy.py", """
class RetryPolicy:
    \"\"\"
    Aturan retry untuk eksekusi yang gagal.
    \"\"\"
    def __init__(
        self,
        max_retries: int = 3,
        delay_seconds: float = 1.0,
        backoff_multiplier: float = 2.0,
        retryable_exceptions: tuple = (Exception,),
    ):
        self.max_retries = max_retries
        self.delay_seconds = delay_seconds
        self.backoff_multiplier = backoff_multiplier
        self.retryable_exceptions = retryable_exceptions

    def should_retry(self, attempt: int, error: Exception) -> bool:
        if attempt >= self.max_retries:
            return False
        return isinstance(error, self.retryable_exceptions)

    def get_delay(self, attempt: int) -> float:
        return self.delay_seconds * (self.backoff_multiplier ** attempt)
""")

w(f"{BASE}/spi/timeout_policy.py", """
class TimeoutPolicy:
    \"\"\"
    Aturan timeout untuk eksekusi.
    \"\"\"
    def __init__(
        self,
        execution_timeout_seconds: float = 300.0,
        session_timeout_seconds: float = 3600.0,
    ):
        self.execution_timeout_seconds = execution_timeout_seconds
        self.session_timeout_seconds = session_timeout_seconds
""")

w(f"{BASE}/spi/middleware.py", """
from abc import ABC, abstractmethod
from typing import Any, Callable, Awaitable

NextMiddleware = Callable[['ExecutionContext', Any], Awaitable[Any]]

class ExecutionMiddleware(ABC):
    \"\"\"
    Middleware untuk Execution Pipeline.
    Setiap middleware dapat memproses, memodifikasi, atau menolak eksekusi
    sebelum meneruskannya ke middleware berikutnya.
    \"\"\"

    @abstractmethod
    async def invoke(self, context: Any, payload: Any, next_mw: NextMiddleware) -> Any:
        \"\"\"Memproses dan meneruskan ke middleware berikutnya.\"\"\"
        ...
""")

# ═══════════════════════════════════════════════════
# 3. INTERNAL — Private Implementation
# ═══════════════════════════════════════════════════

w(f"{BASE}/internal/__init__.py", """
from .exceptions import (
    ExecutionEngineError,
    ExecutorNotFoundError,
    ExecutorAllocationError,
    ExecutionTimeoutError,
    ExecutionCancelledError,
    ExecutionRetryExhaustedError,
    ExecutionValidationError,
)

__all__ = [
    "ExecutionEngineError",
    "ExecutorNotFoundError",
    "ExecutorAllocationError",
    "ExecutionTimeoutError",
    "ExecutionCancelledError",
    "ExecutionRetryExhaustedError",
    "ExecutionValidationError",
]
""")

w(f"{BASE}/internal/README.md", """
# Internal

## Purpose
Implementasi private yang TIDAK BOLEH digunakan oleh plugin atau komponen di luar `core/execution/`.

## Responsibilities
- Exceptions hierarchy.
- Helper utilities.

## Forbidden
- Tidak boleh diimpor dari luar `core/execution/`.
""")

w(f"{BASE}/internal/exceptions.py", """
class ExecutionEngineError(Exception):
    \"\"\"Root exception untuk Execution Engine.\"\"\"
    pass

class ExecutorNotFoundError(ExecutionEngineError):
    \"\"\"Tidak ada executor yang cocok ditemukan.\"\"\"
    pass

class ExecutorAllocationError(ExecutionEngineError):
    \"\"\"Gagal mengalokasikan executor dari pool.\"\"\"
    pass

class ExecutionTimeoutError(ExecutionEngineError):
    \"\"\"Eksekusi melebihi batas waktu.\"\"\"
    pass

class ExecutionCancelledError(ExecutionEngineError):
    \"\"\"Eksekusi dibatalkan.\"\"\"
    pass

class ExecutionRetryExhaustedError(ExecutionEngineError):
    \"\"\"Semua percobaan retry telah habis.\"\"\"
    pass

class ExecutionValidationError(ExecutionEngineError):
    \"\"\"Payload gagal validasi sebelum eksekusi.\"\"\"
    pass
""")

# ═══════════════════════════════════════════════════
# 4. EXECUTION CONTEXT
# ═══════════════════════════════════════════════════

w(f"{BASE}/execution_context/__init__.py", """
from .context import ExecutionContext

__all__ = ["ExecutionContext"]
""")

w(f"{BASE}/execution_context/README.md", """
# Execution Context

## Purpose
Context immutable yang diberikan kepada Executor saat eksekusi.

## Responsibilities
- Membawa informasi korelasi (correlation_id, trace_id).
- Membawa metadata dan konfigurasi eksekusi.
- Membawa cancellation token.

## Extension Points
- Tambahkan field metadata untuk kebutuhan custom executor.
""")

w(f"{BASE}/execution_context/context.py", """
from typing import Dict, Any
from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID, uuid4

class ExecutionContext(BaseModel):
    \"\"\"
    Context immutable yang diturunkan ke Executor.
    Berisi semua informasi yang dibutuhkan executor untuk menjalankan tugas.
    \"\"\"
    model_config = ConfigDict(frozen=True)

    context_id: UUID = Field(default_factory=uuid4)
    correlation_id: str = Field(...)
    trace_id: str = Field(...)
    parent_context_id: UUID | None = Field(default=None)
    tenant_id: str = Field(default="default")
    namespace: str = Field(default="default")
    metadata: Dict[str, Any] = Field(default_factory=dict)
""")

# ═══════════════════════════════════════════════════
# 5. EXECUTION SESSION
# ═══════════════════════════════════════════════════

w(f"{BASE}/execution_session/__init__.py", """
from .session import ExecutionSession, SessionStatus

__all__ = ["ExecutionSession", "SessionStatus"]
""")

w(f"{BASE}/execution_session/README.md", """
# Execution Session

## Purpose
Unit of Work wrapper untuk setiap eksekusi. Melacak timing, parent/child, dan status.

## Extension Points
- Nest sessions untuk sub-task execution.
""")

w(f"{BASE}/execution_session/session.py", """
from enum import StrEnum
from typing import List
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime, UTC

class SessionStatus(StrEnum):
    CREATED = "created"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"
    TIMED_OUT = "timed_out"

class ExecutionSession(BaseModel):
    \"\"\"
    Session runtime yang membungkus satu unit eksekusi.
    \"\"\"
    session_id: UUID = Field(default_factory=uuid4)
    parent_session_id: UUID | None = Field(default=None)
    child_session_ids: List[UUID] = Field(default_factory=list)
    status: SessionStatus = Field(default=SessionStatus.CREATED)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    started_at: datetime | None = Field(default=None)
    completed_at: datetime | None = Field(default=None)
    correlation_id: str = Field(default="")
""")

# ═══════════════════════════════════════════════════
# 6. EXECUTION PLAN
# ═══════════════════════════════════════════════════

w(f"{BASE}/execution_plan/__init__.py", """
from .plan import ExecutionPlan

__all__ = ["ExecutionPlan"]
""")

w(f"{BASE}/execution_plan/README.md", """
# Execution Plan

## Purpose
Rencana eksekusi immutable yang dihasilkan oleh Scheduler. Berisi task, prioritas, dependencies, dan strategy.

## Extension Points
- Custom planning logic via Scheduler SPI.
""")

w(f"{BASE}/execution_plan/plan.py", """
from typing import List, Dict, Any
from pydantic import BaseModel, ConfigDict, Field

class ExecutionPlan(BaseModel):
    \"\"\"
    Arahan eksekusi immutable yang dihasilkan Scheduler.
    Setelah dibuat, tidak boleh dimutasi. Perubahan menghasilkan plan baru.
    \"\"\"
    model_config = ConfigDict(frozen=True)

    task_id: str = Field(...)
    priority: int = Field(default=0)
    strategy_name: str = Field(default="sequential")
    dependency_ids: List[str] = Field(default_factory=list)
    executor_requirements: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
""")

# ═══════════════════════════════════════════════════
# 7. EXECUTION RESULT
# ═══════════════════════════════════════════════════

w(f"{BASE}/execution_result/__init__.py", """
from .result import ExecutionResult, ExecutionStatus

__all__ = ["ExecutionResult", "ExecutionStatus"]
""")

w(f"{BASE}/execution_result/README.md", """
# Execution Result

## Purpose
Hasil akhir dari sebuah eksekusi. Immutable.

## Extension Points
- Field `output` dan `metadata` bersifat generic untuk menampung hasil apapun.
""")

w(f"{BASE}/execution_result/result.py", """
from enum import StrEnum
from typing import Any, Dict
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, UTC

class ExecutionStatus(StrEnum):
    SUCCESS = "success"
    FAILURE = "failure"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"
    RETRY_EXHAUSTED = "retry_exhausted"

class ExecutionResult(BaseModel):
    \"\"\"
    Hasil eksekusi. Immutable setelah dibuat.
    \"\"\"
    model_config = ConfigDict(frozen=True)

    status: ExecutionStatus = Field(...)
    output: Any = Field(default=None)
    error: str | None = Field(default=None)
    duration_ms: float = Field(default=0.0)
    retry_count: int = Field(default=0)
    completed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    metadata: Dict[str, Any] = Field(default_factory=dict)
""")

# ═══════════════════════════════════════════════════
# 8. EXECUTION POLICY
# ═══════════════════════════════════════════════════

w(f"{BASE}/execution_policy/__init__.py", """
from .policy_manager import ExecutionPolicyManager

__all__ = ["ExecutionPolicyManager"]
""")

w(f"{BASE}/execution_policy/README.md", """
# Execution Policy

## Purpose
Mengelola dan menerapkan policy (Retry, Timeout, Cancellation, Priority) untuk eksekusi.

## Extension Points
- Custom RetryPolicy dan TimeoutPolicy via SPI.
""")

w(f"{BASE}/execution_policy/policy_manager.py", """
from core.execution.spi import ExecutionPolicy, RetryPolicy, TimeoutPolicy

class ExecutionPolicyManager:
    \"\"\"
    Menyimpan dan meresolve policy berdasarkan konteks eksekusi.
    \"\"\"
    def __init__(self, default_policy: ExecutionPolicy | None = None):
        self._default = default_policy or ExecutionPolicy()

    def get_policy(self, task_id: str | None = None) -> ExecutionPolicy:
        return self._default
""")

# ═══════════════════════════════════════════════════
# 9. EXECUTION STRATEGY
# ═══════════════════════════════════════════════════

w(f"{BASE}/execution_strategy/__init__.py", """
from .sequential import SequentialStrategy
from .parallel import ParallelStrategy
from .registry import StrategyRegistry

__all__ = ["SequentialStrategy", "ParallelStrategy", "StrategyRegistry"]
""")

w(f"{BASE}/execution_strategy/README.md", """
# Execution Strategy

## Purpose
Menentukan bagaimana sekelompok unit kerja dieksekusi (Sequential, Parallel, Batch).

## Extension Points
- Implementasikan `ExecutionStrategy` SPI untuk strategi kustom.
""")

w(f"{BASE}/execution_strategy/sequential.py", """
from typing import Any, List
from core.execution.spi import ExecutionStrategy

class SequentialStrategy(ExecutionStrategy):
    \"\"\"Menjalankan units satu per satu secara berurutan.\"\"\"

    async def execute(self, units: List[Any], executor_fn: Any) -> List[Any]:
        results = []
        for unit in units:
            result = await executor_fn(unit)
            results.append(result)
        return results
""")

w(f"{BASE}/execution_strategy/parallel.py", """
import asyncio
from typing import Any, List
from core.execution.spi import ExecutionStrategy

class ParallelStrategy(ExecutionStrategy):
    \"\"\"Menjalankan semua units secara paralel menggunakan asyncio.gather.\"\"\"

    async def execute(self, units: List[Any], executor_fn: Any) -> List[Any]:
        tasks = [executor_fn(unit) for unit in units]
        return list(await asyncio.gather(*tasks, return_exceptions=True))
""")

w(f"{BASE}/execution_strategy/registry.py", """
from typing import Dict
from core.execution.spi import ExecutionStrategy

class StrategyRegistry:
    \"\"\"Registry untuk mendaftarkan dan menemukan strategy berdasarkan nama.\"\"\"

    def __init__(self):
        self._strategies: Dict[str, ExecutionStrategy] = {}

    def register(self, name: str, strategy: ExecutionStrategy) -> None:
        self._strategies[name] = strategy

    def get(self, name: str) -> ExecutionStrategy | None:
        return self._strategies.get(name)
""")

# ═══════════════════════════════════════════════════
# 10. CANCELLATION
# ═══════════════════════════════════════════════════

w(f"{BASE}/cancellation/__init__.py", """
from .token import CancellationToken
from .source import CancellationTokenSource

__all__ = ["CancellationToken", "CancellationTokenSource"]
""")

w(f"{BASE}/cancellation/README.md", """
# Cancellation

## Purpose
Cooperative cancellation pattern (mirip .NET CancellationToken).

## Extension Points
- Executor wajib memeriksa token secara periodik.
""")

w(f"{BASE}/cancellation/token.py", """
import asyncio

class CancellationToken:
    \"\"\"
    Token cooperative cancellation (read-only view).
    Executor memeriksa token ini secara periodik.
    \"\"\"
    def __init__(self):
        self._event = asyncio.Event()
        self._reason: str = ""

    @property
    def is_cancelled(self) -> bool:
        return self._event.is_set()

    @property
    def reason(self) -> str:
        return self._reason

    async def wait_for_cancellation(self) -> None:
        await self._event.wait()
""")

w(f"{BASE}/cancellation/source.py", """
from .token import CancellationToken

class CancellationTokenSource:
    \"\"\"
    Sumber yang mengontrol CancellationToken.
    Hanya pemilik source yang boleh memicu cancel.
    \"\"\"
    def __init__(self):
        self._token = CancellationToken()

    @property
    def token(self) -> CancellationToken:
        return self._token

    def cancel(self, reason: str = "Cancellation requested") -> None:
        self._token._reason = reason
        self._token._event.set()
""")

# ═══════════════════════════════════════════════════
# 11. RETRY
# ═══════════════════════════════════════════════════

w(f"{BASE}/retry/__init__.py", """
from .handler import RetryHandler

__all__ = ["RetryHandler"]
""")

w(f"{BASE}/retry/README.md", """
# Retry

## Purpose
Menangani retry logic berdasarkan RetryPolicy SPI.

## Extension Points
- Custom RetryPolicy via SPI.
""")

w(f"{BASE}/retry/handler.py", """
import asyncio
from typing import Any, Callable, Awaitable
from core.execution.spi import RetryPolicy
from core.execution.internal import ExecutionRetryExhaustedError

class RetryHandler:
    \"\"\"
    Menjalankan callable dengan retry berdasarkan policy.
    \"\"\"
    def __init__(self, policy: RetryPolicy):
        self._policy = policy

    async def execute_with_retry(self, fn: Callable[..., Awaitable[Any]], *args: Any, **kwargs: Any) -> Any:
        last_error: Exception | None = None
        for attempt in range(self._policy.max_retries + 1):
            try:
                return await fn(*args, **kwargs)
            except Exception as e:
                last_error = e
                if not self._policy.should_retry(attempt, e):
                    break
                delay = self._policy.get_delay(attempt)
                await asyncio.sleep(delay)
        raise ExecutionRetryExhaustedError(f"All {self._policy.max_retries} retries exhausted: {last_error}")
""")

# ═══════════════════════════════════════════════════
# 12. TIMEOUT
# ═══════════════════════════════════════════════════

w(f"{BASE}/timeout/__init__.py", """
from .handler import TimeoutHandler

__all__ = ["TimeoutHandler"]
""")

w(f"{BASE}/timeout/README.md", """
# Timeout

## Purpose
Menerapkan batas waktu eksekusi berdasarkan TimeoutPolicy SPI.

## Extension Points
- Custom TimeoutPolicy via SPI.
""")

w(f"{BASE}/timeout/handler.py", """
import asyncio
from typing import Any, Callable, Awaitable
from core.execution.spi import TimeoutPolicy
from core.execution.internal import ExecutionTimeoutError

class TimeoutHandler:
    \"\"\"
    Menjalankan callable dengan batas waktu.
    \"\"\"
    def __init__(self, policy: TimeoutPolicy):
        self._policy = policy

    async def execute_with_timeout(self, fn: Callable[..., Awaitable[Any]], *args: Any, **kwargs: Any) -> Any:
        try:
            return await asyncio.wait_for(
                fn(*args, **kwargs),
                timeout=self._policy.execution_timeout_seconds
            )
        except asyncio.TimeoutError:
            raise ExecutionTimeoutError(
                f"Execution exceeded {self._policy.execution_timeout_seconds}s timeout"
            )
""")

# ═══════════════════════════════════════════════════
# 13. EXECUTOR POOL
# ═══════════════════════════════════════════════════

w(f"{BASE}/executor_pool/__init__.py", """
from .pool import ExecutorPool

__all__ = ["ExecutorPool"]
""")

w(f"{BASE}/executor_pool/README.md", """
# Executor Pool

## Purpose
Mengelola kumpulan Executor instances. Mendukung Register, Unregister, Lookup, Allocate, Release.

## Extension Points
- Future: Distributed pool, weighted allocation, sticky sessions.
""")

w(f"{BASE}/executor_pool/pool.py", """
from typing import Dict, List, Any
from core.execution.spi import Executor
from core.execution.internal import ExecutorNotFoundError, ExecutorAllocationError

class ExecutorPool:
    \"\"\"
    Pool pengelola Executor instances.
    \"\"\"
    def __init__(self):
        self._executors: Dict[str, Executor] = {}
        self._allocated: Dict[str, str] = {}

    def register(self, executor_id: str, executor: Executor) -> None:
        self._executors[executor_id] = executor

    def unregister(self, executor_id: str) -> None:
        self._executors.pop(executor_id, None)
        self._allocated = {k: v for k, v in self._allocated.items() if v != executor_id}

    def lookup(self, executor_id: str) -> Executor:
        executor = self._executors.get(executor_id)
        if not executor:
            raise ExecutorNotFoundError(f"Executor '{executor_id}' not found in pool")
        return executor

    def allocate(self, session_id: str, executor_id: str | None = None) -> Executor:
        if executor_id:
            executor = self.lookup(executor_id)
            self._allocated[session_id] = executor_id
            return executor
        for eid, ex in self._executors.items():
            if eid not in self._allocated.values():
                self._allocated[session_id] = eid
                return ex
        raise ExecutorAllocationError("No available executors in pool")

    def release(self, session_id: str) -> None:
        self._allocated.pop(session_id, None)

    def list_available(self) -> List[str]:
        allocated_ids = set(self._allocated.values())
        return [eid for eid in self._executors if eid not in allocated_ids]
""")

# ═══════════════════════════════════════════════════
# 14. LIFECYCLE
# ═══════════════════════════════════════════════════

w(f"{BASE}/lifecycle/__init__.py", """
from .execution_lifecycle import ExecutionLifecycle, ExecutionState

__all__ = ["ExecutionLifecycle", "ExecutionState"]
""")

w(f"{BASE}/lifecycle/README.md", """
# Lifecycle

## Purpose
Mengelola transisi status eksekusi (Created → Queued → Running → Completed/Cancelled/Failed/TimedOut).

## Extension Points
- Custom transition validation rules.
""")

w(f"{BASE}/lifecycle/execution_lifecycle.py", """
from enum import StrEnum

class ExecutionState(StrEnum):
    CREATED = "created"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"
    TIMED_OUT = "timed_out"

VALID_TRANSITIONS = {
    ExecutionState.CREATED: {ExecutionState.QUEUED, ExecutionState.CANCELLED},
    ExecutionState.QUEUED: {ExecutionState.RUNNING, ExecutionState.CANCELLED},
    ExecutionState.RUNNING: {ExecutionState.COMPLETED, ExecutionState.FAILED, ExecutionState.CANCELLED, ExecutionState.TIMED_OUT},
    ExecutionState.COMPLETED: set(),
    ExecutionState.CANCELLED: set(),
    ExecutionState.FAILED: set(),
    ExecutionState.TIMED_OUT: set(),
}

class ExecutionLifecycle:
    \"\"\"
    Mengelola dan memvalidasi transisi status eksekusi.
    \"\"\"
    def __init__(self):
        self._state = ExecutionState.CREATED

    @property
    def state(self) -> ExecutionState:
        return self._state

    def transition_to(self, new_state: ExecutionState) -> bool:
        if new_state in VALID_TRANSITIONS.get(self._state, set()):
            self._state = new_state
            return True
        return False
""")

# ═══════════════════════════════════════════════════
# 15. STATE
# ═══════════════════════════════════════════════════

w(f"{BASE}/state/__init__.py", """
from .manager import ExecutionStateManager

__all__ = ["ExecutionStateManager"]
""")

w(f"{BASE}/state/README.md", """
# State

## Purpose
Mengelola mutable state untuk Execution dan Session.

## Extension Points
- Future: Persistent state store (Redis, PostgreSQL).
""")

w(f"{BASE}/state/manager.py", """
from typing import Dict, Any
from core.execution.execution_session import ExecutionSession

class ExecutionStateManager:
    \"\"\"
    State Manager khusus Execution Engine.
    Satu-satunya tempat mutable state boleh hidup.
    \"\"\"
    def __init__(self):
        self._sessions: Dict[str, ExecutionSession] = {}
        self._execution_data: Dict[str, Any] = {}

    def store_session(self, session_id: str, session: ExecutionSession) -> None:
        self._sessions[session_id] = session

    def get_session(self, session_id: str) -> ExecutionSession | None:
        return self._sessions.get(session_id)

    def update_execution_data(self, session_id: str, data: Any) -> None:
        self._execution_data[session_id] = data

    def get_execution_data(self, session_id: str) -> Any:
        return self._execution_data.get(session_id)
""")

# ═══════════════════════════════════════════════════
# 16. METRICS
# ═══════════════════════════════════════════════════

w(f"{BASE}/metrics/__init__.py", """
from .collector import ExecutionMetricsCollector

__all__ = ["ExecutionMetricsCollector"]
""")

w(f"{BASE}/metrics/README.md", """
# Metrics

## Purpose
Mengumpulkan dan mengagregasi metrik eksekusi (count, success, failure, timeout, retry, duration).

## Extension Points
- Future: Export ke OpenTelemetry via Kernel Metrics Exporter.
""")

w(f"{BASE}/metrics/collector.py", """
from typing import Dict
import time

class ExecutionMetricsCollector:
    \"\"\"
    In-memory metrics collector untuk Execution Engine.
    \"\"\"
    def __init__(self):
        self._counters: Dict[str, int] = {
            "execution_count": 0,
            "success_count": 0,
            "failure_count": 0,
            "timeout_count": 0,
            "retry_count": 0,
            "cancelled_count": 0,
        }
        self._durations: list[float] = []

    def record_execution(self, status: str, duration_ms: float = 0.0, retries: int = 0) -> None:
        self._counters["execution_count"] += 1
        self._counters["retry_count"] += retries
        self._durations.append(duration_ms)
        if status == "success":
            self._counters["success_count"] += 1
        elif status == "failure":
            self._counters["failure_count"] += 1
        elif status == "timeout":
            self._counters["timeout_count"] += 1
        elif status == "cancelled":
            self._counters["cancelled_count"] += 1

    def get_average_duration(self) -> float:
        if not self._durations:
            return 0.0
        return sum(self._durations) / len(self._durations)

    def snapshot(self) -> Dict[str, int | float]:
        result = dict(self._counters)
        result["average_duration_ms"] = self.get_average_duration()
        return result
""")

# ═══════════════════════════════════════════════════
# 17. DIAGNOSTICS
# ═══════════════════════════════════════════════════

w(f"{BASE}/diagnostics/__init__.py", """
from .report import ExecutionDiagnostics

__all__ = ["ExecutionDiagnostics"]
""")

w(f"{BASE}/diagnostics/README.md", """
# Diagnostics

## Purpose
Menyediakan laporan status Execution Engine, Executor Pool, dan Pipeline.

## Extension Points
- Future: Real-time streaming diagnostics.
""")

w(f"{BASE}/diagnostics/report.py", """
from typing import Dict, Any
from core.execution.executor_pool import ExecutorPool
from core.execution.metrics import ExecutionMetricsCollector

class ExecutionDiagnostics:
    \"\"\"
    Menghasilkan laporan diagnostik Execution Engine.
    \"\"\"
    def __init__(self, pool: ExecutorPool, metrics: ExecutionMetricsCollector):
        self._pool = pool
        self._metrics = metrics

    def report(self) -> Dict[str, Any]:
        return {
            "available_executors": self._pool.list_available(),
            "metrics": self._metrics.snapshot(),
        }
""")

# ═══════════════════════════════════════════════════
# 18. EVENTS
# ═══════════════════════════════════════════════════

w(f"{BASE}/events/__init__.py", """
from .execution_events import (
    ExecutionStarted,
    ExecutionCompleted,
    ExecutionFailed,
    ExecutionCancelled,
    ExecutionTimedOut,
    ExecutionRetried,
    ExecutorAllocated,
    ExecutorReleased,
)

__all__ = [
    "ExecutionStarted", "ExecutionCompleted", "ExecutionFailed",
    "ExecutionCancelled", "ExecutionTimedOut", "ExecutionRetried",
    "ExecutorAllocated", "ExecutorReleased",
]
""")

w(f"{BASE}/events/README.md", """
# Events

## Purpose
Domain events internal Execution Engine. Digunakan oleh Metrics, Diagnostics, dan Supervisor.

## Extension Points
- Subscribe ke event ini dari plugin via Kernel EventBus.
""")

w(f"{BASE}/events/execution_events.py", """
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
""")

# ═══════════════════════════════════════════════════
# 19. EXECUTION HISTORY
# ═══════════════════════════════════════════════════

w(f"{BASE}/execution_history/__init__.py", """
from .store import ExecutionHistoryStore

__all__ = ["ExecutionHistoryStore"]
""")

w(f"{BASE}/execution_history/README.md", """
# Execution History

## Purpose
In-memory log dari eksekusi yang telah selesai. Future: persistent store.

## Extension Points
- Swap ke database-backed store.
""")

w(f"{BASE}/execution_history/store.py", """
from typing import List, Dict
from core.execution.execution_result import ExecutionResult

class ExecutionHistoryStore:
    \"\"\"
    In-memory store untuk riwayat eksekusi.
    \"\"\"
    def __init__(self, max_entries: int = 10000):
        self._history: Dict[str, ExecutionResult] = {}
        self._max = max_entries

    def record(self, session_id: str, result: ExecutionResult) -> None:
        if len(self._history) >= self._max:
            oldest_key = next(iter(self._history))
            del self._history[oldest_key]
        self._history[session_id] = result

    def get(self, session_id: str) -> ExecutionResult | None:
        return self._history.get(session_id)

    def list_recent(self, limit: int = 50) -> List[ExecutionResult]:
        return list(self._history.values())[-limit:]
""")

# ═══════════════════════════════════════════════════
# 20. RESOURCE MANAGER
# ═══════════════════════════════════════════════════

w(f"{BASE}/resource_manager/__init__.py", """
from .manager import ResourceManager

__all__ = ["ResourceManager"]
""")

w(f"{BASE}/resource_manager/README.md", """
# Resource Manager

## Purpose
Mengelola Execution Resources (thread slots, memory budget). Saat ini in-memory.

## Extension Points
- Future: Distributed resource allocation (Kubernetes, Nomad).
""")

w(f"{BASE}/resource_manager/manager.py", """
from typing import Dict

class ResourceManager:
    \"\"\"
    In-memory resource manager untuk mengatur slot eksekusi.
    \"\"\"
    def __init__(self, max_concurrent: int = 10):
        self._max = max_concurrent
        self._allocated: Dict[str, bool] = {}

    @property
    def available_slots(self) -> int:
        return self._max - len(self._allocated)

    def acquire(self, session_id: str) -> bool:
        if self.available_slots <= 0:
            return False
        self._allocated[session_id] = True
        return True

    def release(self, session_id: str) -> None:
        self._allocated.pop(session_id, None)
""")

# ═══════════════════════════════════════════════════
# 21. SCHEDULER
# ═══════════════════════════════════════════════════

w(f"{BASE}/scheduler/__init__.py", """
from .scheduler import ExecutionScheduler

__all__ = ["ExecutionScheduler"]
""")

w(f"{BASE}/scheduler/README.md", """
# Scheduler

## Purpose
Menghasilkan ExecutionPlan dari Task. Tidak mengeksekusi.

## Extension Points
- Custom scheduling strategies.
""")

w(f"{BASE}/scheduler/scheduler.py", """
from core.execution.execution_plan import ExecutionPlan

class ExecutionScheduler:
    \"\"\"
    Menghasilkan ExecutionPlan dari task metadata.
    Hanya planner — bukan executor.
    \"\"\"
    def create_plan(
        self,
        task_id: str,
        priority: int = 0,
        strategy: str = "sequential",
    ) -> ExecutionPlan:
        return ExecutionPlan(
            task_id=task_id,
            priority=priority,
            strategy_name=strategy,
        )
""")

# ═══════════════════════════════════════════════════
# 22. MIDDLEWARE
# ═══════════════════════════════════════════════════

w(f"{BASE}/middleware/__init__.py", """
from .validation import ValidationMiddleware
from .metrics_mw import MetricsMiddleware
from .logging_mw import LoggingMiddleware

__all__ = ["ValidationMiddleware", "MetricsMiddleware", "LoggingMiddleware"]
""")

w(f"{BASE}/middleware/README.md", """
# Middleware

## Purpose
Built-in middleware untuk Execution Pipeline.

## Extension Points
- Implementasikan `ExecutionMiddleware` SPI untuk menambahkan middleware kustom.
""")

w(f"{BASE}/middleware/validation.py", """
from typing import Any, Callable, Awaitable
from core.execution.spi import ExecutionMiddleware
from core.execution.internal import ExecutionValidationError

class ValidationMiddleware(ExecutionMiddleware):
    \"\"\"Memvalidasi bahwa payload tidak kosong sebelum meneruskan.\"\"\"

    async def invoke(self, context: Any, payload: Any, next_mw: Callable) -> Any:
        if payload is None:
            raise ExecutionValidationError("Payload cannot be None")
        return await next_mw(context, payload)
""")

w(f"{BASE}/middleware/metrics_mw.py", """
import time
from typing import Any, Callable
from core.execution.spi import ExecutionMiddleware
from core.execution.metrics import ExecutionMetricsCollector

class MetricsMiddleware(ExecutionMiddleware):
    \"\"\"Merekam durasi dan status eksekusi.\"\"\"

    def __init__(self, collector: ExecutionMetricsCollector):
        self._collector = collector

    async def invoke(self, context: Any, payload: Any, next_mw: Callable) -> Any:
        start = time.monotonic()
        try:
            result = await next_mw(context, payload)
            duration = (time.monotonic() - start) * 1000
            self._collector.record_execution("success", duration)
            return result
        except Exception as e:
            duration = (time.monotonic() - start) * 1000
            self._collector.record_execution("failure", duration)
            raise
""")

w(f"{BASE}/middleware/logging_mw.py", """
import logging
from typing import Any, Callable
from core.execution.spi import ExecutionMiddleware

logger = logging.getLogger("aether.execution")

class LoggingMiddleware(ExecutionMiddleware):
    \"\"\"Logging middleware untuk observability.\"\"\"

    async def invoke(self, context: Any, payload: Any, next_mw: Callable) -> Any:
        logger.info("Execution started")
        try:
            result = await next_mw(context, payload)
            logger.info("Execution completed successfully")
            return result
        except Exception as e:
            logger.error(f"Execution failed: {e}")
            raise
""")

# ═══════════════════════════════════════════════════
# 23. PIPELINE
# ═══════════════════════════════════════════════════

w(f"{BASE}/pipeline/__init__.py", """
from .pipeline import ExecutionPipeline

__all__ = ["ExecutionPipeline"]
""")

w(f"{BASE}/pipeline/README.md", """
# Pipeline

## Purpose
Middleware-based execution pipeline. Validation → Scheduling → Allocation → Execution → Metrics → Completion.

## Extension Points
- Tambahkan middleware via `pipeline.use(middleware)`.
""")

w(f"{BASE}/pipeline/pipeline.py", """
from typing import List, Any
from core.execution.spi import ExecutionMiddleware

class ExecutionPipeline:
    \"\"\"
    Middleware-based execution pipeline.
    Merangkai middleware secara berurutan dengan pola chain-of-responsibility.
    \"\"\"
    def __init__(self):
        self._middlewares: List[ExecutionMiddleware] = []

    def use(self, middleware: ExecutionMiddleware) -> 'ExecutionPipeline':
        self._middlewares.append(middleware)
        return self

    async def execute(self, context: Any, payload: Any) -> Any:
        async def terminal(ctx: Any, pl: Any) -> Any:
            return pl

        chain = terminal
        for mw in reversed(self._middlewares):
            current_mw = mw
            previous_chain = chain
            async def make_next(ctx: Any, pl: Any, _mw=current_mw, _prev=previous_chain) -> Any:
                return await _mw.invoke(ctx, pl, _prev)
            chain = make_next

        return await chain(context, payload)
""")

# ═══════════════════════════════════════════════════
# 24. SERVICES
# ═══════════════════════════════════════════════════

w(f"{BASE}/services/__init__.py", "")

w(f"{BASE}/services/README.md", """
# Services

## Purpose
Internal service layer untuk Execution Engine. Berisi orchestration services.

## Forbidden Dependencies
- Tidak boleh diakses dari luar `core/execution/`.
""")

# ═══════════════════════════════════════════════════
# 25. CONTEXT (Top-level alias)
# ═══════════════════════════════════════════════════

w(f"{BASE}/context/__init__.py", """
from core.execution.execution_context import ExecutionContext

__all__ = ["ExecutionContext"]
""")

w(f"{BASE}/context/README.md", """
# Context

## Purpose
Re-export dari execution_context untuk backward compatibility dan konvensi package.
""")

# ═══════════════════════════════════════════════════
# 26. BOOTSTRAP
# ═══════════════════════════════════════════════════

w(f"{BASE}/bootstrap/__init__.py", """
from .engine_bootstrap import ExecutionEngineBootstrap

__all__ = ["ExecutionEngineBootstrap"]
""")

w(f"{BASE}/bootstrap/README.md", """
# Bootstrap

## Purpose
Inisialisasi seluruh komponen Execution Engine.

## Extension Points
- Hook untuk plugin registration pasca-bootstrap.
""")

w(f"{BASE}/bootstrap/engine_bootstrap.py", """
from core.execution.executor_pool import ExecutorPool
from core.execution.metrics import ExecutionMetricsCollector
from core.execution.diagnostics import ExecutionDiagnostics
from core.execution.state import ExecutionStateManager
from core.execution.execution_policy import ExecutionPolicyManager
from core.execution.execution_strategy import SequentialStrategy, ParallelStrategy, StrategyRegistry
from core.execution.pipeline import ExecutionPipeline
from core.execution.middleware import ValidationMiddleware, MetricsMiddleware, LoggingMiddleware
from core.execution.resource_manager import ResourceManager
from core.execution.execution_history import ExecutionHistoryStore
from core.execution.scheduler import ExecutionScheduler

class ExecutionEngineBootstrap:
    \"\"\"
    Orkestrator inisialisasi Execution Engine.
    Membangun semua komponen dan merangkainya.
    \"\"\"
    @staticmethod
    def initialize() -> 'ExecutionEngineInstance':
        pool = ExecutorPool()
        metrics = ExecutionMetricsCollector()
        diagnostics = ExecutionDiagnostics(pool, metrics)
        state = ExecutionStateManager()
        policy = ExecutionPolicyManager()
        resource = ResourceManager()
        history = ExecutionHistoryStore()
        scheduler = ExecutionScheduler()

        strategy_registry = StrategyRegistry()
        strategy_registry.register("sequential", SequentialStrategy())
        strategy_registry.register("parallel", ParallelStrategy())

        pipeline = ExecutionPipeline()
        pipeline.use(LoggingMiddleware())
        pipeline.use(ValidationMiddleware())
        pipeline.use(MetricsMiddleware(metrics))

        return ExecutionEngineInstance(
            pool=pool,
            metrics=metrics,
            diagnostics=diagnostics,
            state=state,
            policy=policy,
            resource=resource,
            history=history,
            scheduler=scheduler,
            strategy_registry=strategy_registry,
            pipeline=pipeline,
        )

class ExecutionEngineInstance:
    \"\"\"
    Instance Execution Engine yang sudah ter-bootstrap.
    \"\"\"
    def __init__(
        self,
        pool: ExecutorPool,
        metrics: ExecutionMetricsCollector,
        diagnostics: ExecutionDiagnostics,
        state: ExecutionStateManager,
        policy: ExecutionPolicyManager,
        resource: ResourceManager,
        history: ExecutionHistoryStore,
        scheduler: ExecutionScheduler,
        strategy_registry: StrategyRegistry,
        pipeline: ExecutionPipeline,
    ):
        self.pool = pool
        self.metrics = metrics
        self.diagnostics = diagnostics
        self.state = state
        self.policy = policy
        self.resource = resource
        self.history = history
        self.scheduler = scheduler
        self.strategy_registry = strategy_registry
        self.pipeline = pipeline
""")

# ═══════════════════════════════════════════════════
# 27. API — Public Facade
# ═══════════════════════════════════════════════════

w(f"{BASE}/api/__init__.py", """
from core.execution.execution_context import ExecutionContext
from core.execution.execution_session import ExecutionSession, SessionStatus
from core.execution.execution_plan import ExecutionPlan
from core.execution.execution_result import ExecutionResult, ExecutionStatus
from core.execution.diagnostics import ExecutionDiagnostics
from core.execution.bootstrap import ExecutionEngineBootstrap

__all__ = [
    "ExecutionContext",
    "ExecutionSession",
    "SessionStatus",
    "ExecutionPlan",
    "ExecutionResult",
    "ExecutionStatus",
    "ExecutionDiagnostics",
    "ExecutionEngineBootstrap",
]
""")

w(f"{BASE}/api/README.md", """
# API (Public)

## Purpose
Semua class yang boleh digunakan oleh subsystem lain (Kernel, Plugin, Provider, Distribution).

## Responsibilities
- Re-export public-facing types.

## Forbidden
- Jangan mengekspos internal implementation detail.
""")

print("Execution Engine implementation complete.")
