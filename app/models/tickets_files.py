from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class TicketsFiles(Base):
    __tablename__ = "tickets_files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    upload_datetime = Column(DateTime(timezone=True), nullable=False)
    processing_status = Column(Boolean, nullable=False, default=False)
    finished_at = Column(DateTime(timezone=True), nullable=True)

    tickets = relationship("ProcessedTickets", back_populates="file")
