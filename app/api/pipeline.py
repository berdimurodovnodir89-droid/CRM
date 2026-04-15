from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.pipeline import PipelineStage
from app.schemas.pipeline import PipelineCreate, PipelineResponse

router = APIRouter(prefix="/pipeline", tags=["pipeline"])


@router.post("/", response_model=PipelineResponse)
def create_stage(data: PipelineCreate, db: Session = Depends(get_db)):

    stage = PipelineStage(**data.dict())

    db.add(stage)
    db.commit()
    db.refresh(stage)

    return stage


@router.get("/", response_model=list[PipelineResponse])
def get_stages(db: Session = Depends(get_db)):

    return db.query(PipelineStage).order_by(PipelineStage.order).all()
