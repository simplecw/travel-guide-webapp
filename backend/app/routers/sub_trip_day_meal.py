from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import SubTripDayMeal as MealModel
from app import schemas

router = APIRouter(prefix="/sub_trip_day_meal", tags=["SubTripDayMeal"])

@router.post("/", response_model=schemas.SubTripDayMeal)
def create_meal(item: schemas.SubTripDayMealCreate, db: Session = Depends(get_db)):
    obj = MealModel(**item.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=List[schemas.SubTripDayMeal])
def list_meals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(MealModel).offset(skip).limit(limit).all()

@router.get("/{meal_id}", response_model=schemas.SubTripDayMeal)
def get_meal(meal_id: int, db: Session = Depends(get_db)):
    obj = db.query(MealModel).filter(MealModel.id == meal_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Meal not found")
    return obj

@router.put("/{meal_id}", response_model=schemas.SubTripDayMeal)
def update_meal(meal_id: int, item: schemas.SubTripDayMealUpdate, db: Session = Depends(get_db)):
    obj = db.query(MealModel).filter(MealModel.id == meal_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Meal not found")
    update_data = item.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{meal_id}")
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    obj = db.query(MealModel).filter(MealModel.id == meal_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Meal not found")
    db.delete(obj)
    db.commit()
    return {"message": "Deleted successfully"}