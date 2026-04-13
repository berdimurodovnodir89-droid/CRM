from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.db.deps import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(name: str, phone: str, password: str, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.phone == phone).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Phone already registered")

    user = User(name=name, phone=phone, password=password)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
