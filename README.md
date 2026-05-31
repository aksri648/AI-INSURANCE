# Insurance Copilot

Evidence-Based Insurance Intelligence Platform

## Architecture

```
┌─────────────────────┐      ┌──────────────────────┐
│   React 19 Frontend │─────▶│   FastAPI Backend     │
│   Vite + Tailwind   │      │   CrewAI + pgvector   │
│   Clerk Auth        │      │   Ollama + Groq       │
└─────────────────────┘      └──────────┬───────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    ▼                   ▼                   ▼
            ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
            │  PostgreSQL  │   │    Ollama    │   │    Redis     │
            │   + pgvector │   │  LLM Models  │   │   Cache/Queue│
            └──────────────┘   └──────────────┘   └──────────────┘
```

## Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 16+ with pgvector extension
- Docker & Docker Compose (optional)
- Ollama (running locally or remotely)
- Clerk account (for authentication)

## Quick Start (Docker)

```bash
# 1. Clone and set up environment
cp BACKEND/.env.example BACKEND/.env
# Edit BACKEND/.env with your API keys

# 2. Start infrastructure
docker compose up -d postgres ollama redis

# 3. Pull Ollama models
docker compose exec ollama ollama pull qwen3:8b
docker compose exec ollama ollama pull nomic-embed-text

# 4. Start backend
docker compose up -d backend

# 5. Start frontend
cd FRONTEND
cp .env.example .env
npm install
npm run dev
```

## Manual Setup

### Backend

```bash
cd BACKEND

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd FRONTEND

# Install dependencies
npm install

# Set up environment
cp .env.example .env
# Edit .env with your Clerk publishable key

# Start development server
npm run dev
```

## Environment Variables

### Backend (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL async URL | postgresql+asyncpg://postgres:postgres@localhost:5432/insurance_copilot |
| CLERK_API_KEY | Clerk secret key | - |
| OLLAMA_BASE_URL | Ollama server URL | http://localhost:11434 |
| OLLAMA_PRIMARY_MODEL | Primary LLM model | qwen3:8b |
| OLLAMA_FALLBACK_MODEL | Fallback LLM model | qwen3:14b |
| GROQ_API_KEY | Groq API key (fallback) | - |
| TAVILY_API_KEY | Tavily search API key | - |

### Frontend (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| VITE_CLERK_PUBLISHABLE_KEY | Clerk publishable key | - |
| VITE_API_URL | Backend API URL | http://localhost:8000 |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| GET/PUT | /api/auth/me | Current user |
| GET | /api/auth/stats | User statistics |
| POST | /api/policies/upload | Upload policy document |
| GET | /api/policies/ | List policies |
| GET | /api/policies/{id} | Get policy details |
| POST | /api/policies/{id}/analyze | Analyze policy |
| POST | /api/chat/policy/{id} | Chat with policy |
| POST | /api/claims/assess | Assess claim |
| POST | /api/companies/search | Search company |
| POST | /api/companies/compare | Compare companies |
| POST | /api/education/explain | Learn insurance topic |
| POST | /api/education/mis-selling-check | Check mis-selling |

## AI Safety Rules

1. **Never hallucinate** policy details, benefits, coverage, or exclusions
2. **Every fact** must be evidence-backed from uploaded documents
3. **Confidence system**: 🟢 Verified, 🟡 Needs Review, 🔴 Not Found
4. **Fallback message**: "Information could not be verified from available sources."
5. **Simple language**: 8th-grade reading level for all user-facing content

## CrewAI Agents

1. **Policy Analysis Agent** - Extracts structured policy details
2. **Recommendation Agent** - Generates personalized coverage recommendations
3. **Mis-selling Detection Agent** - Detects misleading statements
4. **Claims Assessment Agent** - Analyzes claim readiness
5. **Insurance Education Agent** - Explains concepts simply
6. **Evidence Validation Agent** - Verifies factual claims
7. **Grounding Validation Agent** - Ensures citation accuracy
8. **Report Generation Agent** - Produces final reports
9. **Company Intelligence Agent** - Researches insurers
10. **Research Agent** - External research via Tavily

## Report Structure (25 Sections)

- Quick Summary
- Benefits Breakdown
- Coverage Tables
- Exclusions
- Waiting Periods
- Hidden Conditions
- Claim Experience Score
- Coverage Adequacy
- Suggestions
- Mis-selling Detection
- Example Claim Scenarios
- Company Trust Score
- Sources & Evidence
- Final Verdict

## Testing

```bash
# Backend tests
cd BACKEND
pytest tests/ -v

# Frontend tests
cd FRONTEND
npm run test
```

## Deployment

```bash
# Build frontend
cd FRONTEND
npm run build

# Build backend Docker image
cd BACKEND
docker build -t insurance-copilot-backend .

# Deploy with Docker Compose
docker compose up -d
```
