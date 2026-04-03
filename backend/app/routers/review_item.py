from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import ReviewItem as ReviewItemModel
from app import schemas

router = APIRouter(prefix="/review_item", tags=["ReviewItem"])

@router.post("/", response_model=schemas.ReviewItem)
def create_review(item: schemas.ReviewItemCreate, db: Session = Depends(get_db)):
    obj = ReviewItemModel(**item.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=List[schemas.ReviewItem])
def list_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(ReviewItemModel).offset(skip).limit(limit).all()

@router.get("/{review_id}", response_model=schemas.ReviewItem)
def get_review(review_id: int, db: Session = Depends(get_db)):
    obj = db.query(ReviewItemModel).filter(ReviewItemModel.id == review_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="ReviewItem not found")
    return obj

@router.put("/{review_id}", response_model=schemas.ReviewItem)
def update_review(review_id: int, item: schemas.ReviewItemUpdate, db: Session = Depends(get_db)):
    obj = db.query(ReviewItemModel).filter(ReviewItemModel.id == review_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="ReviewItem not found")
    update_data = item.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    obj = db.query(ReviewItemModel).filter(ReviewItemModel.id == review_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="ReviewItem not found")
    db.delete(obj)
    db.commit()
    return {"message": "Deleted successfully"}