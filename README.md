# CareerOS

AI-powered career platform with a resume builder, ATS optimization engine, and hybrid RAG system for intelligent resume analysis and job matching.

**Status: Phase 1 — Foundation**

CareerOS is an AI-powered career platform integrating Resume Building, ATS Analysis, and RAG-powered AI into a single product. See `docs/IMPLEMENTATION_PLAN.md` for the full roadmap.

---

## Architecture

```
Next.js Frontend → FastAPI Backend → PostgreSQL + pgvector
                                  → Redis + Celery Workers
                                  → Object Storage (local/S3)
```

Detailed architecture: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) 24+
- [Node.js](https://nodejs.org/) 20+ (for local frontend development only)
- [Python](https://www.python.org/) 3.11+ (for local backend development only)

---

## Quick Start (Docker)

```bash
# 1. Clone
git clone https://github.com/Sanskarsanshu/careeros.git
cd careeros

# 2. Configure environment
cp .env.example .env
# Edit .env — at minimum set a strong AUTH_SECRET value

# 3. Start all services
docker compose up --build

# 4. Verify
curl http://localhost:8000/api/v1/health
curl http://localhost:8000/api/v1/health/db
curl http://localhost:8000/api/v1/health/redis
```

Frontend: http://localhost:3000  
Backend API: http://localhost:8000  
API Docs: http://localhost:8000/docs

---

## Environment Setup

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

For Phase 1 (foundation only), the minimum required variables are:

```
DATABASE_URL=postgresql+asyncpg://careeros:careeros@postgres:5432/careeros
REDIS_URL=redis://redis:6379/0
AUTH_SECRET=<generate a strong random secret>
```

LLM and embedding keys are not required until Phase 5–6.

---

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
pip install -r requirements-dev.txt

# Start dependent services (postgres + redis only)
docker compose up postgres redis -d

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on http://localhost:3000

---

## Database Migrations

```bash
cd backend

# Apply all migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"

# Rollback one step
alembic downgrade -1
```

---

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# With coverage
pytest --cov=app --cov-report=term-missing

# Specific test file
pytest tests/test_health.py -v
```

### Frontend Type Check + Lint

```bash
cd frontend
npm run type-check
npm run lint
npm run build
```

---

## Project Structure

```
careeros/
├── frontend/          # Next.js 16, TypeScript, Tailwind CSS v4
├── backend/           # FastAPI, Python 3.11, SQLAlchemy 2.x
├── database/          # Alembic migrations
├── infrastructure/    # Dockerfiles, deployment configs
├── docs/              # Architecture, decisions, audit
├── docker-compose.yml
├── .env.example
└── ATTRIBUTIONS.md
```

---



This is **Phase 1**. Product features (resume builder, ATS, RAG, AI) are intentionally not implemented yet.

---

## Docker Services

| Service | Port | Description |
|---------|------|-------------|
| frontend | 3000 | Next.js app |
| backend | 8000 | FastAPI app |
| worker | — | Celery worker |
| postgres | 5432 | PostgreSQL 16 + pgvector |
| redis | 6379 | Redis 7 |

---
