"""Minimal Phase 2 API coverage using an isolated async SQLite database."""

import asyncio
from collections.abc import AsyncIterator, Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.base import Base
from app.db import models  # noqa: F401
from app.dependencies import get_db_session
from app.main import app


@pytest.fixture()
def client() -> Iterator[TestClient]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def setup() -> None:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def override_session() -> AsyncIterator[AsyncSession]:
        async with session_factory() as session:
            yield session

    asyncio.run(setup())
    app.dependency_overrides[get_db_session] = override_session
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        asyncio.run(engine.dispose())


def test_create_rule_and_reject_duplicate(client: TestClient) -> None:
    payload = {"keyword": "price", "dm_message": "Here is the price list."}
    response = client.post("/rules", json=payload)
    assert response.status_code == 201
    assert response.json()["keyword"] == "PRICE"

    duplicate = client.post("/rules", json=payload)
    assert duplicate.status_code == 409


def test_duplicate_webhook_is_counted(client: TestClient) -> None:
    payload = {
        "event_id": "evt-1", "event_type": "comment.created", "comment_id": "comment-1",
        "user_id": "user-1", "username": "example", "post_id": "post-1", "comment_text": "PRICE",
    }
    assert client.post("/webhook", json=payload).status_code == 200
    assert client.post("/webhook", json=payload).status_code == 200
    assert client.get("/stats").json() == {"sent": 0, "failed": 0, "queued": 0, "duplicates_blocked": 1}
