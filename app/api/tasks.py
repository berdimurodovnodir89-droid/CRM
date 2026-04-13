from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.task import Task

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/")
def create_task(
    title: str, description: str, lead_id: int, db: Session = Depends(get_db)
):

    task = Task(title=title, description=description, lead_id=lead_id)

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@router.get("/")
def get_tasks(db: Session = Depends(get_db)):

    tasks = db.query(Task).all()

    return tasks


@router.get("/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.put("/{task_id}")
def update_task(
    task_id: int, title: str, description: str, db: Session = Depends(get_db)
):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = title
    task.description = description

    db.commit()
    db.refresh(task)

    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}
