from urllib.parse import urlparse, parse_qsl
from .resource_uri import ResourceURI

class URIParser:
    """Parses a string into a ResourceURI."""
    @staticmethod
    def parse(uri_str: str) -> ResourceURI:
        parsed = urlparse(uri_str)
        query = dict(parse_qsl(parsed.query))
        return ResourceURI(
            scheme=parsed.scheme,
            authority=parsed.netloc,
            path=parsed.path,
            query=query,
            fragment=parsed.fragment if parsed.fragment else None
        )
