from pydantic import BaseModel

class TokenCreate(BaseModel):
    firebase_token: str
    summary_id: str