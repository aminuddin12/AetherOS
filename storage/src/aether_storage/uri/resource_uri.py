from dataclasses import dataclass
from typing import Optional, Dict

@dataclass(frozen=True)
class ResourceURI:
    """Represents a universal resource identifier in AetherOS."""
    scheme: str
    authority: str
    path: str
    query: Dict[str, str]
    fragment: Optional[str] = None

    def __str__(self) -> str:
        base = f"{self.scheme}://{self.authority}{self.path}"
        if self.query:
            qs = "&".join(f"{k}={v}" for k, v in self.query.items())
            base += f"?{qs}"
        if self.fragment:
            base += f"#{self.fragment}"
        return base
