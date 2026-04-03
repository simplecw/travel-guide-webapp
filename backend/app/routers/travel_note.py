from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import TravelNote as TravelNoteModel
from app import schemas

router = APIRouter(prefix="/travel_note", tags=["TravelNote"])

@router.post("/", response_model=schemas.TravelNote)
def create_note(item: schemas.TravelNoteCreate, db: Session = Depends(get_db)):
    obj = TravelNoteModel(**item.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=List[schemas.TravelNote])
def list_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(TravelNoteModel).offset(skip).limit(limit).all()

@router.get("/{note_id}", response_model=schemas.TravelNote)
def get_note(note_id: int, db: Session = Depends(get_db)):
    obj = db.query(TravelNoteModel).filter(TravelNoteModel.id == note_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="TravelNote not found")
    return obj

@router.put("/{note_id}", response_model=schemas.TravelNote)
def update_note(note_id: int, item: schemas.TravelNoteUpdate, db: Session = Depends(get_db)):
    obj = db.query(TravelNoteModel).filter(TravelNoteModel.id == note_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="TravelNote not found")
    
    update_data = item.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(obj, k, v)
        
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{note_id}", response_model=dict)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    obj = db.query(TravelNoteModel).filter(TravelNoteModel.id == note_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="TravelNote not found")
    db.delete(obj)
    db.commit()
    return {"detail": "deleted"}