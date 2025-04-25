from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)