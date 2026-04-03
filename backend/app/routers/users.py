from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User as UserModel
from app import schemas

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/", response_model=schemas.User)
def create_user(item: schemas.UserCreate, db: Session = Depends(get_db)):
    obj = UserModel(**item.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=List[schemas.User])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(UserModel).offset(skip).limit(limit).all()

@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    obj = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="User not found")
    return obj

@router.put("/{user_id}", response_model=schemas.User)
def update_user(user_id: int, item: schemas.UserUpdate, db: Session = Depends(get_db)):
    obj = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = item.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(obj, k, v)
        
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    obj = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(obj)
    db.commit()
    return {"detail": "deleted"}