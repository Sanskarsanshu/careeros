# CareerOS — Source Repository Audit

**Audit Date:** 2026-08-31  
**Status:** COMPLETE (Phase 0)

---

## 1. CareerOS Repository (Target)

**URL:** https://github.com/Sanskarsanshu/careeros  
**Local path:** `c:\Users\sansk\OneDrive\Desktop\careeros\`

### Current State at Audit Time

| Item | Status |
|------|--------|
| Files present | 1 (master specification markdown) |
| Frontend code | NONE |
| Backend code | NONE |
| Database migrations | NONE |
| Docker configuration | NONE |
| Tests | NONE |

**Conclusion:** Green-field repository. Phase 0 applies in full.

---

## 2. Resume Builder Foundation

**URL:** https://github.com/giteshChauhan/ai-resume-builder  
**License:** MIT — Copyright © 2026 Gitesh Chauhan  
**Stack:** Next.js 16.2.6, React 19, TypeScript, Tailwind CSS v4, Zustand v5

### Key Characteristics
- 100% client-side; no backend, no database, no auth
- localStorage persistence via Zustand `persist` middleware
- Client-side AI (user pastes API key into browser)
- Print-based PDF via `window.print()` + `@page` CSS
- ATS scoring is client-side heuristics only (`lib/ats.ts`)
- Clean template registry pattern (reusable)

### Existing Data Model (`lib/types.ts`)
```typescript
interface Resume {
  name, title, photo?, contact, summary,
  workExperience[], projects[], education[],
  skills[], softwareLogos?, pageBreaks[], templateId?
}
```
Missing from CareerOS spec: certifications, achievements, publications, links, customSections, versioning.

---

## 3. Production RAG Foundation

**URL:** https://github.com/Ashok007-cmd/production-grade-rag  
**License:** MIT  
**Stack:** FastAPI, Python, ChromaDB, rank-bm25, sentence-transformers, OpenAI/Anthropic

### Key Characteristics
- Full hybrid pipeline: BM25 + ChromaDB vector + RRF + CrossEncoder reranking
- 147 tests, RAGAS-style LLM-as-Judge evaluation
- SSE streaming, async ingestion, OpenTelemetry, Langfuse tracing
- Reranker: `cross-encoder/ms-marco-MiniLM-L-6-v2` (configurable via `RAG_RERANKER_MODEL`)
- Default: chunk_size=800, chunk_overlap=150, top_k_retrieval=20, top_k_final=5

---

## 4. Reuse Decisions

### From Resume Builder — REUSE
| Component | Decision |
|-----------|----------|
| Template registry pattern (types.ts, index.ts) | ✅ REUSE |
| 4 template components | ✅ ADAPT (server data) |
| Resume type interface | ✅ EXTEND |
| EditorPanel form structure | ✅ ADAPT (API-backed state) |
| Zustand patterns | ✅ UI state only |

### From Resume Builder — DISCARD
| Component | Reason |
|-----------|--------|
| Client-side AI (browser API key) | Backend owns AI |
| `window.print()` PDF | Server-side PDF needed |
| localStorage persistence | PostgreSQL via API |

### From Production RAG — REUSE
| Component | Decision |
|-----------|----------|
| Chunking strategy | ✅ ADAPT (candidate metadata) |
| RRF fusion logic | ✅ REUSE |
| Cross-encoder reranking interface | ✅ REUSE |
| Citation format | ✅ EXTEND |
| FastAPI patterns, middleware | ✅ REUSE |
| OpenTelemetry + Prometheus | ✅ REUSE |
| Dockerfile multi-stage pattern | ✅ REUSE |
| RAGAS evaluation pattern | ✅ REUSE |

### From Production RAG — REPLACE
| Component | Replacement |
|-----------|-------------|
| ChromaDB | pgvector (Decision 5) |
| rank-bm25 | PostgreSQL FTS (Decision 6) |
| Anthropic as secondary | Gemini (Decision 3) |

---

## 5. Conflicts Resolved

| Conflict | Resolution |
|----------|------------|
| ChromaDB vs pgvector | pgvector — Decision 5 |
| BM25 vs PostgreSQL FTS | PostgreSQL FTS — Decision 6 |
| Client ATS vs backend ATS | Backend — spec requirement |
| Client AI vs backend AI | Backend — spec requirement |
| Anthropic secondary vs Gemini | Gemini — Decision 3 |

---

## 6. License Compliance

Both source repositories use MIT license. CareerOS must:
1. Include copyright notices in `ATTRIBUTIONS.md`
2. Not falsely claim all code originates from these repos
