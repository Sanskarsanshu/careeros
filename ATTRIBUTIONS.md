# Attributions

CareerOS is an original product built on top of two open-source foundations.

---

## Resume Builder Foundation

**Repository:** https://github.com/giteshChauhan/ai-resume-builder  
**License:** MIT  
**Copyright:** © 2026 Gitesh Chauhan

CareerOS selectively adapts the following components from this repository:
- Template registry architecture (`TemplateProps`, `TemplateDefinition` interfaces)
- Resume template components (Classic, Modern, Executive, Creative) — adapted for server-backed data
- Resume editor form field structure — adapted for API-backed state
- TypeScript resume type interfaces — extended with additional fields

The original client-side architecture (localStorage persistence, browser-based AI, window.print() export) has been replaced with a server-backed architecture in CareerOS.

### MIT License Notice
```
MIT License

Copyright (c) 2026 Gitesh Chauhan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Production RAG Foundation

**Repository:** https://github.com/Ashok007-cmd/production-grade-rag  
**License:** MIT  
**Copyright:** © 2026 Ashok007-cmd

CareerOS selectively adapts the following components from this repository:
- Hybrid retrieval architecture (dense + lexical + RRF fusion) — adapted to PostgreSQL pgvector + FTS
- Cross-encoder reranking interface — adapted with abstraction layer
- Citation format and grounded answer pattern
- FastAPI middleware patterns (X-Request-ID, health checks, structured error responses)
- OpenTelemetry + Prometheus observability patterns
- Dockerfile multi-stage build pattern
- RAGAS-style evaluation dataset pattern

The original ChromaDB vector store and rank-bm25 library have been replaced with PostgreSQL pgvector and PostgreSQL Full-Text Search in CareerOS. The Anthropic LLM provider has been replaced with Google Gemini as the secondary provider.

### MIT License Notice
```
MIT License

Copyright (c) 2026 Ashok007-cmd

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## CareerOS

CareerOS itself is an original product. Code not derived from the above repositories is original work.
