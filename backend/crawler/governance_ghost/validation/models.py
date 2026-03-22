"""Data models for the validation and scheduling subsystems."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """Result of validating a single scraped item."""

    score: float  # 0.0 (worst) to 1.0 (best)
    issues: list[str] = field(default_factory=list)
    auto_approve: bool = False
    needs_review: bool = False
    claude_verified: bool = False

    def __post_init__(self) -> None:
        self.score = max(0.0, min(1.0, self.score))
        self.auto_approve = self.score > 0.8
        self.needs_review = 0.3 <= self.score <= 0.8


@dataclass
class ScrapingSchedule:
    """Represents the automatic scraping schedule for a single spider."""

    spider_name: str
    cron_expression: str
    enabled: bool = True
    last_run: str | None = None
    last_status: str | None = None
    items_scraped: int = 0
    avg_quality_score: float = 0.0
