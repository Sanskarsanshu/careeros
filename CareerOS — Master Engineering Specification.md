# CareerOS — Master Engineering Specification

You are the lead software architect and senior full-stack/AI engineer responsible for building **CareerOS**, a production-ready AI-powered career platform.

Repository:

`https://github.com/Sanskarsanshu/careeros`

Your job is NOT to create a demo, mockup, prototype, or collection of disconnected features.

Your job is to build a **fully functional, testable, maintainable, deployable application** from the repository.

---

# 1. PRODUCT OBJECTIVE

CareerOS is an AI-powered career platform centered around three tightly integrated systems:

```text
                         CareerOS
                            │
        ┌───────────────────┼──────────────────┐
        ↓                   ↓                  ↓
 Resume Builder        ATS Analyzer        AI / RAG
        │                   │                  │
        ↓                   ↓                  ↓
 Templates             JD Analysis        Resume KB
 Live Editor            Keywords           Hybrid Search
 Drag/Drop              Skill Gap          Reranking
 PDF/DOCX               Formatting         Citations
        │                   │                  │
        └───────────────────┼──────────────────┘
                            ↓
                      PostgreSQL
                            +
                         pgvector
                            +
                           Redis
                            │
                            ↓
                       FastAPI API
```

The three systems must work together around a **single canonical candidate profile / knowledge base**.

The final application must allow a user to:

1. Create a resume from scratch.
2. Select professional resume templates.
3. Edit resume sections with a live preview.
4. Drag/reorder sections and entries.
5. Import an existing PDF/DOCX resume.
6. Parse the existing resume into structured candidate data.
7. Store the candidate profile.
8. Store resume versions.
9. Generate PDF and DOCX resumes.
10. Paste or upload a Job Description.
11. Analyze the Job Description.
12. Compare the JD against the candidate's resume.
13. Calculate an explainable ATS/job-match score.
14. Identify matched skills.
15. Identify missing skills.
16. Identify partially matched skills.
17. Detect formatting/ATS compatibility problems.
18. Use RAG to retrieve relevant candidate evidence.
19. Ask questions about the candidate's resume.
20. Generate job-specific resume improvements.
21. Generate/rewrite resume bullets.
22. Generate professional summaries.
23. Tailor an entire resume for a specific JD.
24. Prevent fabricated experience, skills, companies, metrics, education, or achievements.
25. Show evidence/citations for AI-generated claims.
26. Allow users to review and accept/reject AI changes.
27. Maintain multiple resume versions.
28. Re-run ATS analysis after changes.
29. Compare ATS results before/after optimization.
30. Deploy the entire system to production.

---

# 2. NON-NEGOTIABLE PRINCIPLE

DO NOT hallucinate requirements.

DO NOT invent product requirements.

DO NOT silently replace technologies.

DO NOT remove functionality because it is difficult.

DO NOT create fake buttons that do nothing.

DO NOT create placeholder API responses pretending features work.

DO NOT hard-code fake ATS scores.

DO NOT use mock data in production flows.

DO NOT claim a feature is complete until it is actually functional and tested.

If something is ambiguous:

1. Inspect the repository.
2. Inspect the existing implementation.
3. Follow the architecture specified here.
4. Choose the simplest production-safe implementation.
5. Document the decision.
6. Do not invent unrelated functionality.

If a requirement conflicts with an existing implementation, the specification in this document takes priority.

---

# 3. TARGET ARCHITECTURE

Use a clear separation between frontend, backend, AI/RAG, data, and infrastructure.

Recommended architecture:

```text
careeros/
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── features/
│   │   ├── resume-builder/
│   │   ├── resume-reader/
│   │   ├── ats/
│   │   ├── jobs/
│   │   └── ai/
│   ├── hooks/
│   ├── lib/
│   ├── stores/
│   └── types/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── workers/
│   │   └── main.py
│   │
│   ├── ingestion/
│   ├── parsing/
│   ├── ats/
│   ├── rag/
│   │   ├── ingestion/
│   │   ├── embeddings/
│   │   ├── retrieval/
│   │   ├── hybrid/
│   │   ├── reranking/
│   │   ├── generation/
│   │   └── citations/
│   └── tests/
│
├── database/
│   ├── migrations/
│   └── seeds/
│
├── infrastructure/
│   ├── docker/
│   └── deployment/
│
├── docker-compose.yml
├── .env.example
└── README.md
```

You may adjust this structure when technically justified, but preserve the separation of responsibilities.

---

# 4. FRONTEND

Use:

- Next.js
- TypeScript
- Tailwind CSS
- modern component architecture
- accessible UI
- responsive design

The UI must feel like a serious SaaS product.

Do NOT build a generic AI chatbot UI.

The product should have:

## Dashboard

Show:

- Resume versions
- Recent ATS analyses
- Recent job descriptions
- Resume completion status
- Latest ATS score
- Quick actions

## Resume Builder

Provide:

- Personal information
- Professional summary
- Experience
- Education
- Projects
- Skills
- Certifications
- Achievements
- Publications
- Links
- Custom sections

Allow:

- Add
- Delete
- Edit
- Reorder
- Duplicate
- Hide/show sections
- Drag and drop
- Autosave
- Undo/redo where practical

## Template system

Implement a real template architecture.

Templates must consume the same canonical resume schema.

Initial templates should include at least:

- ATS Classic
- Modern
- Professional
- Minimal
- Engineering

Do not duplicate business logic inside every template.

Use a shared resume schema + rendering abstraction.

## Live preview

Changes made in the editor must immediately reflect in the preview.

The preview must be printable/exportable.

---

# 5. RESUME DATA MODEL

Create a canonical resume schema.

Do NOT allow every component to invent its own resume structure.

The same schema must power:

- editor
- templates
- PDF
- DOCX
- ATS
- parsing
- RAG
- AI generation

Example conceptual model:

```text
Resume
 ├── personal
 ├── summary
 ├── experience[]
 ├── education[]
 ├── projects[]
 ├── skills[]
 ├── certifications[]
 ├── achievements[]
 ├── publications[]
 ├── links[]
 └── customSections[]
```

Use versioning:

```text
Resume
 ├── version 1
 ├── version 2
 ├── version 3
 └── tailored version for Job X
```

---

# 6. RESUME IMPORT / READER

Support:

- PDF
- DOCX

Pipeline:

```text
PDF/DOCX
   ↓
Document extraction
   ↓
Text normalization
   ↓
Section detection
   ↓
Entity extraction
   ↓
Structured Resume
   ↓
Candidate Knowledge Base
```

The parser must distinguish between:

- contact information
- education
- experience
- projects
- skills
- certifications
- achievements
- links

Preserve the original uploaded document.

Allow the user to review parsed information before committing it.

Never silently overwrite user data.

---

# 7. ATS ENGINE

The ATS system must NOT be just an LLM prompt that returns:

"ATS Score: 87"

Build an explainable scoring pipeline.

Analyze:

## Resume structure

- Contact information
- Standard section headings
- Experience
- Education
- Skills
- Projects
- Certifications

## Formatting

Detect potential ATS problems such as:

- image-based text
- unreadable PDF text
- unusual layouts
- excessive tables
- important content hidden in headers/footers
- missing headings
- problematic formatting
- excessively complex structures

## Job Description

Extract:

- required skills
- preferred skills
- technologies
- responsibilities
- qualifications
- education requirements
- experience requirements
- keywords
- seniority
- domain terminology

## Matching

Calculate:

- keyword match
- semantic skill match
- experience relevance
- project relevance
- education fit
- responsibility alignment
- formatting compatibility

Produce an explainable report:

```text
ATS / Job Match Score: 91

Keyword Match: 94
Skills Match: 92
Experience Match: 88
Education Match: 100
Formatting: 96
```

Every score must have an explanation.

---

# 8. SKILL GAP ANALYSIS

Categorize skills:

```text
Strong Match
Partial Match
Missing
```

Example:

```text
React          Strong
Node.js        Strong
PostgreSQL     Strong
Docker         Partial
Kubernetes     Missing
```

IMPORTANT:

A missing skill must NOT be recommended for addition to the resume unless the candidate actually has evidence for it.

Instead say:

> "This requirement appears in the JD but no supporting evidence was found in your profile."

---

# 9. RAG SYSTEM

RAG is a core engineering feature.

Do NOT implement a simplistic:

```text
PDF → embeddings → vector search → LLM
```

Implement:

```text
Candidate Documents
        ↓
Document Parser
        ↓
Chunking
        ↓
Metadata
        ↓
Embeddings
        ↓
PostgreSQL + pgvector
        +
Keyword/BM25 retrieval
        ↓
Hybrid Retrieval
        ↓
RRF
        ↓
Cross-Encoder Reranking
        ↓
Top Evidence
        ↓
LLM
        ↓
Grounded Answer
        ↓
Citations
```

Use metadata such as:

- candidate_id
- resume_id
- version_id
- section
- document_id
- page
- chunk_id
- source_type

---

# 10. HYBRID SEARCH

Implement both:

### Dense retrieval

Semantic similarity using embeddings.

### Lexical retrieval

BM25 or PostgreSQL full-text search.

### Fusion

Use Reciprocal Rank Fusion.

Conceptually:

```text
Dense results
      +
BM25 results
      ↓
RRF
      ↓
Combined ranking
      ↓
Reranker
```

Do not claim hybrid search if only vector search exists.

---

# 11. RERANKING

Use a reranking stage after initial retrieval.

Pipeline:

```text
Top 20–50 retrieved chunks
        ↓
Cross encoder
        ↓
Top 5–10 evidence chunks
        ↓
LLM
```

Make retrieval limits configurable.

---

# 12. CITATIONS / EVIDENCE

Every grounded AI response should expose its evidence.

Example:

```text
Answer:
You have strong backend experience.

Evidence:
[1] VeriSync — Projects — page 2
[2] Experience — Backend Engineer — page 1
```

Users should be able to inspect the source.

If the system cannot find sufficient evidence:

```text
Insufficient evidence.
```

Do NOT fabricate.

---

# 13. AI RESUME GENERATION

AI generation must be grounded.

Pipeline:

```text
Job Description
      ↓
JD Analyzer
      ↓
Required capabilities
      ↓
Retrieve candidate evidence
      ↓
Rank evidence
      ↓
Generate tailored content
      ↓
Claim verification
      ↓
Resume version
```

AI can:

- rewrite bullets
- improve summaries
- tailor experience
- improve project descriptions
- generate professional summaries
- reorder relevant content
- optimize wording for a JD

AI MUST NOT invent:

- companies
- job titles
- skills
- technologies
- metrics
- users
- achievements
- responsibilities
- certifications
- education
- experience

If evidence does not exist, preserve the gap.

---

# 14. CLAIM VERIFICATION

Every generated claim should be checked against the candidate knowledge base.

Conceptually:

```text
Generated claim
      ↓
Claim extraction
      ↓
Evidence retrieval
      ↓
Evidence verification
      ↓
SUPPORTED / UNSUPPORTED
```

Unsupported claims must be rejected or flagged.

This is a major differentiating feature of CareerOS.

---

# 15. AI ASSISTANT

Provide:

### Chat with my Resume

Examples:

> What projects best demonstrate backend development?

> Do I have experience with Docker?

> What are my strongest technical skills?

> What evidence supports my Python experience?

> Which project should I discuss for this job?

Answers must be grounded in the user's knowledge base.

---

# 16. JOB-SPECIFIC RESUME TAILORING

User flow:

```text
Create/select resume
        ↓
Paste/upload JD
        ↓
Analyze JD
        ↓
ATS analysis
        ↓
Skill gap
        ↓
Retrieve candidate evidence
        ↓
Generate recommendations
        ↓
User accepts/rejects changes
        ↓
Create new resume version
        ↓
Run ATS again
        ↓
Show before/after score
```

Never overwrite the original resume automatically.

---

# 17. DATABASE

Use PostgreSQL.

Use pgvector for embeddings.

Design proper relationships.

At minimum support:

```text
users
resumes
resume_versions
resume_sections
experience
education
projects
skills
certifications
documents
document_chunks
embeddings
job_descriptions
ats_reports
ats_findings
ai_generations
generation_evidence
```

Use migrations.

Do not rely on manual database creation.

---

# 18. REDIS

Use Redis for:

- caching
- asynchronous jobs
- document processing
- embedding jobs
- expensive AI operations
- rate limiting where appropriate

Do not introduce Redis merely because it is in the specification. Use it meaningfully.

---

# 19. FASTAPI

Create a clean API.

Examples:

```text
POST /api/resumes
GET  /api/resumes
GET  /api/resumes/{id}
PUT  /api/resumes/{id}

POST /api/resumes/import
POST /api/resumes/{id}/versions

POST /api/jobs
GET  /api/jobs/{id}

POST /api/ats/analyze

POST /api/rag/query

POST /api/ai/rewrite
POST /api/ai/tailor

GET /api/ats/{id}
GET /api/generations/{id}
```

Use:

- Pydantic schemas
- validation
- proper error handling
- authentication boundaries
- structured responses

---

# 20. AUTHENTICATION

Implement proper authentication before production deployment.

Users must only access their own:

- resumes
- documents
- jobs
- ATS reports
- AI generations
- embeddings/evidence

Never expose another user's candidate data.

---

# 21. SECURITY

Never expose API keys in frontend code.

Never commit:

```text
.env
API keys
tokens
database passwords
secrets
```

Use environment variables.

Validate uploads.

Restrict file types.

Apply upload size limits.

Protect endpoints.

---

# 22. TESTING

Do not consider the project complete without tests.

Test:

### Frontend

- builder
- templates
- state
- editing
- versioning

### Backend

- API
- database
- parsing
- ATS
- RAG
- retrieval
- reranking
- generation

### Critical AI safety tests

Test that:

```text
Unsupported skill
        ↓
NOT generated
```

and:

```text
Unsupported metric
        ↓
NOT generated
```

and:

```text
Evidence unavailable
        ↓
System refuses to fabricate
```

Also create a small RAG evaluation dataset.

Measure:

- retrieval relevance
- retrieval recall
- answer faithfulness
- citation correctness
- groundedness

---

# 23. OBSERVABILITY

Implement useful logging.

Track:

- request latency
- retrieval latency
- reranking latency
- generation latency
- token usage where available
- errors
- ingestion failures

Do not log sensitive resume content unnecessarily.

---

# 24. DOCKER

The complete application must be reproducible.

Provide:

```text
docker-compose.yml
```

with services conceptually equivalent to:

```text
frontend
backend
postgres
redis
```

The project should be runnable with a documented command.

Do not leave deployment dependent on undocumented manual steps.

---

# 25. ENVIRONMENT VARIABLES

Create:

`.env.example`

Document every variable.

Example categories:

```text
DATABASE_URL
REDIS_URL

LLM_PROVIDER
LLM_API_KEY

EMBEDDING_PROVIDER
EMBEDDING_API_KEY

NEXT_PUBLIC_API_URL

AUTH_SECRET
```

Never hardcode secrets.

---

# 26. DEPLOYMENT

The final system must be deployable.

Document:

1. Local development.
2. Docker deployment.
3. Production environment variables.
4. Database migrations.
5. Backend deployment.
6. Frontend deployment.
7. Redis setup.
8. PostgreSQL/pgvector setup.
9. File storage strategy.
10. Health checks.
11. Production build.
12. Smoke testing.

Prefer an architecture that can realistically be deployed using services such as:

- Vercel for frontend
- Render/Railway/Fly.io for backend
- managed PostgreSQL with pgvector
- managed Redis

Do not assume a specific provider unless necessary.

---

# 27. CI/CD

Create GitHub Actions for:

```text
push / pull request
        ↓
lint
        ↓
type check
        ↓
unit tests
        ↓
backend tests
        ↓
build
```

Production deployment should only occur after required checks pass.

---

# 28. UI/UX QUALITY

The application must look like a polished SaaS product.

Do not use:

- random gradients everywhere
- excessive animations
- meaningless dashboard cards
- fake statistics
- placeholder buttons
- emoji-heavy interfaces
- inconsistent spacing
- inconsistent typography

Prioritize:

- clean hierarchy
- accessibility
- responsive layouts
- keyboard usability
- loading states
- empty states
- error states
- success states
- skeleton loaders
- clear feedback

The Resume Builder should prioritize the actual editing workflow.

---

# 29. PERFORMANCE

Avoid unnecessary:

- LLM calls
- embedding calls
- database queries
- reranking operations
- frontend rerenders

Use caching where appropriate.

Use background jobs for expensive operations.

Stream long-running AI responses where appropriate.

---

# 30. SOURCE-OF-TRUTH RULE

The canonical candidate profile must be the source of truth.

Do NOT create separate conflicting versions of:

- skills
- projects
- experience
- education

The resume builder, ATS engine, RAG engine and AI generator should ultimately operate on the same underlying candidate data.

---

# 31. NO FAKE COMPLETION

Before marking any feature complete, verify:

```text
UI exists
   ↓
API exists
   ↓
Database integration exists
   ↓
Real data flows through it
   ↓
Errors handled
   ↓
Tests exist
   ↓
Feature works end-to-end
```

A button that only displays a toast is NOT a completed feature.

A score generated from hard-coded values is NOT a completed ATS engine.

A vector database that isn't actually queried is NOT a RAG system.

A generated resume that isn't downloadable is NOT a completed resume generator.

---

# 32. DEVELOPMENT STRATEGY

Do NOT attempt to implement everything at once.

Use phases.

## Phase 0 — Repository audit

Before changing code:

- inspect repository
- inspect package files
- inspect existing code
- inspect README
- identify current state
- identify dependencies
- identify missing architecture

Create:

`docs/ARCHITECTURE.md`

and

`docs/IMPLEMENTATION_PLAN.md`

Do not modify major functionality before this audit.

---

## Phase 1 — Foundation

Implement:

- frontend structure
- FastAPI backend
- PostgreSQL
- Redis
- migrations
- environment configuration
- Docker
- health checks

Verify everything starts correctly.

---

## Phase 2 — Resume Builder

Implement:

- canonical schema
- templates
- editor
- live preview
- drag/drop
- autosave
- versions
- PDF
- DOCX

Verify end-to-end.

---

## Phase 3 — Resume Reader

Implement:

- PDF parser
- DOCX parser
- section extraction
- structured resume extraction
- review/edit workflow

---

## Phase 4 — ATS Engine

Implement:

- JD parser
- keyword extraction
- skill matching
- semantic matching
- formatting checks
- explainable scoring
- recommendations
- before/after comparison

---

## Phase 5 — RAG

Implement:

- chunking
- embeddings
- pgvector
- lexical retrieval
- hybrid retrieval
- RRF
- reranking
- citations

---

## Phase 6 — AI Generation

Implement:

- bullet rewriting
- summary generation
- JD tailoring
- complete resume generation
- claim verification
- evidence display

---

## Phase 7 — Production

Implement:

- authentication
- authorization
- security
- rate limiting
- observability
- tests
- CI/CD
- Docker production configuration
- deployment documentation

---

# 33. ACCEPTANCE CRITERIA

CareerOS is considered complete only when a new user can perform this entire flow:

```text
Register
   ↓
Create resume
   ↓
Choose template
   ↓
Fill/edit sections
   ↓
Drag/reorder content
   ↓
See live preview
   ↓
Save resume
   ↓
Export PDF/DOCX
   ↓
Paste Job Description
   ↓
Analyze JD
   ↓
Run ATS analysis
   ↓
See score
   ↓
See matched skills
   ↓
See missing skills
   ↓
See formatting problems
   ↓
Ask AI questions
   ↓
Retrieve evidence through RAG
   ↓
See citations
   ↓
Tailor resume
   ↓
Verify generated claims
   ↓
Review changes
   ↓
Create new resume version
   ↓
Run ATS again
   ↓
Compare before/after
   ↓
Download final resume
```

Every stage must actually work.

---

# 34. DEFINITION OF DONE

A feature is DONE only when:

- implemented
- integrated
- tested
- documented
- error-handled
- persisted where necessary
- connected to real data
- usable from the UI
- deployable

Do not tell me "this can be added later" for a requirement explicitly defined in this specification.

If implementation must be staged, clearly state the current phase and continue systematically.

---

# 35. FINAL RULE

Think like a senior engineer building a real product that will be used by real job seekers.

Prioritize:

1. correctness
2. data integrity
3. grounded AI
4. security
5. maintainability
6. testability
7. deployment reliability
8. UX quality

Do not optimize for the appearance of complexity.

Build the simplest architecture that genuinely satisfies the requirements.

The final product must be **CareerOS**, not a clone of another repository and not a collection of tutorials.

Every major architectural decision must serve the CareerOS product described above.