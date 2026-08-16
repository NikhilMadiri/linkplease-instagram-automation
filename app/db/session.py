"""Async SQLAlchemy session factory and request-scoped session helpers."""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.database import engine

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
