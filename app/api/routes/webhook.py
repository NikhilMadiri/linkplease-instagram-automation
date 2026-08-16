"""Placeholder endpoints for inbound webhook processing."""

from fastapi import APIRouter

router = APIRouter()


@router.post("")
async def receive_webhook() -> dict[str, str]:
    """Reserve webhook ingestion for a future phase."""
    return {"message": "Not implemented"}
