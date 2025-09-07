from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from pathlib import Path
from fastapi.staticfiles import StaticFiles
app = FastAPI(title="Campus Events API")  
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/ui", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="ui")
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, select, desc
from sqlalchemy.exc import IntegrityError
from db import Base, engine, get_db
from models import College, Student, Event, Registration, Attendance, Feedback
from pydantic.alias_generators import to_camel

app = FastAPI(title="Campus Events API")

# Create tables
Base.metadata.create_all(bind=engine)

# ====== Schemas ======
class BaseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

class CollegeIn(BaseSchema):
    college_name: str = Field(alias="CollegeName")

class StudentIn(BaseSchema):
    college_id: int   = Field(alias="CollegeId")
    student_name: str = Field(alias="StudentName")
    email: str
    year: int | None = None

class EventIn(BaseSchema):
    college_id: int   = Field(alias="CollegeId")
    title: str        = Field(alias="Title")
    type: str         = Field(alias="Type")
    starts_at: datetime = Field(alias="StartsAt")
    ends_at: datetime   = Field(alias="EndsAt")

class RegistrationIn(BaseSchema):
    student_id: int = Field(alias="StudentId")
    event_id: int   = Field(alias="EventId")

class CheckinIn(BaseSchema):
    student_id: int = Field(alias="StudentId")
    event_id: int   = Field(alias="EventId")

class FeedbackIn(BaseSchema):
    student_id: int = Field(alias="StudentId")
    event_id: int   = Field(alias="EventId")
    rating: int = Field(ge=1, le=5, alias="Rating")   # API-level validation 1–5
    comment: Optional[str] = Field(default=None, alias="Comment")

# ====== CRUD endpoints ======
@app.post("/colleges")
def create_college(payload: CollegeIn, db: Session = Depends(get_db)):
    c = College(name=payload.name)
    db.add(c); db.commit(); db.refresh(c)
    return c

@app.post("/students")
def create_student(payload: StudentIn, db: Session = Depends(get_db)):
    s = Student(**payload.model_dump())
    db.add(s)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(400, "Student email already exists in this college.")
    db.refresh(s)
    return s

@app.post("/events")
def create_event(payload: EventIn, db: Session = Depends(get_db)):
    e = Event(**payload.model_dump())
    db.add(e)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(400, "Event already exists for this college at this time.")
    db.refresh(e)
    return e

@app.post("/registrations")
def register_student(payload: RegistrationIn, db: Session = Depends(get_db)):
    r = Registration(**payload.model_dump())
    db.add(r)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(400, "Duplicate registration.")
    db.refresh(r)
    return r

@app.post("/attendance/checkin")
def checkin(payload: CheckinIn, db: Session = Depends(get_db)):
    a = Attendance(**payload.model_dump())
    db.add(a)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(400, "Already checked in.")
    db.refresh(a)
    return a

@app.post("/feedback")
def post_feedback(payload: FeedbackIn, db: Session = Depends(get_db)):
    f = Feedback(**payload.model_dump())
    db.add(f)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(400, "Feedback already exists for this student & event.")
    db.refresh(f)
    return f

# ====== Reports ======

# ====== Reports (use new column names + return dicts) ======
from sqlalchemy import func, desc
from sqlalchemy.orm import Session
from fastapi import Depends

@app.get("/reports/event-popularity")
def event_popularity(college_id: int, type: Optional[str] = None, db: Session = Depends(get_db)):
    q = (
        db.query(
            Event.event_id,
            Event.title,
            Event.type,
            func.count(Registration.registration_id).label("registrations"),
        )
        .join(Registration, Registration.event_id == Event.event_id, isouter=True)
        .filter(Event.college_id == college_id)
        .group_by(Event.event_id, Event.title, Event.type)
        .order_by(desc("registrations"))
    )
    if type:
        q = q.filter(Event.type == type)
    rows = q.all()
    # Convert SQLAlchemy Row -> plain dicts (JSON-serializable)
    return [
        {"event_id": r[0], "title": r[1], "type": r[2], "registrations": r[3]}
        for r in rows
    ]

@app.get("/reports/student-participation")
def student_participation(student_id: int, db: Session = Depends(get_db)):
    total = (
        db.query(func.count(Attendance.attendance_id))
        .filter(Attendance.student_id == student_id)
        .scalar()
    )
    return {"student_id": student_id, "events_attended": int(total or 0)}

@app.get("/reports/attendance")
def attendance_percentage(event_id: int, db: Session = Depends(get_db)):
    regs = (
        db.query(func.count(Registration.registration_id))
        .filter(Registration.event_id == event_id)
        .scalar()
    )
    atts = (
        db.query(func.count(Attendance.attendance_id))
        .filter(Attendance.event_id == event_id)
        .scalar()
    )
    pct = (atts / regs * 100.0) if regs else 0.0
    return {
        "event_id": event_id,
        "registrations": int(regs or 0),
        "attended": int(atts or 0),
        "attendance_percent": round(pct, 2),
    }

@app.get("/reports/average-feedback")
def average_feedback(event_id: int, db: Session = Depends(get_db)):
    avg = db.query(func.avg(Feedback.rating)).filter(Feedback.event_id == event_id).scalar()
    return {"event_id": event_id, "avg_feedback": round(float(avg), 2) if avg is not None else None}

@app.get("/reports/top-active-students")
def top_active_students(college_id: int, limit: int = 3, db: Session = Depends(get_db)):
    rows = (
        db.query(
            Student.student_id,
            Student.student_name,
            func.count(Attendance.attendance_id).label("attended"),
        )
        .join(Attendance, Attendance.student_id == Student.student_id)
        .filter(Student.college_id == college_id)
        .group_by(Student.student_id, Student.student_name)
        .order_by(desc("attended"))
        .limit(limit)
        .all()
    )
    return [{"student_id": r[0], "student_name": r[1], "attended": r[2]} for r in rows]

