from typing import List, Dict
from pydantic import Field
from ..base import ValueObject
from .extension import Extension


class ExtensionManifest(ValueObject):
    """
    Deklarasi paket (Plugin/Distribution) yang mendaftarkan sekumpulan Extension.
    Memiliki mekanisme dependency management untuk Marketplace.
    """

    pack_name: str = Field(..., description="E.g., 'CyberSecurityPack'")
    version: str = Field(..., description="SemVer version")
    author: str = Field(..., description="Vendor/Author name")

    # Metadata Ekstensi
    dependencies: Dict[str, str] = Field(
        default_factory=dict, description="Required plugins and versions"
    )
    conflicts: List[str] = Field(
        default_factory=list, description="Plugins that cannot run together with this"
    )
    compatibility: List[str] = Field(
        default_factory=list, description="Supported AetherOS components"
    )
    minimum_kernel_version: str = Field(
        default="1.0.0", description="Minimum AetherOS version required"
    )

    extensions: List[Extension] = Field(default_factory=list, description="Provided components")
