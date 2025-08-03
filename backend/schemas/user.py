from pydantic import BaseModel, EmailStr, field_validator
from uuid import UUID
from utils.pass_hashing import hash_password

class UserLogin(BaseModel):
    email: str
    password: str 

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

    @field_validator("password")
    def hash_pw(cls, val: str) -> str:
        return hash_password(val)

class UserOut(BaseModel):
    id: UUID
    fb_id: str | None
    first_name: str
    last_name: str
    email: EmailStr

    class config:
        from_attributes = True

