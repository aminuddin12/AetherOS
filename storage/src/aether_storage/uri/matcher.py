from .resource_uri import ResourceURI

class URIMatcher:
    """Matches a ResourceURI against patterns."""
    @staticmethod
    def matches_scheme(uri: ResourceURI, scheme: str) -> bool:
        return uri.scheme == scheme

    @staticmethod
    def matches_authority(uri: ResourceURI, authority: str) -> bool:
        return uri.authority == authority
