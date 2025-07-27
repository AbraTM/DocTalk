from pydantic import BaseModel
from uuid import UUID

class SummaryCreate(BaseModel):
    file_id: UUID
    summary_s3_url: str

