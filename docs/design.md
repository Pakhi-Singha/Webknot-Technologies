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
- colleges(int college_id (primary_key), char college_name)
- students(int student_id (primary_key), int college_id (foreign_key), char student_name, char email, int year)
- events(int event_id (primary_key), int college_id (foreign_key), char title, char type, time starts_at, time ends_at)
- registrations(int college_id (foreign_key), student_id (foreign_key), event_id (foreign_key), date created_at)
- attendance(int college_id (foreign_key), int student_id (foreign_key), int event_id (foreign_key), time checked_in_at)
- feedback(int college_id (foreign_key), int student_id (foreign_key), int event_id (foreign_key), int rating =>0 and rating <=5, char comment, date created_at)

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
- GET  /reports/top-active-students?college_id=...&limit=3
- GET /reports/event-popularity?type=Workshop|Fest|Seminar

## Workflows
- Create a registration script to simulate student and staff registrations on the portal.
- Create a login for the admin portal with authentication (This login page can be extended to include students, staff, etc).
- Create an event updation script that simulates staff publishing events that students can sign up for.
- Create an event registration script that simulates students signing up for an event.
- Create an attendance monitoring system that marks attendance for each day a student attends the event they signed up for. It can include feedback after student is marked.
- Create an event reporting system that can be accessed by admin and uses the APIs to fetch results.

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

