"""Rule management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db_session
from app.schemas import RuleCreate, RuleResponse
from app.services import DuplicateKeywordError, RuleService

router = APIRouter()


@router.post("", response_model=RuleResponse, status_code=status.HTTP_201_CREATED)
async def create_rule(request: RuleCreate, session: AsyncSession = Depends(get_db_session)) -> RuleResponse:
    try:
        rule = await RuleService(session).create(request)
    except DuplicateKeywordError as exc:
        raise HTTPException(status_code=409, detail="keyword already exists") from exc
    return RuleResponse(rule_id=rule.id, keyword=rule.keyword, dm_message=rule.dm_message)
