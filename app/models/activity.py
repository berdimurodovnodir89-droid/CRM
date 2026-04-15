from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    type = Column(String)
    note = Column(String)
