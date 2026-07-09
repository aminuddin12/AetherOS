from __future__ import annotations

import os
from typing import Optional

import pytest

from aether_storage.adapters import ConnectionConfig
from aether_storage.adapters.postgres import PostgresStorageProvider
from aether_storage.adapters.redis import RedisStorageProvider
from aether_storage.uri.resource_uri import ResourceURI


def _pg_env() -> Optional[ConnectionConfig]:
    if not os.environ.get("POSTGRES_HOST"):
        return None
    return ConnectionConfig.from_env()


def _redis_env() -> Optional[ConnectionConfig]:
    if not os.environ.get("REDIS_HOST"):
        return None
    return ConnectionConfig(
        host=os.environ["REDIS_HOST"],
        port=int(os.environ.get("REDIS_PORT", "6379")),
        password=os.environ.get("REDIS_PASSWORD", ""),
    )


@pytest.mark.asyncio
async def test_postgres_table_resolution_from_uri():
    provider = PostgresStorageProvider(ConnectionConfig())
    uri = ResourceURI("postgres", "db", "/knowledge_facts/abc", {}, None)
    assert provider._table_from_uri(uri) == "knowledge_facts"


@pytest.mark.asyncio
async def test_redis_key_resolution_from_uri():
    provider = RedisStorageProvider(ConnectionConfig(host="redis"))
    uri = ResourceURI("redis", "cache", "/session/1", {}, None)
    assert provider._key_from_uri(uri) == "cache:session/1"


@pytest.mark.asyncio
async def test_postgres_lifecycle_without_db_is_graceful():
    cfg = _pg_env()
    if cfg is None:
        pytest.skip("POSTGRES_HOST not configured")
    provider = PostgresStorageProvider(cfg)
    await provider.initialize()
    assert provider._pool is not None
    await provider.shutdown()
    assert provider._pool is None


@pytest.mark.asyncio
async def test_redis_lifecycle_without_db_is_graceful():
    cfg = _redis_env()
    if cfg is None:
        pytest.skip("REDIS_HOST not configured")
    provider = RedisStorageProvider(cfg)
    await provider.initialize()
    assert provider._client is not None
    await provider.shutdown()
    assert provider._client is None
