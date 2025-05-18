from sqlalchemy import Column, Integer, Float
from .base import Base

class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    ast_goal = Column(Float, nullable=True)
