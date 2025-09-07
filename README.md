# Webknot-Technologies

## How to run

Clone the repository 
- git clone https://github.com/Pakhi-Singha/Webknot-Technologies.git

After cloning, copy paste the following commands in the terminal if you're using Windows.
- cd Webknot-Technologies
- python -m venv .venv #Remember to select the new environment for the workspace
- & .\\.venv\Scripts\Activate.ps1
- pip install -r requirements.txt
- cd backend
- python -c "from db import engine, Base; import models; Base.metadata.create_all(bind=engine); print('Tables created')" #create tables
- python -c "import sqlite3; sql=open('seed.sql','r',encoding='utf-8').read(); con=sqlite3.connect('campus.db'); con.executescript(sql); con.commit(); con.close(); print('Seeded campus.db')" #seed tables with seed.sql data or other data
- python -m uvicorn main:app --reload #run

Otherwise use suitable Linux/Mac commands instead, based on your environment.

These were the executed commands for docs screenshots:
- GET /reports/event-popularity?college_id=...
- GET /reports/student-participation?student_id=...
- GET /reports/attendance?event_id=...
- GET /reports/average-feedback?event_id=...
- GET /reports/top-active-students?college_id=...&limit=3
- GET /reports/event-popularity?college_id=...&type=Workshop|Fest|Seminar
