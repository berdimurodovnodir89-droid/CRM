from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.db.base import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    phone = Column(String, index=True)

    status = Column(String, default="new")

    stage_id = Column(Integer, ForeignKey("pipeline_stages.id"))

    manager_id = Column(Integer, ForeignKey("users.id"))

    source = Column(String)
    tag = Column(String)

    created_at = Column(DateTime, server_default=func.now())
