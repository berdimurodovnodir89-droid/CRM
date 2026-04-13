from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.source import Source

router = APIRouter(prefix="/sources", tags=["sources"])


@router.post("/")
def create_source(name: str, icon: str, db: Session = Depends(get_db)):

    source = Source(name=name, icon=icon)

    db.add(source)
    db.commit()
    db.refresh(source)

    return source


@router.get("/")
def get_sources(db: Session = Depends(get_db)):

    sources = db.query(Source).all()

    return sources


@router.delete("/{source_id}")
def delete_source(source_id: int, db: Session = Depends(get_db)):

    source = db.query(Source).filter(Source.id == source_id).first()

    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    db.delete(source)
    db.commit()

    return {"message": "Source deleted"}
