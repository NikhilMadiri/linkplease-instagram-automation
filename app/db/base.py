"""Declarative SQLAlchemy base used by all future database models."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Metadata registry shared by SQLAlchemy models and Alembic."""
