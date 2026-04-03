from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import BudgetItem
from app import schemas

router = APIRouter(prefix="/budget_item", tags=["BudgetItem"])

@router.post("/", response_model=schemas.BudgetItemResponse, status_code=status.HTTP_201_CREATED)
def create_budget(item: schemas.BudgetItemCreate, db: Session = Depends(get_db)):
    obj = BudgetItem(**item.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=List[schemas.BudgetItemResponse])
def list_budgets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(BudgetItem).offset(skip).limit(limit).all()

@router.get("/{budget_id}", response_model=schemas.BudgetItemResponse)
def get_budget(budget_id: int, db: Session = Depends(get_db)):
    obj = db.query(BudgetItem).filter(BudgetItem.id == budget_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="未找到该预算项")
    return obj

@router.put("/{budget_id}", response_model=schemas.BudgetItemResponse)
def update_budget(budget_id: int, item: schemas.BudgetItemUpdate, db: Session = Depends(get_db)):
    obj = db.query(BudgetItem).filter(BudgetItem.id == budget_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="未找到该预算项")
    
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(obj, key, value)
    
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    obj = db.query(BudgetItem).filter(BudgetItem.id == budget_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="未找到该预算项")
    db.delete(obj)
    db.commit()
    return None