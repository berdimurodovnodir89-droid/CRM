from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.db.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    description = Column(String)

    status = Column(String, default="pending")

    lead_id = Column(Integer, ForeignKey("leads.id"))

    created_at = Column(DateTime, server_default=func.now())
