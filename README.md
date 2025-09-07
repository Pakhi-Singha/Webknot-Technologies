# Webknot-Technologies
To run clone the repository and copy paste the below commands.

cd backend
python -m venv .venv && . .venv/Scripts/activate  # (Windows) or source .venv/bin/activate (Linux/Mac)
pip install -r requirements.txt
uvicorn backend.main:app --reload
