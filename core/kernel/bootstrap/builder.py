from core.kernel.dependency_injection import ServiceContainer
from core.kernel.manifest import KernelManifest
from .kernel import AetherKernel

class KernelBuilder:
    def __init__(self):
        self.container = ServiceContainer()
        self.manifest = KernelManifest()

    def configure_services(self, configurator) -> 'KernelBuilder':
        configurator(self.container)
        return self

    def build(self) -> AetherKernel:
        return AetherKernel(self.manifest, self.container)
