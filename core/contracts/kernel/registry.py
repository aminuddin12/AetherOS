from typing import Any, Type
from ..base import ContractProtocol


class ComponentRegistryProtocol(ContractProtocol):
    """
    Kontrak untuk mendaftarkan dan menemukan (discover) plugins, tools, provider, atau agen.
    """

    def register(self, name: str, component_class: Type[Any]) -> None: ...

    def resolve(self, name: str) -> Any: ...
