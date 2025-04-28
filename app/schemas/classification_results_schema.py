from pydantic import BaseModel, ConfigDict
from .tickets_schema import CreateTicketSchema
from typing import List

class ClassificationResults(BaseModel):
    file_id: int
    processed_tickets: List[CreateTicketSchema]

    model_config = ConfigDict(from_attributes=True)