from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.lead import Lead


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


@router.get("/search/")
def search_leads(query: str, db: Session = Depends(get_db)):

    leads = db.query(Lead).filter(Lead.name.ilike(f"%{query}%")).all()

    return leads
