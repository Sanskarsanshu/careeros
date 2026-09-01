# CareerOS — Implementation Plan

**Version:** 1.0  
**Date:** 2026-08-31  
**Phase:** 0 COMPLETE → Phase 1 IN PROGRESS

---

## Phase Roadmap

| Phase | Name | Status |
|-------|------|--------|
| 0 | Repository Audit & Architecture | ✅ COMPLETE |
| 1 | Foundation (infra, auth, DB, Redis) | 🔄 IN PROGRESS |
| 2 | Resume Builder | ⏳ PENDING |
| 3 | Resume Reader (PDF/DOCX import) | ⏳ PENDING |
| 4 | ATS Engine | ⏳ PENDING |
| 5 | RAG Pipeline | ⏳ PENDING |
| 6 | AI Generation | ⏳ PENDING |
| 7 | Production (auth hardening, security, CI/CD) | ⏳ PENDING |

---

## Phase 1 — Foundation

### Objective
Build the infrastructure shell that all product features will run on. No product features implemented yet.

### Deliverables

**Backend (FastAPI)**
- `/api/v1/health` — live connectivity check
- `/api/v1/health/db` — PostgreSQL connectivity
- `/api/v1/health/redis` — Redis connectivity
- `/api/v1/auth/register` — email/password registration
- `/api/v1/auth/login` — login + JWT issuance
- `/api/v1/auth/me` — authenticated user profile
- SQLAlchemy 2.x async setup
- Alembic migrations (users table + pgvector extension)
- Pydantic v2 settings (all config via env)
- Structured JSON logging + request ID middleware
- CORS configuration
- StorageService abstraction (local backend)
- Celery + Redis worker infrastructure + health_check_task
- Security: bcrypt password hashing, JWT, no secret exposure

**Frontend (Next.js)**
- CareerOS shell with navigation
- Dashboard placeholder page
- Login / Register pages (connected to API)
- Typed API client (`lib/api.ts`)
- Responsive layout

**Infrastructure**
- `docker-compose.yml` with 5 services: frontend, backend, worker, postgres, redis
- PostgreSQL 16 + pgvector extension
- `infrastructure/docker/backend.Dockerfile` (multi-stage)
- `infrastructure/docker/frontend.Dockerfile`
- `.env.example` with all variable categories documented
- `.gitignore`

**Documentation**
- `README.md` with setup instructions
- `ATTRIBUTIONS.md`
- `docs/ARCHITECTURE.md`
- `docs/DECISIONS.md`
- `docs/SOURCE_REPOSITORY_AUDIT.md`

### Phase 1 Acceptance Test
```
docker compose up --build
GET /api/v1/health → 200
GET /api/v1/health/db → 200 (real DB check)
GET /api/v1/health/redis → 200 (real Redis check)
POST /api/v1/auth/register → 201
POST /api/v1/auth/login → 200 + tokens
GET /api/v1/auth/me → 200 (with token)
GET /api/v1/auth/me → 401 (without token)
backend tests pass
frontend build succeeds
```

---

## Phase 2 — Resume Builder (Next)

### Planned Deliverables
- Canonical resume schema (DB tables + API schemas)
- Resume CRUD API (`/api/v1/resumes`)
- Resume versioning API
- Resume Builder UI (adapted from ai-resume-builder)
- Template system (4 initial templates)
- Live preview
- Drag/drop section reordering
- Autosave
- Server-side PDF generation (WeasyPrint)
- DOCX generation (python-docx)
- Zustand UI state (editor state only, not persistence)

---

## Phase 3 — Resume Reader

### Planned Deliverables
- PDF/DOCX document upload endpoint
- pypdf + python-docx text extraction
- Section detection (heuristic + LLM-assisted)
- Entity extraction into canonical schema
- User review UI before committing parsed data
- Background job for large documents

---

## Phase 4 — ATS Engine

### Planned Deliverables
- Job description upload + storage
- JD structured extraction (LLM, Pydantic structured output)
- Keyword matching (exact + normalized)
- Skill matching (exact + semantic)
- Formatting check pipeline
- Weighted deterministic ATS score
- Explainable findings (category, severity, evidence, recommendation)
- ATS report persistence
- ATS UI

---

## Phase 5 — RAG Pipeline

### Planned Deliverables
- Document chunker (800 tokens, 150 overlap)
- Metadata attachment (candidate_id, resume_id, version_id, section, page, chunk_id)
- Embedding generation (OpenAI, abstracted)
- pgvector storage
- PostgreSQL FTS lexical index (tsvector)
- Hybrid retrieval (dense + lexical)
- RRF fusion
- Cross-encoder reranking
- Citation format
- INSUFFICIENT_EVIDENCE signal
- RAG query API endpoint
- RAGAS evaluation dataset

---

## Phase 6 — AI Generation

### Planned Deliverables
- Resume bullet rewriter (grounded)
- Professional summary generator (grounded)
- Resume tailoring pipeline (full flow)
- Claim extraction + evidence verification
- User accept/reject interface
- Before/after ATS comparison
- AI generation persistence + evidence records

---

## Phase 7 — Production

### Planned Deliverables
- Google OAuth 2.0 flow (frontend + backend)
- Rate limiting (slowapi)
- Security hardening review
- OpenTelemetry metrics
- Prometheus `/metrics`
- GitHub Actions CI/CD (lint, typecheck, test, build, deploy)
- Production Dockerfile optimizations
- Deployment documentation (Vercel + Render/Fly.io)
