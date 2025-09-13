from fastapi import FastAPI, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session


from .database import Base, engine, get_db
from . import models
from .routers import announcements, exams, quotes, resources, duties
from .deps import basic_auth
import os
from datetime import date as _date, timedelta


app = FastAPI(title="School Display – Starter")
# DB tablolarını oluştur
Base.metadata.create_all(bind=engine)


# Routerlar
app.include_router(announcements.router)
app.include_router(duties.router)
app.include_router(exams.router)      # NEW
app.include_router(quotes.router)     # NEW
app.include_router(resources.router)  # NEW
# Templates
BASE_DIR = os.path.dirname(__file__)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


# Basit girişli panel (BasicAuth)
@app.get("/panel")
def panel(request: Request, _: bool = Depends(basic_auth)):
    return templates.TemplateResponse("panel.html", {"request": request})


# Ekran görünümü (TV'ye verilecek URL)
@app.get("/screen")
def screen(request: Request, db: Session = Depends(get_db)):
    items = db.query(models.Announcement).order_by(models.Announcement.created_at.desc()).limit(8).all()
    today = _date.today()
    todays = db.query(models.Duty).filter(models.Duty.date == today).order_by(models.Duty.created_at.desc()).all()

    # Yaklaşan sınavlar (30 gün)
    upcoming = db.query(models.ExamEvent)\
        .filter(models.ExamEvent.date >= today)\
        .filter(models.ExamEvent.date <= today + timedelta(days=30))\
        .order_by(models.ExamEvent.date.asc()).limit(6).all()

    # Motivasyon + Kaynaklar
    quote = db.query(models.MotivationQuote).order_by(models.MotivationQuote.created_at.desc()).first()
    res_list = db.query(models.StudyResource).order_by(models.StudyResource.created_at.desc()).limit(5).all()

    # === YKS geri sayım / ilerleme ===
    yks_str = os.getenv("YKS_DATE", "2026-06-20")               # .env: YKS_DATE=YYYY-MM-DD
    start_str = os.getenv("SCHOOL_YEAR_START", f"{today.year}-09-08")  # .env: SCHOOL_YEAR_START=YYYY-MM-DD
    try:
        yks_date = _date.fromisoformat(yks_str)
    except Exception:
        yks_date = today
    try:
        school_start = _date.fromisoformat(start_str)
    except Exception:
        school_start = _date(today.year, 9, 9)

    days_left = (yks_date - today).days
    total_days = max((yks_date - school_start).days, 1)
    elapsed_days = max((today - school_start).days, 0)
    progress = min(max(int(elapsed_days * 100 / total_days), 0), 100)

    daily_par_goal = os.getenv("DAILY_PARAGRAPH_GOAL", "20")    # .env: DAILY_PARAGRAPH_GOAL=20

    return templates.TemplateResponse(
        "screen.html",
        {
          "request": request, "items": items, "todays": todays, "today": today,
          "upcoming": upcoming, "quote": quote, "res_list": res_list,
          "yks_date": yks_date, "days_left": days_left, "progress": progress,
          "daily_par_goal": daily_par_goal
        }
    )

# Anasayfa → ekran sayfasına yönlendir
@app.get("/")
def root():
    return RedirectResponse(url="/screen")