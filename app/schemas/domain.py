"""Request and response contracts for Phase 2 endpoints."""

from pydantic import BaseModel, ConfigDict, Field, field_validator


class RuleCreate(BaseModel):
    keyword: str = Field(min_length=1)
    dm_message: str = Field(min_length=1)

    @field_validator("keyword", "dm_message")
    @classmethod
    def reject_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must not be blank")
        return value.strip()


class RuleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    rule_id: str
    keyword: str
    dm_message: str


class WebhookPayload(BaseModel):
    event_id: str = Field(min_length=1)
    event_type: str = Field(min_length=1)
    comment_id: str = Field(min_length=1)
    user_id: str = Field(min_length=1)
    username: str = Field(min_length=1)
    post_id: str = Field(min_length=1)
    comment_text: str = Field(min_length=1)


class StatsResponse(BaseModel):
    sent: int
    failed: int
    queued: int
    duplicates_blocked: int
