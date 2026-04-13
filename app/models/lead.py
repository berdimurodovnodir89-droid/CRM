from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException

from app.db.deps import get_db
from app.models.lead import Lead

from app.db.base import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    phone = Column(String, index=True)

    status = Column(String, default="new")

    manager_id = Column(Integer, ForeignKey("users.id"))

    source = Column(String)
    tag = Column(String)

    created_at = Column(DateTime, server_default=func.now())


router = APIRouter(prefix="/leads", tags=["leads"])


@router.post("/")
def create_lead(name: str, phone: str, db: Session = Depends(get_db)):

    lead = Lead(name=name, phone=phone)

    db.add(lead)
    db.commit()
    db.refresh(lead)

    return lead


@router.get("/")
def get_leads(db: Session = Depends(get_db)):

    leads = db.query(Lead).all()

    return leads


@router.get("/{lead_id}")
def get_lead(lead_id: int, db: Session = Depends(get_db)):

    lead = db.query(Lead).filter(Lead.id == lead_id).first()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    return lead


@router.put("/{lead_id}")
def update_lead(lead_id: int, name: str, phone: str, db: Session = Depends(get_db)):

    lead = db.query(Lead).filter(Lead.id == lead_id).first()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    lead.name = name
    lead.phone = phone

    db.commit()
    db.refresh(lead)

    return lead


@router.delete("/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):

    lead = db.query(Lead).filter(Lead.id == lead_id).first()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    db.delete(lead)
    db.commit()

    return {"message": "Lead deleted"}
