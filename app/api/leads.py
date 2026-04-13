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


@router.get("/kanban")
def get_kanban(db: Session = Depends(get_db)):
    leads = db.query(Lead).all()

    return {
        "new": [l for l in leads if l.status == "new"],
        "contacted": [l for l in leads if l.status == "contacted"],
        "client": [l for l in leads if l.status == "client"],
        "lost": [l for l in leads if l.status == "lost"],
    }


@router.put("/{lead_id}/status")
def update_status(lead_id: int, status: str, db: Session = Depends(get_db)):

    allowed_status = ["new", "contacted", "client", "lost"]

    if status not in allowed_status:
        raise HTTPException(status_code=400, detail="Invalid status")

    lead = db.query(Lead).filter(Lead.id == lead_id).first()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    lead.status = status

    db.commit()
    db.refresh(lead)

    return lead
