"""FastAPI application composition and process lifecycle."""

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.core.logging import configure_logging, logger
from app.database import engine
from app.api.routes import rules, stats, webhook


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Own startup/shutdown hooks for workers and database resources."""
    configure_logging()
    logger.info("Starting %s", get_settings().app_name)
    yield
    await engine.dispose()
    logger.info("Application shutdown complete")


app = FastAPI(title=get_settings().app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rules.router, prefix="/rules", tags=["rules"])
app.include_router(webhook.router, prefix="/webhook", tags=["webhook"])
app.include_router(stats.router, prefix="/stats", tags=["stats"])


@app.get("/", tags=["system"])
async def root() -> dict[str, str]:
    """Provide a simple service identity response."""
    return {"service": "LinkPlease Assignment", "status": "running"}


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    """Provide a lightweight liveness check."""
    return {"status": "healthy"}
