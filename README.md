# mediq backend (FastAPI)

Production-ready starter backend for a hospital management platform.

## Tech
- FastAPI + Pydantic
- PostgreSQL
- SQLAlchemy ORM
- Alembic migrations
- JWT auth + role-based access control (patient/receptionist/doctor/admin)
- WebSocket chat (per appointment)

## Quick start (Windows / PowerShell)

1) Create and activate a virtualenv

```powershell
cd d:\kfiles\mediq
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) Configure env

```powershell
copy .env.example .env
notepad .env
```

3) Create DB (example)

Create a Postgres DB named `mediq`, then set `DATABASE_URL` accordingly.

4) Run migrations

```powershell
alembic upgrade head
```

5) Run API

```powershell
uvicorn app.main:app --reload --port 8000
```

Open docs at `http://localhost:8000/docs`.

## Important endpoints
- `POST /auth/register` patient signup
- `POST /auth/login` get JWT
- `GET /auth/me` current user
- `GET /patients/me/profile` patient profile
- `POST /clinical/appointments` book appointment (auto-assign doctor if available)
- `POST /intake/drafts/from-agent-text` calling-agent transcript → structured intake draft → auto assignment
- `GET /emergency/content` public emergency guidance list
- WebSocket: `/ws/chat/{appointment_id}`

# mediq