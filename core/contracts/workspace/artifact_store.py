from pydantic import Field
from ..base import Entity, ContractProtocol


class Artifact(Entity):
    """
    File yang dihasilkan (diagram, gambar, laporan) dan bukan source code biasa.
    """

    workspace_id: str = Field(..., description="Workspace owning the artifact")
    filename: str = Field(..., description="Name of the file")
    mime_type: str = Field(..., description="E.g., image/png, text/markdown")
    storage_uri: str = Field(..., description="Path or S3 URI")


class ArtifactStore(ContractProtocol):
    """
    Antarmuka penyimpanan (Storage) untuk file artifact.
    """

    async def upload(self, file_data: bytes, metadata: Artifact) -> str: ...

    async def download(self, artifact_id: str) -> bytes: ...
