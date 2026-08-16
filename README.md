# LinkPlease Assignment

Phase 1 is a production-oriented FastAPI skeleton. It establishes application composition, async PostgreSQL connectivity, migrations, dependency injection, logging, and extension points without implementing domain behavior.

## Setup

Requirements: Python 3.12, PostgreSQL 16+, and Docker (optional).

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env
```

Update `DATABASE_URL` in `.env` when using a local PostgreSQL instance. The example value targets the Compose database hostname.

## Run

```bash
uvicorn app.main:app --reload
```

Or run the app and PostgreSQL together:

```bash
docker compose up --build
```

The API is available at `http://localhost:8000`. OpenAPI documentation is at `/docs`.

## Routes

- `GET /` — service status
- `GET /health` — liveness status
- `POST /rules` — placeholder
- `POST /webhook` — placeholder
- `GET /stats` — placeholder

## Migrations

Alembic is configured for SQLAlchemy's async PostgreSQL driver. Once models exist, create and apply migrations with:

```bash
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

No migration is included yet because Phase 1 defines no business models.
