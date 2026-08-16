"""Application services containing Phase 2 business rules."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories import DMRepository, ProcessedEventRepository, RuleRepository
from app.schemas import RuleCreate, StatsResponse, WebhookPayload


class DuplicateKeywordError(Exception):
    pass


class RuleService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = RuleRepository(session)
        self.session = session

    async def create(self, request: RuleCreate):
        keyword = request.keyword.upper()
        if await self.repository.get_by_keyword(keyword):
            raise DuplicateKeywordError
        try:
            rule = await self.repository.create_rule(keyword, request.dm_message)
            await self.session.commit()
            return rule
        except IntegrityError as exc:
            await self.session.rollback()
            raise DuplicateKeywordError from exc


class WebhookService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = ProcessedEventRepository(session)

    async def receive(self, payload: WebhookPayload) -> None:
        if await self.repository.exists(payload.event_id):
            await self.repository.increment_duplicates(payload.event_id)
        else:
            await self.repository.create(**payload.model_dump(), processed=False)
        await self.session.commit()


class StatsService:
    def __init__(self, session: AsyncSession) -> None:
        self.dm_repository = DMRepository(session)
        self.event_repository = ProcessedEventRepository(session)

    async def get_stats(self) -> StatsResponse:
        return StatsResponse(
            sent=await self.dm_repository.count_sent(),
            failed=await self.dm_repository.count_failed(),
            queued=await self.dm_repository.count_queued(),
            duplicates_blocked=await self.event_repository.count_duplicates(),
        )
