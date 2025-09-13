# backend/app/routers/duties.py
from fastapi import APIRouter, Depends, Form, status
from sqlalchemy.orm import Session
from datetime import date

from ..database import get_db
from .. import models

router = APIRouter(prefix="/duties", tags=["duties"])

@router.post("/create-from-form", status_code=status.HTTP_201_CREATED)
def create_from_form(
    teacher_name: str = Form(...),
    date: date = Form(...),
    db: Session = Depends(get_db),
):
    duty = models.Duty(teacher_name=teacher_name, date=date)
    db.add(duty)
    db.commit()
    db.refresh(duty)
    return {"ok": True, "id": duty.id}

# İstersen hızlı test için JSON endpoint’i:
@router.get("/today")
def list_today(db: Session = Depends(get_db)):
    today = date.today()
    rows = db.query(models.Duty).filter(models.Duty.date == today).all()
    return rows
