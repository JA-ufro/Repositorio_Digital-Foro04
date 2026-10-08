from __future__ import annotations

from pydantic import BaseModel, Field

from .domain import Decision


class CreateVersionRequest(BaseModel):
    version_id: str = Field(min_length=1)
    ficha_id: str = Field(min_length=1)


class DecisionRequest(BaseModel):
    actor_role: str = Field(min_length=1)
    decision: Decision
    observation: str | None = None


class AuditResponse(BaseModel):
    decision: str
    observation: str | None
    actor_role: str
    decided_at: str


class VersionResponse(BaseModel):
    version_id: str
    ficha_id: str
    status: str
    observation: str | None
    decided_by: str | None
    decided_at: str | None
    audit: AuditResponse | None = None
