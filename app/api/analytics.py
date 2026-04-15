from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.deps import get_db
from app.models.lead import Lead
from app.schemas.analytics import DashboardStats

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/dashboard", response_model=DashboardStats)
def dashboard_stats(db: Session = Depends(get_db)):

    total_leads = db.query(func.count(Lead.id)).scalar() or 0

    new_leads = db.query(func.count(Lead.id)).filter(Lead.status == "new").scalar() or 0

    contacted = (
        db.query(func.count(Lead.id)).filter(Lead.status == "contacted").scalar() or 0
    )

    clients = (
        db.query(func.count(Lead.id)).filter(Lead.status == "client").scalar() or 0
    )

    lost = db.query(func.count(Lead.id)).filter(Lead.status == "lost").scalar() or 0

    conversion_rate = 0

    if total_leads > 0:
        conversion_rate = round((clients / total_leads) * 100, 2)

    return {
        "total_leads": total_leads,
        "new_leads": new_leads,
        "contacted": contacted,
        "clients": clients,
        "lost": lost,
        "conversion_rate": conversion_rate,
    }
