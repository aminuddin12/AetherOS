from typing import Dict, Optional
from .resource_uri import ResourceURI

class URIBuilder:
    """Builds a ResourceURI fluently."""
    def __init__(self, scheme: str, authority: str):
        self.scheme = scheme
        self.authority = authority
        self.path = ""
        self.query: Dict[str, str] = {}
        self.fragment: Optional[str] = None

    def with_path(self, path: str) -> 'URIBuilder':
        if not path.startswith('/'):
            path = '/' + path
        self.path = path
        return self

    def with_query(self, key: str, value: str) -> 'URIBuilder':
        self.query[key] = value
        return self

    def with_fragment(self, fragment: str) -> 'URIBuilder':
        self.fragment = fragment
        return self

    def build(self) -> ResourceURI:
        return ResourceURI(self.scheme, self.authority, self.path, self.query, self.fragment)
