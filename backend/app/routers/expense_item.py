from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import ExpenseItem
from app import schemas

router = APIRouter(prefix="/expense_item", tags=["ExpenseItem"])

# --- CREATE (增) ---
@router.post("/", response_model=schemas.ExpenseItemResponse, status_code=status.HTTP_201_CREATED)
def create_expense(item: schemas.ExpenseItemCreate, db: Session = Depends(get_db)):
    """新增一条支出记录"""
    obj = ExpenseItem(**item.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

# --- READ ALL (查列表) ---
@router.get("/", response_model=List[schemas.ExpenseItemResponse])
def list_expenses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """分页获取所有支出记录"""
    return db.query(ExpenseItem).offset(skip).limit(limit).all()

# --- READ ONE (查单个) ---
@router.get("/{expense_id}", response_model=schemas.ExpenseItemResponse)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    """根据 ID 获取支出详情"""
    obj = db.query(ExpenseItem).filter(ExpenseItem.id == expense_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="未找到该支出记录")
    return obj

# --- UPDATE (改) ---
@router.put("/{expense_id}", response_model=schemas.ExpenseItemResponse)
def update_expense(expense_id: int, item: schemas.ExpenseItemUpdate, db: Session = Depends(get_db)):
    """修改支出记录"""
    obj = db.query(ExpenseItem).filter(ExpenseItem.id == expense_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="未找到该支出记录")
    
    # 获取传递的更新数据（排除未设置的字段）
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(obj, key, value)
    
    db.commit()
    db.refresh(obj)
    return obj

# --- DELETE (删) ---
@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    """删除支出记录"""
    obj = db.query(ExpenseItem).filter(ExpenseItem.id == expense_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="未找到该支出记录")
    
    db.delete(obj)
    db.commit()
    return None