from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class ProcessedTickets(Base):
    __tablename__ = "processed_tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    service_rating = Column(String, nullable=False)
    sentiment_rating = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    file_id = Column(Integer, ForeignKey("tickets_files.id"))

    file = relationship("TicketsFiles", back_populates="tickets")
