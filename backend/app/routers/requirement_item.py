from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import RequirementItem
from app import schemas

router = APIRouter(prefix="/requirement_item", tags=["RequirementItem"])

@router.post("/", response_model=schemas.RequirementItemResponse, status_code=status.HTTP_201_CREATED)
def create_requirement(item: schemas.RequirementItemCreate, db: Session = Depends(get_db)):
    # 检查是否已存在（模型中 trip_id 是 unique=True）
    existing = db.query(RequirementItem).filter(RequirementItem.trip_id == item.trip_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Requirement already exists for this trip")
    
    obj = RequirementItem(**item.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/{requirement_id}", response_model=schemas.RequirementItemResponse)
def get_requirement(requirement_id: int, db: Session = Depends(get_db)):
    obj = db.query(RequirementItem).filter(RequirementItem.id == requirement_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Requirement not found")
    return obj

@router.get("/by_trip/{trip_id}", response_model=schemas.RequirementItemResponse)
def get_requirement_by_trip(trip_id: int, db: Session = Depends(get_db)):
    obj = db.query(RequirementItem).filter(RequirementItem.trip_id == trip_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Requirement for this trip not found")
    return obj

@router.put("/{requirement_id}", response_model=schemas.RequirementItemResponse)
def update_requirement(requirement_id: int, item: schemas.RequirementItemUpdate, db: Session = Depends(get_db)):
    obj = db.query(RequirementItem).filter(RequirementItem.id == requirement_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Requirement not found")
    
    for key, value in item.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{requirement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_requirement(requirement_id: int, db: Session = Depends(get_db)):
    obj = db.query(RequirementItem).filter(RequirementItem.id == requirement_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Requirement not found")
    db.delete(obj)
    db.commit()
    return None