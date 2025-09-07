# backend/models.py
from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey,
    UniqueConstraint, CheckConstraint, func
)
from sqlalchemy.orm import Mapped, mapped_column
from db import Base

class College(Base):
    __tablename__ = "colleges"
    college_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    college_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

class Student(Base):
    __tablename__ = "students"
    student_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    college_id: Mapped[int] = mapped_column(ForeignKey("colleges.college_id"), index=True, nullable=False)
    student_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=True)  # or String if you prefer "FY-3"
    __table_args__ = (UniqueConstraint("college_id", "email", name="uq_student_email_per_college"),)

class Event(Base):
    __tablename__ = "events"
    event_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    college_id: Mapped[int] = mapped_column(ForeignKey("colleges.college_id"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)  # Workshop/Fest/Seminar/etc.
    starts_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    ends_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    __table_args__ = (UniqueConstraint("college_id", "title", "starts_at", name="uq_event_per_college_time"),)

class Registration(Base):
    __tablename__ = "registrations"
    registration_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.student_id"), index=True, nullable=False)
    event_id: Mapped[int]  = mapped_column(ForeignKey("events.event_id"), index=True, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.strftime('%Y-%m-%d %H:%M:%f', 'now'))
    __table_args__ = (UniqueConstraint("student_id", "event_id", name="uq_unique_registration"),)

class Attendance(Base):
    __tablename__ = "attendance"
    attendance_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.student_id"), index=True, nullable=False)
    event_id: Mapped[int]  = mapped_column(ForeignKey("events.event_id"), index=True, nullable=False)
    checked_in_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.strftime('%Y-%m-%d %H:%M:%f', 'now'))
    __table_args__ = (UniqueConstraint("student_id", "event_id", name="uq_unique_checkin"),)

class Feedback(Base):
    __tablename__ = "feedback"
    feedback_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.student_id"), index=True, nullable=False)
    event_id: Mapped[int]  = mapped_column(ForeignKey("events.event_id"), index=True, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.strftime('%Y-%m-%d %H:%M:%f', 'now'))
    __table_args__ = (
        UniqueConstraint("student_id", "event_id", name="uq_unique_feedback"),
        CheckConstraint("rating BETWEEN 1 AND 5", name="ck_feedback_rating"),
    )
