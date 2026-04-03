from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import TodoItem
from app.schemas import TodoCreate, TodoUpdate, Todo

router = APIRouter(prefix="/todo_item", tags=["TodoItem"])

@router.post("/", response_model=Todo)
def create_todo(item: TodoCreate, db: Session = Depends(get_db)):
    obj = TodoItem(**item.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=List[Todo])
def list_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(TodoItem).offset(skip).limit(limit).all()

@router.get("/{todo_id}", response_model=Todo)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    obj = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="TodoItem not found")
    return obj

@router.put("/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, item: TodoUpdate, db: Session = Depends(get_db)):
    obj = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="TodoItem not found")
    
    update_data = item.dict(exclude_unset=True)
    for k, v in update_data.items():
        setattr(obj, k, v)
        
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{todo_id}", response_model=dict)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    obj = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="TodoItem not found")
    db.delete(obj)
    db.commit()
    return {"message": "TodoItem deleted successfully"}