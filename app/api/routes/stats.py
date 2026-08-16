"""Live statistics endpoint."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db_session
from app.schemas import StatsResponse
from app.services import StatsService

router = APIRouter()


@router.get("", response_model=StatsResponse)
async def get_stats(session: AsyncSession = Depends(get_db_session)) -> StatsResponse:
    return await StatsService(session).get_stats()
