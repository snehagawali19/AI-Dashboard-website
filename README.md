<<<<<<< HEAD
# AI NewsPulse — AI News Aggregation & Broadcasting Dashboard

A production-quality MVP that aggregates AI news from 20+ RSS sources,
applies GPT-4o-mini for summarisation and caption generation, and
simulates broadcasting to Email, LinkedIn, and WhatsApp.

## Features

- **20+ AI news sources** — RSS ingestion every 15 minutes via APScheduler
- **AI Summaries** — GPT-4o-mini 2-3 sentence summaries per article
- **AI Captions** — LinkedIn posts and email newsletter snippets auto-generated
- **Tag Extraction** — Topic tags extracted for filtering
- **Semantic Dedup** — text-embedding-3-small cosine similarity deduplication
- **Favorites** — Save articles across sessions
- **Broadcast Simulation** — Email / LinkedIn / WhatsApp mock with preview
- **Infinite scroll** + tag filter pills in the dashboard

## Tech Stack

| Layer      | Technology                                  |
| ---------- | ------------------------------------------- |
| Backend    | FastAPI 0.111, Python 3.11                  |
| Database   | PostgreSQL 16 + SQLAlchemy 2.0              |
| Migrations | Alembic                                     |
| AI         | OpenAI GPT-4o-mini + text-embedding-3-small |
| Scheduler  | APScheduler                                 |
| Frontend   | Next.js 14 App Router + Tailwind CSS        |
| Deployment | Render.com                                  |
| Containers | Docker + Docker Compose                     |

## Architecture Decisions

- **FastAPI** chosen for async support (critical for parallel AI calls), auto-docs, and Python-native AI library compatibility
- **Two-layer dedup**: URL hash (O(1), zero API cost) first; semantic embedding cosine similarity only for unprocessed items (batched to respect rate limits)
- **Background AI processing**: Items are stored immediately on ingestion; AI enrichment runs asynchronously in a 5-minute scheduler job — ensures the API is never blocked on OpenAI
- **Mock broadcasting**: Handlers are swappable; replace `_mock_email` with a real SendGrid call in one line
- **Demo user**: Auth is mocked with a fixed UUID for MVP speed; add JWT via `fastapi-users` for production

## Cost Estimate (GPT-4o-mini)

- Summary + 2 captions + tags ≈ ~800 tokens per article
- 500 articles/day × 800 tokens = 400K tokens/day ≈ $0.06/day
=======
# AI-News-Dashboard
>>>>>>> 534c79b5043ccc1b846eb1a6fabad71d6420cca5
