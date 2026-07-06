from core.kernel.manifest import KernelManifest
from core.kernel.dependency_injection import ServiceContainer


class AetherKernel:
    """Object OS yang sudah running"""

    def __init__(self, manifest: KernelManifest, container: ServiceContainer):
        self.manifest = manifest
        self.container = container

    async def shutdown(self):
        pass
