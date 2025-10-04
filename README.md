# JobScout (MVP)

## Stack
- Backend: FastAPI, SQLAlchemy, APScheduler
- Frontend: Next.js (App Router), Tailwind
- DB: SQLite (dev) / PostgreSQL (prod)

## Dev Quickstart

Backend:
1. cd backend
2. cp .env.example .env (optional)
3. Install deps: pip install -r requirements.txt
4. Run: PYTHONPATH=. uvicorn app.main:app --reload

Frontend:
1. cd frontend
2. npm run dev

## API Highlights
- POST /api/v1/auth/register
- POST /api/v1/auth/login -> { access_token }
- POST /api/v1/users/me/resume (file upload, Bearer)
- GET /api/v1/jobs?order_by=match&q=python&location=Remote
- POST /api/v1/saved/{job_id}

## Aggregation
- Manual run: POST /api/v1/admin/aggregate/run
- Daily schedule at 02:00 UTC

## Notes
- Resume parsing supports PDF/DOCX/TXT (basic)
- Matching uses simple token overlap (replaceable with embeddings)
