from db.databaseConfig import Base
from sqlalchemy import Column, Text, TIMESTAMP, text, ForeignKey, Enum as EnumPG
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum
import uuid

class Role(Enum):
    user = "user"
    assistant = "assistant"

class Message(Base):
    __tablename__ = "Messages"

    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    chat_id = Column(UUID(as_uuid=True), ForeignKey("Chats.chat_id"), nullable=False)
    role = Column(EnumPG(Role, name='role_enum'), nullable=False)
    content = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    
