from ..models.responses.kernel import KernelStatus, KernelServices

class KernelAdapter:
    @staticmethod
    def to_status_dto(raw_kernel_obj) -> KernelStatus:
        # Translates internal core.kernel objects to DTO
        return KernelStatus(
            version=raw_kernel_obj.get("version", "1.0.0"),
            status=raw_kernel_obj.get("status", "running"),
            uptime=raw_kernel_obj.get("uptime", 3600.0)
        )

    @staticmethod
    def to_services_dto(raw_services_list) -> KernelServices:
        return KernelServices(services=raw_services_list)
