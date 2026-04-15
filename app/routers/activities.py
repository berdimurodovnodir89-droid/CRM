from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityResponse

router = APIRouter(prefix="/activities", tags=["activities"])


@router.post("/", response_model=ActivityResponse)
def create_activity(data: ActivityCreate, db: Session = Depends(get_db)):

    activity = Activity(**data.dict())

    db.add(activity)
    db.commit()
    db.refresh(activity)

    return activity


@router.get("/lead/{lead_id}", response_model=list[ActivityResponse])
def get_lead_activities(lead_id: int, db: Session = Depends(get_db)):

    return db.query(Activity).filter(Activity.lead_id == lead_id).all()
