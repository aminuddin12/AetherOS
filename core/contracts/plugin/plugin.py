from pydantic import Field
from ..base import AggregateRoot
from .extension_manifest import ExtensionManifest

class Plugin(AggregateRoot):
    """
    Entitas instalasi nyata dari sebuah Plugin/Pack di dalam tenant AetherOS.
    """
    manifest: ExtensionManifest = Field(..., description="The parsed manifest details")
    is_enabled: bool = Field(default=True, description="Whether this plugin is active")
    installed_by: str = Field(..., description="Identity ID of the installer")
