from pydantic import BaseModel
from enum import Enum

# class Role(Enum):
#     user = "user"
#     assitant = "assistant"

class ChatCreate(BaseModel):
    user_id: str
    title: str

    class config:
        from_attributes = True