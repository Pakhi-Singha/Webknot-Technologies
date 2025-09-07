# Webknot-Technologies
## Description

This is a repository providing a UI to an admin to monitor the activities occuring on the campus database via the web and mobile applications. 

It's divided into 4 folders.

The backend folder contains:

- db.py: this python file connects the sql database to the server.
- main.py: this python file connects to the frontend and provides a back end API to perform GET and POST operations on the server. These operations are used to monitor modifications, registraions, updating of events, attendance tallies, etc, actions, taken by the staff and students.
- models.py: this python file creates the classes which serve as blueprints for various objects like students, events, etc.
- requirements.txt: this text file contains all the necessary downloads along with their versions required to run this repository.
- seed.sql: this sql file seeds mock input in the database to run queries.

The docs folder contains:

- ai-log folder: AI chat logs used to build this application are in this folder.
- design.md: the plan created before beginning work on this application. It discusses everything this application needs to accomplish.
- er_diagram.png: a photo of the ER diagram for the database.

The frontend folder contains:

- index.html: the html file used to stylize the application UI.

The reports folder contains:

- screenshots folder: these are the output snippets with various queries.
- sample-queries.sql: these are the mock queries used to test the database.

The file .gitignore is used to prevent clutter (for example the older python environments, other files on the desktop, etc) from running with the application, preventing performance degradation.

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

Open the link running and add /docs to the end.
- http://127.0.0.1:8000/docs

Execute the commands as needed.
 
These were the commands I executed for screenshots:
- GET /reports/event-popularity?college_id=...
- GET /reports/student-participation?student_id=...
- GET /reports/attendance?event_id=...
- GET /reports/average-feedback?event_id=...
- GET /reports/top-active-students?college_id=...&limit=...
- GET /reports/event-popularity?college_id=...&type=Workshop|Fest|Seminar
