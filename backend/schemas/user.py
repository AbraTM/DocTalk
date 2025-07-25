from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserCreate(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr

class UserOut(BaseModel):
    id: UUID
    fb_id: str
    firstName: str
    lastName: str
    email: EmailStr

    class config:
        from_attributes = True

