from pydantic import BaseModel
from datetime import datetime


class ReportRequest(BaseModel):

    campaign_id: str

    report_type: str


class ReportResponse(BaseModel):

    campaign_id: str

    report_type: str

    generated_at: datetime

    report_url: str

    summary: str