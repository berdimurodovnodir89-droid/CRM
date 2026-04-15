from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.lead import Lead
from app.models.task import Task
from app.models.activity import Activity

from app.schemas.lead import LeadCreate, LeadResponse

router = APIRouter(prefix="/leads", tags=["leads"])


# CREATE
@router.post("/", response_model=LeadResponse)
def create_lead(data: LeadCreate, db: Session = Depends(get_db)):

    lead = Lead(**data.dict())

    db.add(lead)
    db.commit()
    db.refresh(lead)

    return lead


# GET ALL (Pagination)
@router.get("/", response_model=list[LeadResponse])
def get_leads(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):

    leads = db.query(Lead).offset(skip).limit(limit).all()

    return leads


# GET ONE
@router.get("/{lead_id}", response_model=LeadResponse)
def get_lead(lead_id: int, db: Session = Depends(get_db)):

    lead = db.query(Lead).filter(Lead.id == lead_id).first()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    return lead


# UPDATE
@router.put("/{lead_id}", response_model=LeadResponse)
def update_lead(lead_id: int, data: LeadCreate, db: Session = Depends(get_db)):

    lead = db.query(Lead).filter(Lead.id == lead_id).first()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    lead.name = data.name
    lead.phone = data.phone
    lead.source = data.source
    lead.tag = data.tag

    db.commit()
    db.refresh(lead)

    return lead


# DELETE
@router.delete("/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):

    lead = db.query(Lead).filter(Lead.id == lead_id).first()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    db.delete(lead)
    db.commit()

    return {"message": "Lead deleted"}


# SEARCH
@router.get("/search/")
def search_leads(query: str, db: Session = Depends(get_db)):

    leads = db.query(Lead).filter(Lead.name.ilike(f"%{query}%")).all()

    return leads


# KANBAN
@router.get("/kanban")
def get_kanban(db: Session = Depends(get_db)):

    leads = db.query(Lead).all()

    return {
        "new": [l for l in leads if l.status == "new"],
        "contacted": [l for l in leads if l.status == "contacted"],
        "client": [l for l in leads if l.status == "client"],
        "lost": [l for l in leads if l.status == "lost"],
    }


# UPDATE STATUS
@router.put("/{lead_id}/status", response_model=LeadResponse)
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


# LEAD DETAIL (CRM uchun eng muhim endpoint)
@router.get("/{lead_id}/detail")
def get_lead_detail(lead_id: int, db: Session = Depends(get_db)):

    lead = db.query(Lead).filter(Lead.id == lead_id).first()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    tasks = db.query(Task).filter(Task.lead_id == lead_id).all()

    activities = (
        db.query(Activity)
        .filter(Activity.lead_id == lead_id)
        .order_by(Activity.created_at.desc())
        .all()
    )

    return {"lead": lead, "tasks": tasks, "activities": activities}
