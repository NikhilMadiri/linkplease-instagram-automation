"""Placeholder endpoints for rule management."""

from fastapi import APIRouter

router = APIRouter()


@router.post("")
async def create_rule() -> dict[str, str]:
    """Reserve the rule creation contract for a future phase."""
    return {"message": "Not implemented"}
