from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import TripOverview as TripOverviewModel
from app import schemas

router = APIRouter(prefix="/trip_overview", tags=["TripOverview"])

@router.post("/", response_model=schemas.TripOverview)
def create_trip_overview(item: schemas.TripOverviewCreate, db: Session = Depends(get_db)):
    obj = TripOverviewModel(**item.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=List[schemas.TripOverview])
def list_trip_overviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(TripOverviewModel).offset(skip).limit(limit).all()

@router.get("/{overview_id}", response_model=schemas.TripOverview)
def get_trip_overview(overview_id: int, db: Session = Depends(get_db)):
    obj = db.query(TripOverviewModel).filter(TripOverviewModel.id == overview_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="TripOverview not found")
    return obj

@router.put("/{overview_id}", response_model=schemas.TripOverview)
def update_trip_overview(overview_id: int, item: schemas.TripOverviewUpdate, db: Session = Depends(get_db)):
    obj = db.query(TripOverviewModel).filter(TripOverviewModel.id == overview_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="TripOverview not found")
    
    update_data = item.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(obj, k, v)
        
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{overview_id}", response_model=dict)
def delete_trip_overview(overview_id: int, db: Session = Depends(get_db)):
    obj = db.query(TripOverviewModel).filter(TripOverviewModel.id == overview_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="TripOverview not found")
    db.delete(obj)
    db.commit()
    return {"detail": "deleted"}