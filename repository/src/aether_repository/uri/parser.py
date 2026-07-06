from aether_storage.uri.resource_uri import ResourceURI
from typing import Optional

class RepositoryURIParser:
    """Specialized parser for repository:// URIs."""
    @staticmethod
    def extract_repository_name(uri: ResourceURI) -> str:
        return uri.authority

    @staticmethod
    def extract_revision_alias(uri: ResourceURI) -> Optional[str]:
        # Example: repository://backend/revisions/HEAD
        parts = uri.path.strip('/').split('/')
        if len(parts) >= 2 and parts[0] in ['revisions', 'branches', 'tags']:
            return parts[1]
        return None
