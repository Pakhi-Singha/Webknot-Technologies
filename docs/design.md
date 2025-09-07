# Campus Event Reporting – Design Document

## Scope & Assumptions
- Multi-tenant: 50 colleges, approximately 500 students each, approximately 20 events/semester.
- Event IDs are unique per college: they include college_id and event_id.
- Registration requires unique student_id for each unique event_id.
- Attendance is per event-day check-in; one check-in per student.
- Feedback is optional and monitored on a scale of 1–5 rating. One feedback per student per event.
- Edge cases: duplicate registrations, cancelled events, no feedback, late check-in, etc.

## Data To Track
- Event creation, student registration, attendance, feedback (rating 1–5).

## Database Schema (ER sketch)
- colleges(college_id PK, college_name UNIQUE)
- students(student_id PK, college_id FK → colleges, student_name, email, year, UNIQUE(college_id,email))
- events(event_id PK, college_id FK → colleges, title, type, starts_at, ends_at, UNIQUE(college_id,title,starts_at))
- registrations(registration_id PK, student_id FK, event_id FK, created_at, UNIQUE(student_id,event_id))
- attendance(attendance_id PK, student_id FK, event_id FK, checked_in_at, UNIQUE(student_id,event_id))
- feedback(feedback_id PK, student_id FK, event_id FK, rating 1–5, comment, created_at, UNIQUE(student_id,event_id))

## API Design 
- POST /events
- POST /students
- POST /registrations
- POST /attendance/checkin
- POST /feedback
- GET  /reports/event-popularity?college_id=...
- GET  /reports/student-participation?student_id=...
- GET  /reports/attendance?event_id=...
- GET  /reports/average-feedback?event_id=...
- GET  /reports/top-active-students?college_id=...&limit=...
- GET /reports/event-popularity?college_id=...&type=Workshop|Fest|Seminar

## Workflows
- Script to seed students/staff; also add an admin.
- Admin login (auth) for portal.
- Staff publishes/updates events.
- Students register for events.
- Attendance capture (one check-in per event per student).
- Reports for admin via APIs.

## Scale & Multi-tenancy
- Keep per-college partitioning via foreign keys + indexed filters by college_id.

## Deviations from AI
- Database Schema & Scale was altered to include primary keys (serving as indexes) for easier access.
- Database Schema & Scale was altered to include foreign keys to create a relational schema.
- Database Schema was updated to include data types for validation.
- Database Schema variable names were altered to be unique. Hence, prevent errors during querying.
- Database Schema was altered to include data validation for rating from 1-5.
- Database Schema diagram was generated manually.
- Workflow was altered to include registration script for students and staff.
- Workflow was altered to include authentication for admin protal.
- Workflow was altered to include event updation script.
- Workflow was altered to include attendance monitoring and feedback.
- Workflow was altered to include the API usage of the event monitoring system.
- Frontend was developed with HTML for a cleaner interface.

