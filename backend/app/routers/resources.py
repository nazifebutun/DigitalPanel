from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models
from ..database import get_db
from ..deps import basic_auth

router = APIRouter(prefix="/resources", tags=["Resources"])

@router.get("/", response_model=List[schemas.ResourceOut])
def list_resources(db: Session = Depends(get_db)):
    return db.query(models.StudyResource).order_by(models.StudyResource.created_at.desc()).all()

@router.post("/", response_model=schemas.ResourceOut)
def create_resource(payload: schemas.ResourceCreate, db: Session = Depends(get_db), _: bool = Depends(basic_auth)):
    r = models.StudyResource(title=payload.title, url=str(payload.url), subject=payload.subject)
    db.add(r)
    db.commit()
    db.refresh(r)
    return r

@router.post("/create-from-form")
def create_from_form(title: str = Form(...), url: str = Form(...), subject: str | None = Form(None), db: Session = Depends(get_db), _: bool = Depends(basic_auth)):
    r = models.StudyResource(title=title, url=url, subject=subject)
    db.add(r)
    db.commit()
    return {"status": "ok"}