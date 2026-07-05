from typing import List
from pydantic import Field
from ..base import ValueObject
from .extension import Extension

class ExtensionManifest(ValueObject):
    """
    Deklarasi paket yang mendaftarkan sekumpulan Extension.
    """
    pack_name: str = Field(..., description="E.g., 'CyberSecurityPack'")
    version: str = Field(..., description="SemVer version")
    author: str = Field(..., description="Vendor/Author name")
    extensions: List[Extension] = Field(default_factory=list, description="Provided components")
