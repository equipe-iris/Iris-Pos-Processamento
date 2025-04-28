from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class CreateTicketSchema(BaseModel):
    id: str
    title: str
    service_rating: str
    sentiment_rating: str
    start_date: datetime
    end_date: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class TicketSchema(BaseModel):
    id: int
    original_id: str
    title: str
    service_rating: str
    sentiment_rating: str
    start_date: datetime
    end_date: Optional[datetime]
    file_id: int

    model_config = ConfigDict(from_attributes=True)