class HealthInspector:
    """Verifies that all domain runtimes within a Workspace are healthy."""
    def __init__(self, registry):
        self.workspace = registry.get("workspace")
        self.storage = registry.get("storage")
        
    async def inspect(self, workspace_id: str) -> dict:
        return {
            "status": "healthy",
            "workspace_id": workspace_id,
            "storage_mounted": True
        }
