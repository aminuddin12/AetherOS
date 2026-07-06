from ..adapters.kernel import KernelAdapter

class KernelService:
    @staticmethod
    async def get_status():
        # Mock calling internal kernel
        raw_kernel = {"version": "1.0.0", "status": "running", "uptime": 3600.0}
        return KernelAdapter.to_status_dto(raw_kernel)

    @staticmethod
    async def get_services():
        raw_services = ["EventBus", "Scheduler", "StateManager"]
        return KernelAdapter.to_services_dto(raw_services)
