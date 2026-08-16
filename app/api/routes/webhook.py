"""Inbound webhook ingestion endpoint."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db_session
from app.schemas import WebhookPayload
from app.services import WebhookService

router = APIRouter()


@router.post("")
async def receive_webhook(payload: WebhookPayload, session: AsyncSession = Depends(get_db_session)) -> dict[str, str]:
    await WebhookService(session).receive(payload)
    return {"status": "received"}
