from .builder import KernelBuilder
from .kernel import AetherKernel


class KernelBootstrap:
    """
    Orkestrator utama dengan Pre, Main, dan Post phases.
    """

    @staticmethod
    def pre_bootstrap() -> KernelBuilder:
        return KernelBuilder()

    @staticmethod
    def bootstrap(builder: KernelBuilder) -> AetherKernel:
        return builder.build()

    @staticmethod
    def post_bootstrap(kernel: AetherKernel) -> None:
        # Load extensions/plugins here
        pass
