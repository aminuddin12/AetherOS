from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ConnectionConfig:
    host: str = "localhost"
    port: int = 5432
    database: str = "aetheros"
    user: str = "aetheros"
    password: str = "aetheros"
    pool_size: int = 10

    @classmethod
    def from_env(cls) -> ConnectionConfig:
        import os

        return cls(
            host=os.environ.get("POSTGRES_HOST", "localhost"),
            port=int(os.environ.get("POSTGRES_PORT", "5432")),
            database=os.environ.get("POSTGRES_DB", "aetheros"),
            user=os.environ.get("POSTGRES_USER", "aetheros"),
            password=os.environ.get("POSTGRES_PASSWORD", "aetheros"),
        )
