# Webknot-Technologies

## How to run

Clone the repository 
- git clone https://github.com/Pakhi-Singha/Webknot-Technologies.git

After cloning, copy paste the following commands in the terminal if you're using Windows.
- cd Webknot-Technologies/backend
- python -m venv .venv #Remember to select the new environment for the workspace
- & .\\.venv\Scripts\Activate.ps1
- pip install -r requirements.txt
- python -m uvicorn main:app --reload

Otherwise use suitable Linux/Mac commands instead, based on your environment.

If database is empty, seed it using the below command in terminal.
- sqlite3 campus.db < seed.sql
