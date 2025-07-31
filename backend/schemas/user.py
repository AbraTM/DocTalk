from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

class UserOut(BaseModel):
    id: UUID
    fb_id: str
    first_name: str
    last_name: str
    email: EmailStr

    class config:
        from_attributes = True

