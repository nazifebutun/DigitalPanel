from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models
from ..database import get_db
from ..deps import basic_auth

router = APIRouter(prefix="/quotes", tags=["Quotes"])

@router.get("/", response_model=List[schemas.QuoteOut])
def list_quotes(db: Session = Depends(get_db)):
    return db.query(models.MotivationQuote).order_by(models.MotivationQuote.created_at.desc()).all()

@router.post("/", response_model=schemas.QuoteOut)
def create_quote(payload: schemas.QuoteCreate, db: Session = Depends(get_db), _: bool = Depends(basic_auth)):
    q = models.MotivationQuote(text=payload.text, author=payload.author)
    db.add(q)
    db.commit()
    db.refresh(q)
    return q

@router.post("/create-from-form")
def create_from_form(text: str = Form(...), author: str | None = Form(None), db: Session = Depends(get_db), _: bool = Depends(basic_auth)):
    q = models.MotivationQuote(text=text, author=author)
    db.add(q)
    db.commit()
    return {"status": "ok"}