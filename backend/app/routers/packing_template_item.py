from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import PackingTemplateItem
from app import schemas

router = APIRouter(prefix="/packing_template_item", tags=["PackingTemplateItem"])

@router.post("/", response_model=schemas.PackingTemplateItemResponse, status_code=status.HTTP_201_CREATED)
def create_template(item: schemas.PackingTemplateItemCreate, db: Session = Depends(get_db)):
    obj = PackingTemplateItem(**item.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=List[schemas.PackingTemplateItemResponse])
def list_templates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(PackingTemplateItem).offset(skip).limit(limit).all()

@router.get("/{template_id}", response_model=schemas.PackingTemplateItemResponse)
def get_template(template_id: int, db: Session = Depends(get_db)):
    obj = db.query(PackingTemplateItem).filter(PackingTemplateItem.id == template_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Template not found")
    return obj

@router.put("/{template_id}", response_model=schemas.PackingTemplateItemResponse)
def update_template(template_id: int, item: schemas.PackingTemplateItemUpdate, db: Session = Depends(get_db)):
    obj = db.query(PackingTemplateItem).filter(PackingTemplateItem.id == template_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Template not found")
    
    for key, value in item.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_template(template_id: int, db: Session = Depends(get_db)):
    obj = db.query(PackingTemplateItem).filter(PackingTemplateItem.id == template_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Template not found")
    db.delete(obj)
    db.commit()
    return None