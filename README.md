# AI Data Agent (MVP)

## Features
- Upload any Excel file
- Preview first 5 rows
- Automatic summary (stats)
- Generate a simple bar chart for a chosen column

## Tech Stack
- Frontend: React
- Backend: FastAPI (Python)
- Database: None (in-memory for MVP)

## Run locally
### Backend
```bash
cd backend
pip install fastapi uvicorn pandas matplotlib openpyxl
uvicorn main:app --reload --port 8000

