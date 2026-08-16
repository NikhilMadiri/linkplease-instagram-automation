"""Persistence operations kept separate from domain services."""

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import DMRecord, DMStatus, ProcessedEvent, Rule


class RuleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_rule(self, keyword: str, dm_message: str) -> Rule:
        rule = Rule(keyword=keyword, dm_message=dm_message)
        self.session.add(rule)
        await self.session.flush()
        return rule

    async def get_by_keyword(self, keyword: str) -> Rule | None:
        return await self.session.scalar(select(Rule).where(Rule.keyword == keyword))

    async def list_rules(self) -> list[Rule]:
        return list((await self.session.scalars(select(Rule).order_by(Rule.created_at))).all())


class ProcessedEventRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def exists(self, event_id: str) -> bool:
        return await self.session.scalar(select(ProcessedEvent.event_id).where(ProcessedEvent.event_id == event_id)) is not None

    async def create(self, **event_data: object) -> ProcessedEvent:
        event = ProcessedEvent(**event_data)
        self.session.add(event)
        await self.session.flush()
        return event

    async def increment_duplicates(self, event_id: str) -> None:
        await self.session.execute(
            update(ProcessedEvent)
            .where(ProcessedEvent.event_id == event_id)
            .values(duplicates_blocked=ProcessedEvent.duplicates_blocked + 1)
        )

    async def count_duplicates(self) -> int:
        return int(await self.session.scalar(select(func.coalesce(func.sum(ProcessedEvent.duplicates_blocked), 0))) or 0)


class DMRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, **record_data: object) -> DMRecord:
        record = DMRecord(**record_data)
        self.session.add(record)
        await self.session.flush()
        return record

    async def _count(self, status: DMStatus) -> int:
        return int(await self.session.scalar(select(func.count()).select_from(DMRecord).where(DMRecord.status == status)) or 0)

    async def count_sent(self) -> int:
        return await self._count(DMStatus.SENT)

    async def count_failed(self) -> int:
        return await self._count(DMStatus.FAILED)

    async def count_queued(self) -> int:
        return await self._count(DMStatus.QUEUED)
