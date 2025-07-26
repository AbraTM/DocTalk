from db.databaseConfig import Base
from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
import uuid


class File(Base):
    __tablename__ = "Files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("Users.id"), nullable=False)
    file_name = Column(String, nullable=False, unique=True)
    s3_url = Column(String, nullable=False)
    uploaded_on = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))