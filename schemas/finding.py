from pydantic import BaseModel, Field
from datetime import datetime


class CreateFinding(BaseModel):
    title: str = Field(min_length=4, max_length=100)
    description: str = Field(min_length=10, max_length=500)
    severity: str
    cve_id: str | None = None
    port: int | None = None
    endpoint: str | None = None


class FindingResponse(BaseModel):
    id: int
    scan_id: int
    title: str
    description: str
    severity: str
    cve_id: str | None
    host: str
    port: int | None
    endpoint: str | None
    created_at: datetime
    status: str
    cvss_score: float | None


