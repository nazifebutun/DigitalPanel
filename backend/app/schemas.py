from pydantic import BaseModel, HttpUrl
from datetime import datetime, date

class AnnouncementCreate(BaseModel):
    title: str
    content: str

class AnnouncementOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    class Config:
        from_attributes = True

class TeacherCreate(BaseModel):
    name: str
    branch: str | None = None

class TeacherOut(BaseModel):
    id: int
    name: str
    branch: str | None = None
    class Config:
        from_attributes = True

class DutyCreate(BaseModel):
    teacher_name: str
    date: date

class DutyOut(BaseModel):
    id: int
    teacher_name: str
    date: date
    created_at: datetime
    class Config:
        from_attributes = True

# YENİ: Sınav
class ExamCreate(BaseModel):
    title: str
    date: date
    note: str | None = None

class ExamOut(BaseModel):
    id: int
    title: str
    date: date
    note: str | None = None
    created_at: datetime
    class Config:
        from_attributes = True

# YENİ: Motivasyon
class QuoteCreate(BaseModel):
    text: str
    author: str | None = None

class QuoteOut(BaseModel):
    id: int
    text: str
    author: str | None = None
    created_at: datetime
    class Config:
        from_attributes = True

# YENİ: Kaynak
class ResourceCreate(BaseModel):
    title: str
    url: HttpUrl
    subject: str | None = None

class ResourceOut(BaseModel):
    id: int
    title: str
    url: HttpUrl
    subject: str | None = None
    created_at: datetime
    class Config:
        from_attributes = True