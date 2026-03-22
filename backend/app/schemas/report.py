from pydantic import BaseModel, Field


class CreateReportRequest(BaseModel):
    title: str = Field(min_length=5, max_length=200)
    description: str = Field(min_length=10, max_length=2000)
    report_type: str = Field(
        pattern="^(concern|feedback|corruption_tip|progress_update|delay_report)$"
    )
    lgu_id: int | None = None
    project_id: int | None = None
    is_anonymous: bool = False
