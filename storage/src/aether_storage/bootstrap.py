from __future__ import annotations

from .adapters import ConnectionConfig, registry
from .adapters.postgres import PostgresStorageProvider
from .adapters.redis import RedisStorageProvider


class PersistenceBootstrap:
    def __init__(self) -> None:
        self._pg: PostgresStorageProvider | None = None
        self._redis: RedisStorageProvider | None = None

    async def start(self) -> None:
        self._pg = PostgresStorageProvider(ConnectionConfig.from_env())
        try:
            await self._pg.initialize()
        except Exception:
            self._pg = None

        redis_cfg = ConnectionConfig(
            host=__import__("os").environ.get("REDIS_HOST", "localhost"),
            port=int(__import__("os").environ.get("REDIS_PORT", "6379")),
            password=__import__("os").environ.get("REDIS_PASSWORD", ""),
        )
        self._redis = RedisStorageProvider(redis_cfg)
        try:
            await self._redis.initialize()
        except Exception:
            self._redis = None

        registry.register("postgres", PostgresStorageProvider)
        registry.register("redis", RedisStorageProvider)

    async def stop(self) -> None:
        if self._pg is not None:
            await self._pg.shutdown()
        if self._redis is not None:
            await self._redis.shutdown()

    @property
    def postgres(self) -> PostgresStorageProvider | None:
        return self._pg

    @property
    def redis(self) -> RedisStorageProvider | None:
        return self._redis


_bootstrap: PersistenceBootstrap | None = None


async def start_persistence() -> PersistenceBootstrap:
    global _bootstrap
    if _bootstrap is None:
        _bootstrap = PersistenceBootstrap()
        await _bootstrap.start()
    return _bootstrap


async def stop_persistence() -> None:
    global _bootstrap
    if _bootstrap is not None:
        await _bootstrap.stop()
        _bootstrap = None


def get_persistence() -> PersistenceBootstrap | None:
    return _bootstrap
