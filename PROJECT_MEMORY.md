# PROJECT MEMORY

> This document is the single source of truth for the project.
> It must be continuously updated during development.
> Never delete useful historical information.
> Update the current state whenever architecture, implementation,
> bugs, decisions, or progress change.

---

# 1. PROJECT OVERVIEW

## Project Name
CareerOS

## One-Line Description
AI-powered career platform with a production-quality Resume Builder and ATS Engine.

## Full Description
CareerOS is a comprehensive platform designed to help users manage their careers. The initial core feature is a robust Resume Builder that allows users to create, version, and export (PDF/DOCX) resumes using various templates. It features a backend-driven canonical resume schema, ensuring data consistency across the platform. Future phases will introduce AI-assisted parsing, ATS scoring, RAG-based context retrieval, and AI generation.

## Problem Being Solved
Existing resume builders are often frontend-only, lose data when cache is cleared, lack proper versioning, or generate non-ATS-friendly PDFs. CareerOS solves this by persisting a canonical resume schema in a PostgreSQL database, offering real version control, and generating high-quality PDFs via a backend rendering engine (WeasyPrint).

## Target Users
Job seekers, professionals, and students needing high-quality, ATS-optimized resumes.

## Current Development Stage
Phase 1 (Foundation) completed. Phase 2 (Resume Builder) is currently stalled pending local Docker infrastructure fixes.

## Project Status

- [x] Planning (Phase 0)
- [x] Foundation (Phase 1)
- [ ] Core Development (Phase 2 - Resume Builder)
- [ ] Integration
- [ ] Testing
- [ ] Deployment
- [ ] Production

## Current Overall Progress
Estimated percentage: 15%

---

# 2. PROJECT VISION

## Original Goal
Build a real production-quality Resume Builder integrated with CareerOS's backend, PostgreSQL database, authentication system, and canonical resume schema, moving away from localStorage-based architectures.

## Final Intended Product
A full-suite AI career platform supporting resume building, AI generation, ATS parsing and scoring, and intelligent career pathing.

## Core Features
- User Authentication (JWT)
- Canonical Resume Schema (PostgreSQL)
- Resume Versioning (Immutable JSONB snapshots)
- Drag & Drop Section Reordering
- Live Preview
- Server-side PDF & DOCX Export
- Multiple Templates (Classic, Engineering, Modern, etc.)

## Future Features
- LLM Integration (OpenAI/Gemini)
- RAG Pipeline (PostgreSQL pgvector)
- ATS Scoring & Analysis
- Cross-encoder reranking

## Features Explicitly NOT Planned
- LocalStorage-only persistence
- Client-side only AI parsing
- `window.print()` based PDF generation

---

# 3. TECHNOLOGY STACK

## Frontend
- Framework: Next.js 14 (App Router)
- Language: TypeScript
- UI: Radix UI Primitives
- Styling: Tailwind CSS v4
- State Management: Zustand
- Animation: N/A (Yet)
- Other: lucide-react

## Backend
- Framework: FastAPI
- Language: Python 3.11
- API: REST (versioned under `/api/v1`)
- Validation: Pydantic V2
- Authentication: JWT + passlib (bcrypt v3.2.2)

## Database
- Database: PostgreSQL 16
- ORM: SQLAlchemy 2.0 (Async)
- Migrations: Alembic

## AI / ML (Future)
- Models: OpenAI / Gemini
- Embeddings: text-embedding-3-small
- Vector Database: PostgreSQL (pgvector)
- RAG: Hybrid Search (FTS + Vector)
- LLM: gpt-4o-mini
- Reranking: cross-encoder/ms-marco-MiniLM-L-6-v2

## Infrastructure
- Docker: Docker Compose (5 services)
- Cache: Redis 7
- Queue: Celery
- Storage: Local (StorageService abstraction ready for S3)
- Deployment: Pending

## Development Tools
- Git: GitHub
- Package Manager: npm (frontend), pip (backend)
- IDE: VS Code
- Testing: pytest (backend with in-memory SQLite), Next.js build (frontend)

---

# 4. SYSTEM ARCHITECTURE

## Architecture Diagram

```text
                    CAREEROS
                       |
          +------------+------------+
          |                         |
       FRONTEND                  BACKEND (FastAPI)
      (Next.js)                     |
          |                    +----+----+
          |                    |         |
          |                 DATABASE   CACHE & QUEUE
          |               (PostgreSQL) (Redis + Celery)
          |                    |
          |                 +--+--+
          |                 |     |
          |            pgvector  FTS
          |
          +--------- REST API ------+
```

## Communication
- Frontend communicates with Backend via REST API (`/api/v1`).
- Backend uses async SQLAlchemy to talk to PostgreSQL.
- Backend uses Redis for Celery task queuing and caching.
- Authentication is handled via Bearer JWTs passed in headers.

---

# 5. REPOSITORY STRUCTURE

```text
careeros/
├── backend/              # FastAPI application
│   ├── app/              # Core application logic
│   │   ├── api/          # API routers
│   │   ├── core/         # Config, security, DB, dependencies
│   │   ├── models/       # SQLAlchemy ORM models
│   │   ├── repositories/ # Database access layer
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── workers/      # Celery tasks
│   └── tests/            # Pytest test suite
├── database/             # Database migrations
│   └── migrations/       # Alembic configurations
├── docs/                 # Project documentation & ADRs
├── frontend/             # Next.js application
│   ├── app/              # App router pages
│   ├── components/       # React components
│   ├── lib/              # API clients & utilities
│   └── stores/           # Zustand stores
├── infrastructure/       # Dockerfiles & deployment config
│   └── docker/
├── docker-compose.yml    # Main Docker service definitions
└── PROJECT_MEMORY.md     # Single source of truth (this file)
```

---

# 6. FEATURE INVENTORY

| Feature | Status | Location | Notes |
|---|---|---|---|
| JWT Authentication | Complete | `backend/app/api/v1/auth.py` | Registration, login, /me working. |
| Health Checks | Complete | `backend/app/api/v1/health.py` | API, DB, Redis health endpoints. |
| Database Connection | Complete | `backend/app/core/database.py` | Async SQLAlchemy setup. |
| Storage Abstraction | Complete | `backend/app/services/storage_service.py` | Local storage ready. |
| Celery Config | Complete | `backend/app/workers/` | Basic health task verified. |
| Resume Schema | Planned | `backend/app/models/` | Needs 14 tables created. |
| Resume CRUD API | Planned | `backend/app/api/v1/resumes.py` | — |
| Resume Versioning | Planned | — | JSONB snapshots in DB. |
| Editor UI | Planned | `frontend/components/resume-builder/` | — |
| Live Preview | Planned | `frontend/components/resume-preview/` | — |
| PDF Export | Planned | `backend/app/services/export_service.py`| Using WeasyPrint. |

---

# 7. IMPLEMENTATION STATUS

## Completed
- [x] Phase 0 - Repository Audit
- [x] Phase 1 - Foundation Setup (Monorepo, Next.js, FastAPI, PostgreSQL, Redis, Celery)
- [x] Phase 1 - Authentication (JWT, bcrypt)
- [x] Phase 1 - Testing (pytest configured with SQLite)
- [x] Phase 1 - Dockerfiles (frontend & backend optimized)

## Currently Working On
- [ ] Phase 2 - Docker Infrastructure Validation (Blocked)

## Remaining
- [ ] Phase 2 - Canonical Resume Database Schema
- [ ] Phase 2 - Resume Builder API (CRUD & Versioning)
- [ ] Phase 2 - Resume Editor UI
- [ ] Phase 2 - PDF & DOCX Export

## Blocked
- [x] **Docker Daemon Unhealthy**: Local Docker Desktop is unresponsive/hanging on Windows, preventing the startup of PostgreSQL and Redis. Cannot proceed with DB-dependent Phase 2 features until infrastructure is healthy.

---

# 8. CURRENT DEVELOPMENT STATE

## What We Were Working On
Verifying the Docker infrastructure before beginning Phase 2 (Resume Builder) implementation. 

## What Was Just Completed
- Fixed Pydantic V2 deprecation warnings (`ConfigDict`).
- Fixed `python-json-logger` import path deprecation.
- Updated `backend.Dockerfile` to `python:3.11-slim-bookworm` to support WeasyPrint.
- Added `.dockerignore` for frontend and backend.
- Created this `PROJECT_MEMORY.md` file.

## What Is Currently Broken
**Docker Desktop**. The local Docker daemon on Windows hangs and throws `Input/output error` and `context deadline exceeded` when attempting to build images or start containers (`docker compose up -d`).

## What Should Be Done Next
The user needs to restart/fix Docker Desktop locally. Once `docker compose ps` shows healthy PostgreSQL and Redis containers, we must run the initial Alembic migration.

## Exact Next Step
1. Verify Docker is running: `docker compose ps`
2. Run migrations: `docker compose exec backend alembic upgrade head`
3. Test health endpoints: `GET /api/v1/health/db`
4. Test real Auth flow against PostgreSQL.
5. Begin Phase 2 implementation starting with the `Resume` database models.

---

# 9. FILES CREATED

| File | Purpose | Status | Created/Modified |
|---|---|---|---|
| `backend/app/main.py` | FastAPI entry point | Active | Phase 1 |
| `backend/app/models/user.py` | User ORM model | Active | Phase 1 |
| `backend/app/core/security.py`| JWT / Password hashing | Active | Phase 1 |
| `frontend/app/(auth)/login/page.tsx` | Login UI | Active | Phase 1 |
| `docker-compose.yml` | Infrastructure definition | Active | Phase 1 |
| `PROJECT_MEMORY.md` | Single Source of Truth | Active | Phase 2 Start |

---

# 10. FILES MODIFIED

| File | Change | Reason | Status |
|---|---|---|---|
| `backend/app/schemas/auth.py` | `class Config` -> `ConfigDict` | Pydantic V2 Deprecation | Complete |
| `backend/app/core/config.py` | `jsonlogger` import update | Deprecation | Complete |
| `infrastructure/docker/backend.Dockerfile` | Base image `bookworm` + deps | Fix WeasyPrint support | Complete |

---

# 11. DATABASE

**Database**: PostgreSQL 16 (via Docker)
**ORM**: SQLAlchemy 2.0 (Async)

## Current Tables
### `users`
- `id` (UUID, PK)
- `email` (String, Unique)
- `password_hash` (String)
- `google_id` (String, Nullable)
- `full_name` (String, Nullable)
- `is_active` (Boolean)
- `created_at` / `updated_at` (DateTime)

## Planned Tables (Phase 2)
- `resumes`
- `resume_versions` (with JSONB `snapshot`)
- `resume_sections`
- `personal_info`
- `experiences`, `educations`, `projects`, `skills`, `certifications`, `achievements`, `publications`, `links`, `custom_sections`

---

# 12. API DOCUMENTATION

| Method | Endpoint | Purpose | Auth | Status |
|---|---|---|---|---|
| GET | `/api/v1/health` | Basic API health | No | Complete |
| GET | `/api/v1/health/db` | Database connectivity | No | Complete |
| GET | `/api/v1/health/redis`| Redis connectivity | No | Complete |
| POST | `/api/v1/auth/register`| Register user | No | Complete |
| POST | `/api/v1/auth/login` | Login, returns JWT | No | Complete |
| GET | `/api/v1/auth/me` | Get current user | Yes| Complete |

---

# 13. AI / ML / RAG ARCHITECTURE

*(To be implemented in Phase 4 & 5. See `docs/DECISIONS.md` for architectural decisions regarding OpenAI/Gemini, pgvector, and cross-encoders.)*

---

# 14. ENVIRONMENT VARIABLES

| Variable | Purpose | Required |
|---|---|---|
| `APP_ENV` | Environment (dev/prod) | No |
| `DATABASE_URL` | Async PG connection string | Yes |
| `DATABASE_SYNC_URL` | Sync PG connection string (Alembic)| Yes |
| `REDIS_URL` | Redis connection | Yes |
| `CELERY_BROKER_URL` | Celery broker | Yes |
| `AUTH_SECRET` | JWT signing secret | Yes |
| `CORS_ORIGINS` | Allowed frontend domains | Yes |

---

# 15. DEPENDENCIES

| Package | Purpose | Version | Reason |
|---|---|---|---|
| `fastapi` | Backend Framework | latest | High performance, async, types |
| `sqlalchemy` | ORM | 2.0+ | Standard DB interaction |
| `passlib` | Password hashing | latest | Security |
| `bcrypt` | Hashing algorithm | 3.2.2 | Pinned due to passlib compatibility issues with newer bcrypt versions in Python 3.11+ |
| `next` | Frontend Framework | 14.x | App router, React 18 |
| `weasyprint` | PDF Generation | (Planned) | High fidelity HTML -> PDF |
| `python-docx` | DOCX Generation | (Planned) | Native word document export |

---

# 16. BUG TRACKER

| ID | Bug | Severity | Cause | Status | Fix |
|---|---|---|---|---|---|
| BUG-001 | Test `AttributeError: 'str' object has no attribute 'hex'` | High | SQLite test DB passed string UUIDs to SQLAlchemy. | Fixed | Converted string to `uuid.UUID` in `UserRepository.get_by_id`. |
| BUG-002 | `Alembic` env.py cannot find `app` module | Medium | Path insertion in `env.py` was too shallow. | Fixed | Updated `sys.path.insert` to correctly navigate up 3 levels to find `backend`. |
| BUG-003 | Docker Compose build hangs/Input Output Error | Critical | Windows Docker Desktop daemon unresponsive/corrupted. | Blocked | User must restart/reset Docker Desktop locally. |

---

# 17. DEBUGGING HISTORY

## BUG-003: Docker Daemon Hangs on Windows

**Problem**: `docker compose up -d --build` fails.
**Symptoms**: `Input/output error` during `apt-get` inside the container build. `context deadline exceeded` when running `docker compose ps` or `docker info`.
**Root Cause**: The Docker Desktop daemon on Windows is hung, likely due to a corrupted WSL2 disk, MTU mismatch, or internal locking.
**Investigation**: Ran `docker info` (hung), restarted Docker process via PowerShell (briefly recovered, then hung again when pulling postgres/redis).
**Solution**: Pending user action to reset Docker Desktop.
**Regression Risk**: High, if Docker is unstable, local development and testing of DB features is impossible.

---

# 18. ARCHITECTURAL DECISIONS

### ADR-001 — PDF Generation Strategy
**Date:** 2026-08-31
**Decision:** Use WeasyPrint on the backend instead of `window.print()` on the frontend.
**Why This Was Chosen:** WeasyPrint provides exact styling control, ensures selectable text (ATS friendly), and decouples export from the browser context.
**Tradeoffs:** Requires system-level dependencies (Pango, Cairo) which necessitates using Debian-based Docker images (`bookworm-slim`) rather than Alpine.

### ADR-002 — Resume Versioning
**Date:** 2026-08-31
**Decision:** Store historical versions as immutable JSONB snapshots in `resume_versions.snapshot`.
**Why This Was Chosen:** Prevents massive database complexity. Reconstructing a past resume from dozens of normalized relational tables (when relationships might have been deleted) is error-prone. A JSONB snapshot captures the exact state cleanly.

---

# 19. DESIGN DECISIONS

- **Design System**: Radix UI Primitives + Tailwind CSS v4.
- **Styling Approach**: Dual-renderer for Resumes. React components for the live web preview; Jinja2 HTML/CSS for backend WeasyPrint PDF generation.
- **Color Scheme**: Defined via CSS variables in `globals.css` (Light/Dark mode ready).

---

# 20. PERFORMANCE

- **Backend Latency**: `TimingMiddleware` implemented to track endpoint speeds.
- **Database**: Async SQLAlchemy engine with connection pooling enabled.
- **Frontend**: Next.js App Router for optimal Server Components delivery.

---

# 21. SECURITY

- **Authentication**: JWT stored securely (client-side implementation pending secure HttpOnly cookies vs localStorage debate).
- **Passwords**: Bcrypt hashing.
- **Data Isolation**: All `UserRepository` and future `ResumeRepository` methods strictly filter by `user_id` to prevent cross-tenant data access.
- **Error Handling**: Global exception handler masks 500 errors to prevent stack trace leaks.

---

# 22. TESTING

## Unit Tests
*(Pending Phase 2)*

## Integration Tests
- `backend/tests/test_health.py` (Passed)
- `backend/tests/test_auth.py` (Passed)
- Database tests use an isolated in-memory async SQLite engine (`sqlite+aiosqlite:///:memory:`).

## Known Untested Areas
- Live PostgreSQL integration (Blocked by Docker issues).

---

# 23. DEPLOYMENT

*(Not yet configured. Docker Compose is currently used for local development.)*

---

# 24. COMMANDS

```bash
# Backend (Local)
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
python -m pytest -v

# Frontend (Local)
cd frontend
npm run dev
npm run build

# Docker
docker compose up -d --build
docker compose ps
docker compose exec backend alembic upgrade head
```

---

# 25. KNOWN LIMITATIONS

- Cannot generate initial Alembic migration script until a live PostgreSQL connection is established.
- Storage service is currently local-only; S3 backend needs implementation.

---

# 26. TECHNICAL DEBT

* **Problem**: Alembic initial migration missing.
* **Why it exists**: Docker daemon crashed before it could be run against the live DB.
* **Impact**: Database schema cannot be initialized locally using standard tools.
* **Priority**: High (Fix once Docker is back).

---

# 27. TODO / ROADMAP

## Immediate
- Resolve Docker Desktop issues.
- Run `alembic upgrade head`.

## Short Term (Phase 2)
- Implement Canonical Resume Schema (PostgreSQL).
- Implement Resume CRUD and Versioning APIs.
- Build Frontend Resume Editor and Live Preview.
- Implement Backend PDF/DOCX generation.

## Medium Term (Phase 3 & 4)
- Resume Parser (Upload existing PDF).
- ATS Scoring Engine.

## Long Term (Phase 5+)
- RAG & AI Generation capabilities.

---

# 28. CHANGELOG

## 2026-08-31 — Session 1
### Added
- Created `PROJECT_MEMORY.md`.
- Added `.dockerignore` for frontend and backend.
### Changed
- Fixed Pydantic V2 and `python-json-logger` deprecation warnings.
- Updated `backend.Dockerfile` to use `bookworm` for WeasyPrint dependencies.
### Blocked
- Docker Desktop daemon hung, preventing live database testing.
### Next Step
- User to fix Docker Desktop locally.

---

# 29. SESSION HANDOFF

## Last Session
Date: 2026-08-31

## What We Did
- Audited the entire Phase 1 foundation.
- Fixed backend deprecation warnings.
- Prepared Dockerfiles for Phase 2 WeasyPrint dependencies.
- Attempted to start Docker Compose infrastructure.
- Initialized the `PROJECT_MEMORY.md` file.

## What Changed
- `backend/app/schemas/auth.py` (Pydantic V2 fix)
- `backend/app/core/config.py` (Logger fix)
- `infrastructure/docker/backend.Dockerfile` (Base image update)
- Added `.dockerignore` files.
- Created `PROJECT_MEMORY.md`.

## Current State
Phase 1 code is fully written, tested (via SQLite), and ready. However, the local Docker environment is completely broken/unresponsive.

## Problems Remaining
**Docker Desktop is hung/dead on the host Windows machine.** We cannot start PostgreSQL, Redis, or Celery.

## Exact Next Task
1. Wait for the user to restart Docker Desktop and confirm it works (`docker compose ps`).
2. Run the Alembic migrations against the live database: `docker compose exec backend alembic upgrade head`.
3. Test real authentication against PostgreSQL.
4. Begin Phase 2 implementation starting with the `models/resume.py` database schema.

## Files Relevant To Next Task
- `docker-compose.yml`
- `database/migrations/env.py`
- `backend/app/models/resume.py` (To be created)

## Important Context
Do not start writing the Phase 2 Resume Models until the Docker infrastructure is verified as healthy, per the user's strict instructions.

---

# 30. AI HANDOFF INSTRUCTIONS

## Before Changing Code
1. Read `PROJECT_MEMORY.md`.
2. Inspect the relevant existing code.
3. Understand the current architecture.
4. Do not assume previous implementations are correct.
5. Check known bugs and architectural decisions.
6. Identify dependencies between the requested change and existing functionality.

## While Changing Code
1. Make the smallest correct change necessary.
2. Do not unnecessarily rewrite working systems.
3. Preserve existing functionality.
4. Follow existing architecture and naming conventions.
5. Test changes.
6. Check for regressions.
7. Update `PROJECT_MEMORY.md`.

## After Changing Code
Always:
1. Verify the implementation.
2. Record what changed.
3. Record important files modified.
4. Record bugs discovered.
5. Record bugs fixed.
6. Record architectural decisions.
7. Update implementation status.
8. Update the changelog.
9. Update the session handoff.
10. Clearly state the next task.
