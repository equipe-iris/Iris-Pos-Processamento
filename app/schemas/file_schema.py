from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FileCreateSchema(BaseModel):
    name: str

class FileSchema(BaseModel):
    id: int
    name: str
    upload_datetime: datetime
    processing_status: bool
    finished_at: Optional[datetime]
    error: bool

    class Config:
        orm_mode = True