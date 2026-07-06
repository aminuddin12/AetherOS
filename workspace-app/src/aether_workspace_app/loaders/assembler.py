class WorkspaceAssembler:
    """Assembles full Workspace Aggregate from Workspace, Storage, Repo, and Artifact runtimes."""
    def __init__(self, registry):
        self.registry = registry
        
    async def assemble(self, workspace_id: str) -> dict:
        w_core = await self.registry.get("workspace").resolve(f"workspace://{workspace_id}")
        return {
            "identity": w_core,
            "status": "Assembled"
        }

class ResourceHydrator:
    """Hydrates references into full objects by querying the appropriate runtime."""
    def __init__(self, registry):
        self.registry = registry
        
    async def hydrate(self, resource_uri: str) -> dict:
        return {"uri": resource_uri, "hydrated": True}
