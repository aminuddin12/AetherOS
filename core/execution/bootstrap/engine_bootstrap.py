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
    """
    Orkestrator inisialisasi Execution Engine.
    Membangun semua komponen dan merangkainya.
    """
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
    """
    Instance Execution Engine yang sudah ter-bootstrap.
    """
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
