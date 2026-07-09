from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

import redis.asyncio as aioredis

from ...core.handle import StorageHandle
from ...core.provider import StorageProvider
from ...uri.resource_uri import ResourceURI
from ..config import ConnectionConfig


class RedisStorageProvider(StorageProvider):
    def __init__(self, config: ConnectionConfig) -> None:
        self._config = config
        self._client: aioredis.Redis | None = None
        self._handle_counter = 0

    def _require_client(self) -> aioredis.Redis:
        if self._client is None:
            raise RuntimeError("RedisStorageProvider is not initialized")
        return self._client

    async def initialize(self) -> None:
        client = aioredis.Redis(
            host=self._config.host,
            port=self._config.port,
            password=self._config.password or None,
            decode_responses=False,
        )
        await client.ping()
        self._client = client

    async def shutdown(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def open(self, uri: ResourceURI, mode: str = "r") -> StorageHandle:
        client = self._require_client()
        self._handle_counter += 1
        return StorageHandle(
            uri=uri,
            mode=mode,
            handle_id=f"redis-{self._handle_counter}",
            raw_connection=client,
        )

    async def close(self, handle: StorageHandle) -> None:
        pass

    async def exists(self, uri: ResourceURI) -> bool:
        client = self._require_client()
        return bool(await client.exists(self._key_from_uri(uri)))

    async def resolve(self, uri: ResourceURI) -> ResourceURI:
        return uri

    async def stat(self, uri: ResourceURI) -> dict[str, Any]:
        client = self._require_client()
        key = self._key_from_uri(uri)
        return {"scheme": uri.scheme, "key": key, "ttl": await client.ttl(key)}

    async def watch(self, uri: ResourceURI) -> Any:
        async def _watch() -> AsyncIterator[dict[str, Any]]:
            if False:
                yield {}
            return
        return _watch()

    async def transaction(self, uri: ResourceURI) -> Any:
        client = self._require_client()
        async with client.pipeline(transaction=True) as pipe:
            yield pipe

    async def get(self, uri: ResourceURI) -> bytes | None:
        client = self._require_client()
        value = await client.get(self._key_from_uri(uri))
        return value if isinstance(value, bytes) else None

    async def set(self, uri: ResourceURI, value: bytes, ttl: int | None = None) -> None:
        client = self._require_client()
        key = self._key_from_uri(uri)
        if ttl:
            await client.setex(key, ttl, value)
        else:
            await client.set(key, value)

    async def delete(self, uri: ResourceURI) -> int:
        client = self._require_client()
        return int(await client.delete(self._key_from_uri(uri)))

    def _key_from_uri(self, uri: ResourceURI) -> str:
        clean = uri.path.lstrip("/")
        return f"{uri.authority}:{clean}" if clean else uri.authority
