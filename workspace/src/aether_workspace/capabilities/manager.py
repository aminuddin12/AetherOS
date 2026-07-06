from ..manifest.model import WorkspaceManifest
from typing import Dict, Any

class CapabilityManager:
    def derive_capabilities(self, manifest: WorkspaceManifest) -> Dict[str, bool]:
        base = {
            "supports_git": False,
            "supports_memory": False,
            "supports_company_brain": False
        }
        
        # Merge declared capabilities
        for cap, enabled in manifest.capabilities.items():
            base[cap] = enabled
            
        return base

capability_manager = CapabilityManager()
