from ..commands.models import InitWorkspaceCommand, RegisterArtifactCommand
from ..results.models import WorkspaceInitializationResult, ArtifactRegistrationResult

class InitWorkspaceCommandHandler:
    def __init__(self, registry):
        self.workspace = registry.get("workspace")
        self.storage = registry.get("storage")
        self.repository = registry.get("repository")

    async def handle(self, command: InitWorkspaceCommand) -> WorkspaceInitializationResult:
        # 1. Init Workspace Core
        w_uri = await self.workspace.create(command.workspace_name)
        # 2. Init Storage
        s_uri = await self.storage.mount(w_uri)
        # 3. Init Repository
        r_uri = await self.repository.initialize(s_uri)
        
        return WorkspaceInitializationResult(
            workspace_uri=w_uri,
            storage_uri=s_uri,
            repository_uri=r_uri,
            success=True
        )

class RegisterArtifactCommandHandler:
    def __init__(self, registry):
        self.artifact = registry.get("artifact")

    async def handle(self, command: RegisterArtifactCommand) -> ArtifactRegistrationResult:
        a_uri = await self.artifact.register(
            metadata=command.metadata,
            classification_id=command.classification_uri,
            storage_uri=f"storage://{command.context.workspace_id}/artifacts/new"
        )
        return ArtifactRegistrationResult(
            artifact_uri=a_uri,
            lineage_graph_updated=True,
            success=True
        )
