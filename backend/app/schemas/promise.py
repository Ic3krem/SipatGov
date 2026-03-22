from datetime import date

from pydantic import BaseModel


class PromiseListItem(BaseModel):
    id: int
    title: str
    description: str | None = None
    category: str | None = None
    status: str
    date_promised: date | None = None
    confidence_score: float | None = None

    model_config = {"from_attributes": True}


class PromiseStatsResponse(BaseModel):
    lgu_id: int | None = None
    total: int
    kept: int = 0
    broken: int = 0
    in_progress: int = 0
    pending: int = 0
    partially_kept: int = 0
    unverifiable: int = 0
