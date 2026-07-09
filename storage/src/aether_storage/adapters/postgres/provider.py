from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

import asyncpg

from ...core.handle import StorageHandle
from ...core.provider import StorageProvider
from ...uri.resource_uri import ResourceURI
from ..config import ConnectionConfig


class PostgresStorageProvider(StorageProvider):
    def __init__(self, config: ConnectionConfig) -> None:
        self._config = config
        self._pool: asyncpg.Pool | None = None
        self._handle_counter = 0

    def _require_pool(self) -> asyncpg.Pool:
        if self._pool is None:
            raise RuntimeError("PostgresStorageProvider is not initialized")
        return self._pool

    async def initialize(self) -> None:
        dsn = (
            f"postgresql://{self._config.user}:{self._config.password}"
            f"@{self._config.host}:{self._config.port}/{self._config.database}"
        )
        pool = await asyncpg.create_pool(dsn=dsn, min_size=1, max_size=self._config.pool_size)
        if pool is None:
            raise RuntimeError("Failed to create PostgreSQL connection pool")
        self._pool = pool
        async with pool.acquire() as conn:
            await conn.fetchval("SELECT 1")

    async def shutdown(self) -> None:
        if self._pool is not None:
            await self._pool.close()
            self._pool = None

    async def open(self, uri: ResourceURI, mode: str = "r") -> StorageHandle:
        pool = self._require_pool()
        self._handle_counter += 1
        return StorageHandle(
            uri=uri,
            mode=mode,
            handle_id=f"pg-{self._handle_counter}",
            raw_connection=pool,
        )

    async def close(self, handle: StorageHandle) -> None:
        pass

    async def exists(self, uri: ResourceURI) -> bool:
        pool = self._require_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchval(
                "SELECT 1 FROM information_schema.tables WHERE table_name = $1",
                self._table_from_uri(uri),
            )
            return row is not None

    async def resolve(self, uri: ResourceURI) -> ResourceURI:
        return uri

    async def stat(self, uri: ResourceURI) -> dict[str, Any]:
        pool = self._require_pool()
        table = self._table_from_uri(uri)
        async with pool.acquire() as conn:
            size = await conn.fetchval(
                "SELECT pg_total_relation_size($1)", table
            )
            return {"scheme": uri.scheme, "table": table, "bytes": size or 0}

    async def watch(self, uri: ResourceURI) -> Any:
        async def _watch() -> AsyncIterator[dict[str, Any]]:
            if False:
                yield {}
            return
        return _watch()

    async def transaction(self, uri: ResourceURI) -> Any:
        pool = self._require_pool()
        async with pool.acquire() as conn, conn.transaction():
            yield conn

    async def query(self, sql: str, *args: Any) -> list[dict[str, Any]]:
        pool = self._require_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(sql, *args)
            return [dict(row) for row in rows]

    async def execute(self, sql: str, *args: Any) -> str:
        pool = self._require_pool()
        async with pool.acquire() as conn:
            result = await conn.execute(sql, *args)
            return str(result)

    def _table_from_uri(self, uri: ResourceURI) -> str:
        clean = uri.path.lstrip("/")
        return clean.split("/")[0] if clean else "aetheros_default"
