from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import ReferenceItem
from app import schemas

router = APIRouter(prefix="/reference_item", tags=["ReferenceItem"])

@router.post("/", response_model=schemas.ReferenceItemResponse, status_code=status.HTTP_201_CREATED)
def create_reference(item: schemas.ReferenceItemCreate, db: Session = Depends(get_db)):
    obj = ReferenceItem(**item.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=List[schemas.ReferenceItemResponse])
def list_references(trip_id: int = None, db: Session = Depends(get_db)):
    query = db.query(ReferenceItem)
    if trip_id:
        query = query.filter(ReferenceItem.trip_id == trip_id)
    return query.all()

@router.get("/{reference_id}", response_model=schemas.ReferenceItemResponse)
def get_reference(reference_id: int, db: Session = Depends(get_db)):
    obj = db.query(ReferenceItem).filter(ReferenceItem.id == reference_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Reference not found")
    return obj

@router.put("/{reference_id}", response_model=schemas.ReferenceItemResponse)
def update_reference(reference_id: int, item: schemas.ReferenceItemUpdate, db: Session = Depends(get_db)):
    obj = db.query(ReferenceItem).filter(ReferenceItem.id == reference_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Reference not found")
    
    for key, value in item.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{reference_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reference(reference_id: int, db: Session = Depends(get_db)):
    obj = db.query(ReferenceItem).filter(ReferenceItem.id == reference_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Reference not found")
    db.delete(obj)
    db.commit()
    return None