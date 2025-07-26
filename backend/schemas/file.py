from pydantic import BaseModel

class FileCreate(BaseModel):
    user_id: str 
    file_name: str
    s3_url: str

    class Config:
        from_attributes = True
