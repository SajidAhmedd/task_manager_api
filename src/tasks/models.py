from sqlalchemy import Column, Integer, String, Boolean, DateTime
from src.utils.db import Base

class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    is_completed = Column(Boolean, default=False) 