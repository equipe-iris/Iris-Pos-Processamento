from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class TicketsFiles(Base):
    __tablename__ = "tickets_files"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    upload_datetime = Column(DateTime, nullable=False)
    processing_status = Column(Boolean, nullable=False, default=False)
    finished_at = Column(DateTime, nullable=True)
    error = Column(Boolean, nullable=False, default=False)

    tickets = relationship("ProcessedTickets", back_populates="file")
