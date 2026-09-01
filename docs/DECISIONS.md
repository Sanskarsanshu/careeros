# CareerOS — Architecture Decisions

**Document Status:** LOCKED — Phase 0 Approved  
**Date:** 2026-08-31

Changes to these decisions require an entry in this file with: reason, impact, and migration plan.

---

## Decision 1: Authentication Strategy

**Decision:** JWT (access + refresh tokens) + Google OAuth 2.0

**Details:**
- Access tokens: 15-minute lifetime, signed HS256
- Refresh tokens: 7-day lifetime, stored in httpOnly cookie
- Google OAuth: server-side authorization code flow via `authlib`
- Backend owns all authorization; frontend never sees raw secrets

**Reason:** Industry-standard pattern. Supports both email/password and social login. Backend authorization means the frontend cannot be exploited to access other users' data.

**Alternatives considered:** Session cookies only (less flexible for future mobile); Supabase Auth (external dependency, limits control); Firebase Auth (Google lock-in).

**Consequences:** Requires refresh token rotation logic. Google OAuth requires a configured Google Cloud project with OAuth credentials.

---

## Decision 2: LLM Provider Architecture

**Decision:** Internal provider abstraction over OpenAI (primary) and Google Gemini (secondary)

**Details:**
```
LLMProvider (abstract interface)
├── OpenAIProvider
└── GeminiProvider
```
Selected via `LLM_PROVIDER=openai|gemini` env variable.  
Model configurable via `LLM_MODEL=<model-name>`.  
Structured outputs (JSON mode) used for JD parsing, resume extraction, skill extraction, ATS findings, claim extraction.

**Reason:** Prevents direct vendor coupling. Allows switching providers through config without code changes. Forces clean interface design that future providers can implement.

**Alternatives considered:** LiteLLM (additional dependency, less control); LangChain (too heavy, introduces unnecessary abstractions); direct vendor SDKs throughout codebase (coupling, violates spec).

**Consequences:** Requires maintaining provider implementations. Structured output support varies by model — test each provider.

---

## Decision 3: Embedding Architecture

**Decision:** Embedding provider abstraction, OpenAI as initial provider

**Details:**
```
EmbeddingProvider (abstract interface)
└── OpenAIEmbeddingProvider
```
Model configurable via `EMBEDDING_MODEL`.  
Embedding records store: model_name, model_version, dimensions.  
Do NOT mix embeddings from different models in the same pgvector index.

**Reason:** Embedding models change frequently. Abstraction prevents mass migration when upgrading. Storing model metadata enables detecting incompatible embeddings.

**Alternatives considered:** sentence-transformers local models (no API cost, but deployment complexity, GPU for production); Cohere Embed (additional vendor).

**Consequences:** OpenAI API costs for embeddings. Must re-embed all chunks if model changes (document and track in migrations).

---

## Decision 4: Vector Database

**Decision:** PostgreSQL + pgvector

**Details:**
- Single database for relational data, FTS, and vector search
- pgvector extension installed in Docker PostgreSQL image
- `document_chunks.embedding` column: `vector(1536)` (adjustable per model)
- IVFFlat or HNSW index on embedding column

**Reason:** Eliminates a separate vector database service. PostgreSQL already required. Joins between relational data and vector results are native SQL — simpler than cross-service queries.

**Alternatives considered:** ChromaDB (used in RAG foundation — separate service, no relational joins); Pinecone (managed, external dependency, cost); Weaviate (additional infrastructure complexity).

**Consequences:** pgvector has performance limits at very large scale (millions of vectors). Acceptable for CareerOS use case. Monitor at scale and document upgrade path if needed.

---

## Decision 5: Lexical Search

**Decision:** PostgreSQL Full-Text Search (tsvector/tsquery)

**Details:**
- `document_chunks.ts_content` column of type `tsvector`
- GIN index on `ts_content`
- `ts_rank_cd` for ranking
- Lexical retrieval service interface designed for future BM25 swap

**Reason:** Eliminates BM25 as a separate index. PostgreSQL FTS is production-proven. Keeps the data layer unified. Interface abstraction allows BM25 addition later.

**Alternatives considered:** rank-bm25 library (used in RAG foundation — in-memory, requires separate persistence); Elasticsearch (major additional infrastructure); ParadeDB (pg extension, good but adds operational complexity).

**Consequences:** PostgreSQL FTS uses stemming and stop-word removal, not pure BM25 scoring. This is acknowledged. Call it "lexical retrieval" not "BM25" throughout the codebase.

---

## Decision 6: Reranker

**Decision:** Local cross-encoder via sentence-transformers, abstracted

**Details:**
```
RerankerProvider (abstract interface)
└── CrossEncoderReranker (sentence-transformers)
```
Default model: `cross-encoder/ms-marco-MiniLM-L-6-v2` (configurable via `RERANKER_MODEL`).  
Pipeline: dense top-30 + lexical top-30 → RRF top-20 → reranker top-5 (all configurable).

**Reason:** Local reranker avoids API calls and latency. MiniLM is small enough to run on CPU. Abstract interface allows future hosted reranker (Cohere Rerank) without rewriting.

**Alternatives considered:** Cohere Rerank API (hosted, cost per call, external dependency); BAAI/bge-reranker-large (better quality but heavier CPU load).

**Consequences:** First request triggers model download. Docker image caches model at build time (multi-stage). CPU-only inference adds ~100-300ms per reranking call.

---

## Decision 7: File Storage

**Decision:** LocalStorage in dev; S3-compatible in production — abstracted

**Details:**
```
StorageService (abstract interface)
├── LocalStorageBackend (dev: storage/ directory)
└── S3StorageBackend (prod: AWS S3, Cloudflare R2, Backblaze B2)
```
Selected via `STORAGE_BACKEND=local|s3`.  
PostgreSQL stores object metadata and storage keys only. Binary files not in DB.

**Reason:** Keeps dev simple (no S3 credentials needed). Clean abstraction means rest of codebase never touches filesystem or boto3 directly.

**Consequences:** Local dev storage is not shared across processes. S3 credentials required for production. Ensure storage keys are globally unique (use UUIDs).

---

## Decision 8: Background Jobs

**Decision:** Redis + Celery

**Details:**
- Redis as both Celery broker and result backend
- Celery worker runs as separate Docker service
- Only expensive/slow operations go through Celery: document parsing, embedding generation, RAG ingestion, AI generation
- Fast synchronous ops remain in FastAPI request/response cycle

**Reason:** Prevents timeouts on expensive AI and document operations. Redis already required for caching.

**Alternatives considered:** FastAPI BackgroundTasks (no retry, no distributed workers, no result tracking); RQ (simpler but less ecosystem); ARQ (async, but less mature).

**Consequences:** Requires Celery worker process. Tasks must be idempotent. Result polling via `GET /api/v1/jobs/{job_id}`.

---

## Decision 9: ATS Scoring

**Decision:** Deterministic weighted pipeline; LLMs for semantic help only

**Scoring weights (configurable via env/config):**
| Dimension | Default Weight |
|-----------|---------------|
| Keyword relevance | 25% |
| Skill match | 25% |
| Experience alignment | 20% |
| Project alignment | 10% |
| Education alignment | 10% |
| Structure | 5% |
| Formatting | 5% |

LLM role: structured extraction of JD (skills, requirements), semantic skill synonym matching, human-readable explanations.  
LLM does NOT produce the numerical score.

**Reason:** Deterministic scores are reproducible and explainable. LLM-generated scores are non-deterministic and unverifiable.

---

## Decision 10: API Versioning

**Decision:** `/api/v1/` prefix from day one

**Reason:** Breaking change protection. Once frontend builds against `/api/v1/`, a `/api/v2/` can coexist without a coordinated migration.

---

## Decision 11: Canonical Resume Model

**Decision:** One canonical schema across all subsystems

Extended from Resume Builder foundation. CareerOS adds: certifications, achievements, publications, links, customSections, versioning metadata.

Versions are immutable JSONB snapshots stored in `resume_versions.snapshot`.

**Reason:** Multiple incompatible resume representations across subsystems is the leading cause of data inconsistency. One schema enforced at the database and API layer.
