from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from .. import schemas, models
from ..database import get_db
from ..deps import basic_auth

router = APIRouter(prefix="/exams", tags=["Exams"])

@router.get("/", response_model=List[schemas.ExamOut])
def list_exams(db: Session = Depends(get_db)):
    return db.query(models.ExamEvent).order_by(models.ExamEvent.date.asc()).all()

@router.get("/upcoming", response_model=List[schemas.ExamOut])
def upcoming(db: Session = Depends(get_db)):
    return db.query(models.ExamEvent).filter(models.ExamEvent.date >= date.today()).order_by(models.ExamEvent.date.asc()).all()

@router.post("/", response_model=schemas.ExamOut)
def create_exam(payload: schemas.ExamCreate, db: Session = Depends(get_db), _: bool = Depends(basic_auth)):
    e = models.ExamEvent(title=payload.title, date=payload.date, note=payload.note)
    db.add(e)
    db.commit()
    db.refresh(e)
    return e

@router.post("/create-from-form")
def create_from_form(title: str = Form(...), date: str = Form(...), note: str | None = Form(None), db: Session = Depends(get_db), _: bool = Depends(basic_auth)):
    e = models.ExamEvent(title=title, date=date, note=note)
    db.add(e)
    db.commit()
    return {"status": "ok"}