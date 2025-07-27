from db.databaseConfig import Base
from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Summary(Base):
    __tablename__ = "Summaries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    file_id = Column(UUID(as_uuid=True), ForeignKey("Files.id"), nullable=False)
    summary_s3_url = Column(String, nullable=False)
    created_on = Column(TIMESTAMP(timezone=True), server_default=text("now()"),  nullable=False)