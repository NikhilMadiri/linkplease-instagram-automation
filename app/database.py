"""Database engine lifecycle configuration for PostgreSQL."""

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.config import get_settings


def create_database_engine() -> AsyncEngine:
    """Create the SQLAlchemy 2.x async engine from application settings."""
    return create_async_engine(
        get_settings().database_url,
        pool_pre_ping=True,
        future=True,
    )


engine: AsyncEngine = create_database_engine()
