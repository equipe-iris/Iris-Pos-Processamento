from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProcessedTickets(Base):
    __tablename__ = "processed_tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    service_rating = Column(String, nullable=False)
    sentiment_rating = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
