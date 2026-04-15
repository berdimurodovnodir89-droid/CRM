from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)

    lead_id = Column(Integer, ForeignKey("leads.id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    action = Column(String, nullable=False)
    note = Column(String, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
