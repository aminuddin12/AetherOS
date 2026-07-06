from pydantic import BaseModel, Field


class KernelConfiguration(BaseModel):
    """
    Konfigurasi dan Feature Flags Kernel.
    """

    # Feature Flags
    enable_scheduler: bool = True
    enable_metrics: bool = True
    enable_diagnostics: bool = True
    enable_tracing: bool = False
    enable_supervisor: bool = True
    enable_pipeline: bool = True

    # Configurations
    default_queue_size: int = 1000
    dispatcher_timeout_ms: int = 5000
    supervisor_heartbeat_interval_sec: int = 30
