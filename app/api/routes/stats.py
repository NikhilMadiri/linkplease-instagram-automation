"""Placeholder endpoints for statistics queries."""

from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def get_stats() -> dict[str, str]:
    """Reserve statistics aggregation for a future phase."""
    return {"message": "Not implemented"}
