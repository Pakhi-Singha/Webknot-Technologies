# Webknot-Technologies
To run clone the repository and copy paste the following commands in terminal.
- cd backend
- python -m venv .venv && . .venv/Scripts/activate  # (Windows) or source .venv/bin/activate (Linux/Mac)
- pip install -r requirements.txt
- uvicorn backend.main:app --reload
If database is empty, seed it using the below command in terminal.
- sqlite3 campus.db < seed.sql
