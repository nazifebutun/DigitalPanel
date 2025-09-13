# backend/app/routers/quotes.py
from fastapi import APIRouter, Depends, Form, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from .. import models

router = APIRouter(prefix="/quotes", tags=["quotes"])

@router.post("/create-from-form", status_code=status.HTTP_201_CREATED)
def create_from_form(
    text: str = Form(...),
    author: str = Form(None),
    db: Session = Depends(get_db),
):
    q = models.MotivationQuote(text=text, author=author)
    db.add(q)
    db.commit()
    db.refresh(q)
    return {"ok": True, "id": q.id}

@router.get("/random")
def random_quote(db: Session = Depends(get_db)):
    """PostgreSQL için rastgele 1 kayıt."""
    q = db.query(models.MotivationQuote).order_by(func.random()).first()
    if not q:
        return {"text": None, "author": None}
    return {"text": q.text, "author": q.author}
