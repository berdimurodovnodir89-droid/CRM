from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.tag import Tag

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("/")
def create_tag(name: str, color: str, db: Session = Depends(get_db)):

    tag = Tag(name=name, color=color)

    db.add(tag)
    db.commit()
    db.refresh(tag)

    return tag


@router.get("/")
def get_tags(db: Session = Depends(get_db)):

    tags = db.query(Tag).all()

    return tags


@router.delete("/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db)):

    tag = db.query(Tag).filter(Tag.id == tag_id).first()

    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    db.delete(tag)
    db.commit()

    return {"message": "Tag deleted"}
