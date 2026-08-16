"""FastAPI dependency providers shared by API routes."""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.db.session import async_session_factory


async def get_db_session() -> AsyncIterator[AsyncSession]:
    """Provide one transactional session per request."""
    async with async_session_factory() as session:
        yield session


def get_app_settings() -> Settings:
    """Expose settings through FastAPI's dependency system."""
    return get_settings()
