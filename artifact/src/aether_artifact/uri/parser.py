from aether_storage.uri.resource_uri import ResourceURI
from typing import Optional

class ArtifactURIParser:
    """Specialized parser for artifact:// URIs."""
    @staticmethod
    def extract_classification(uri: ResourceURI) -> str:
        # e.g. artifact://contracts/worker -> 'contracts'
        return uri.authority

    @staticmethod
    def extract_name(uri: ResourceURI) -> str:
        # e.g. artifact://contracts/worker -> 'worker'
        return uri.path.strip('/')
