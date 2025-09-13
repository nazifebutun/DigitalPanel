from sqlalchemy import Column, Integer, String, Text, DateTime, Date
from sqlalchemy.sql import func
from .database import Base

class Announcement(Base):
    __tablename__ = "announcements"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), unique=True, nullable=False)
    branch = Column(String(120), nullable=True)

class Duty(Base):
    __tablename__ = "duties"
    id = Column(Integer, primary_key=True, index=True)
    teacher_name = Column(String(120), nullable=False)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# YENİ: Sınav Etkinliği (deneme/YKS vb.)
class ExamEvent(Base):
    __tablename__ = "exam_events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)          # Örn: "TÜM 12'ler YKS Denemesi"
    date = Column(Date, nullable=False)                  # Sınav tarihi
    note = Column(String(255), nullable=True)            # Örn: "1. ve 2. ders"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# YENİ: Motivasyon sözleri
class MotivationQuote(Base):
    __tablename__ = "motivation_quotes"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    author = Column(String(120), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# YENİ: Kaynak linkleri (PDF/drive/site)
class StudyResource(Base):
    __tablename__ = "study_resources"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)          # Örn: "TYT Matematik - Problem Notları"
    url = Column(String(500), nullable=False)
    subject = Column(String(120), nullable=True)         # Örn: "Matematik"
    created_at = Column(DateTime(timezone=True), server_default=func.now())